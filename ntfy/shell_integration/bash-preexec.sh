#!/bin/bash
#
# bash-preexec.sh -- Bash support for ZSH-like 'preexec' and 'precmd' functions.
# https://github.com/rcaloras/bash-preexec
#
#
# 'preexec' functions are executed before each interactive command is
# executed, with the interactive command as its argument. The 'precmd'
# function is executed before each prompt is displayed.
#
# Author: Ryan Caloras (ryan@bashhub.com)
# Forked from Original Author: Glyph Lefkowitz
#
# V0.3.0
#

# General Usage:
#
#  1. Source this file at the end of your bash profile so as not to interfere
#     with anything else that's using PROMPT_COMMAND.
#
#  2. Add any precmd or preexec functions by appending them to their arrays:
#       e.g.
#       precmd_functions+=(my_precmd_function)
#       precmd_functions+=(some_other_precmd_function)
#
#       preexec_functions+=(my_preexec_function)
#
#  3. If you have anything that's using the Debug Trap, change it to use
#     preexec. (Optional) change anything using PROMPT_COMMAND to now use
#     precmd instead.
#
#  Note: This module requires two bash features which you must not otherwise be
#  using: the "DEBUG" trap, and the "PROMPT_COMMAND" variable. prexec_and_precmd_install
#  will override these and if you override one or the other this will most likely break.

# Avoid duplicate inclusion
if [[ "$__bp_imported" == "defined" ]]; then
    return 0
fi
__bp_imported="defined"

# Should be available to each precmd and preexec
# functions, should they want it.
__bp_last_command_ret_value="$?"

# Command to set our preexec trap. It's invoked once via
# PROMPT_COMMAND and then removed.
__bp_trap_install_string="trap '__bp_preexec_invoke_exec' DEBUG;"

# Remove ignorespace and or replace ignoreboth from HISTCONTROL
# so we can accurately invoke preexec with a command from our
# history even if it starts with a space.
__bp_adjust_histcontrol() {
    local histcontrol
    histcontrol="${HISTCONTROL//ignorespace}"
    # Replace ignoreboth with ignoredups
    if [[ "$histcontrol" == *"ignoreboth"* ]]; then
        histcontrol="ignoredups:${histcontrol//ignoreboth}"
    fi;
    export HISTCONTROL="$histcontrol"
}

# This variable describes whether we are currently in "interactive mode";
# i.e. whether this shell has just executed a prompt and is waiting for user
# input.  It documents whether the current command invoked by the trace hook is
# run interactively by the user; it's set immediately after the prompt hook,
# and unset as soon as the trace hook is run.
__bp_preexec_interactive_mode=""

__bp_trim_whitespace() {
    local var=$@
    var="${var#"${var%%[![:space:]]*}"}"   # remove leading whitespace characters
    var="${var%"${var##*[![:space:]]}"}"   # remove trailing whitespace characters
    echo -n "$var"
}

# This function is installed as part of the PROMPT_COMMAND;
# It sets a variable to indicate that the prompt was just displayed,
# to allow the DEBUG trap to know that the next command is likely interactive.
__bp_interactive_mode() {
    __bp_preexec_interactive_mode="on";
}


# This function is installed as part of the PROMPT_COMMAND.
# It will invoke any functions defined in the precmd_functions array.
__bp_precmd_invoke_cmd() {

    # Should be available to each precmd function, should it want it.
    __bp_last_ret_value="$?"

    # For every function defined in our function array. Invoke it.
    local precmd_function
    for precmd_function in "${precmd_functions[@]}"; do

        # Only execute this function if it actually exists.
        # Test existence of functions with: declare -[Ff]
        if type -t "$precmd_function" 1>/dev/null; then
            __bp_set_ret_value $__bp_last_ret_value
            $precmd_function
        fi
    done
}

# Sets a return value in $?. We may want to get access to the $? variable in our
# precmd functions. This is available for instance in zsh. We can simulate it in bash
# by setting the value here.
__bp_set_ret_value() {
    return $1
}

__bp_in_prompt_command() {

    local prompt_command_array
    IFS=';' read -ra prompt_command_array <<< "$PROMPT_COMMAND"

    local trimmed_arg
    trimmed_arg=$(__bp_trim_whitespace "$1")

    local command
    for command in "${prompt_command_array[@]}"; do
        local trimmed_command
        trimmed_command=$(__bp_trim_whitespace "$command")
        # Only execute each function if it actually exists.
        if [[ "$trimmed_command" == "$trimmed_arg" ]]; then
            return 0
        fi
    done

    return 1
}

# This function is installed as the DEBUG trap.  It is invoked before each
# interactive prompt display.  Its purpose is to inspect the current
# environment to attempt to detect if the current command is being invoked
# interactively, and invoke 'preexec' if so.
__bp_preexec_invoke_exec() {

    # Checks if the file descriptor is not standard out (i.e. '1')
    # __bp_delay_install checks if we're in test. Needed for bats to run.
    # Prevents preexec from being invoked for functions in PS1
    if [[ ! -t 1 && -z "$__bp_delay_install" ]]; then
        return
    fi

    if [[ -n "$COMP_LINE" ]]; then
        # We're in the middle of a completer. This obviously can't be
        # an interactively issued command.
        return
    fi
    if [[ -z "$__bp_preexec_interactive_mode" ]]; then
        # We're doing something related to displaying the prompt.  Let the
        # prompt set the title instead of me.
        return
    else
        # If we're in a subshell, then the prompt won't be re-displayed to put
        # us back into interactive mode, so let's not set the variable back.
        # In other words, if you have a subshell like
        #   (sleep 1; sleep 2)
        # You want to see the 'sleep 2' as a set_command_title as well.
        if [[ 0 -eq "$BASH_SUBSHELL" ]]; then
            __bp_preexec_interactive_mode=""
        fi
    fi

    if  __bp_in_prompt_command "$BASH_COMMAND"; then
        # If we're executing something inside our prompt_command then we don't
        # want to call preexec. Bash prior to 3.1 can't detect this at all :/
        __bp_preexec_interactive_mode=""
        return
    fi

    local this_command
    this_command=$(HISTTIMEFORMAT= history 1 | { read -r _ this_command; echo "$this_command"; })

    # Sanity check to make sure we have something to invoke our function with.
    if [[ -z "$this_command" ]]; then
        return
    fi

    # If none of the previous checks have returned out of this function, then
    # the command is in fact interactive and we should invoke the user's
    # preexec functions.

    # For every function defined in our function array. Invoke it.
    local preexec_function
    for preexec_function in "${preexec_functions[@]}"; do

        # Only execute each function if it actually exists.
        # Test existence of function with: declare -[fF]
        if type -t "$preexec_function" 1>/dev/null; then
            __bp_set_ret_value $__bp_last_ret_value
            $preexec_function "$this_command"
        fi
    done
}

# Returns PROMPT_COMMAND with a semicolon appended
# if it doesn't already have one.
__bp_prompt_command_with_semi_colon() {

    # Trim our existing PROMPT_COMMAND
    local trimmed
    trimmed=$(__bp_trim_whitespace "$PROMPT_COMMAND")

    # Take our existing prompt command and append a semicolon to it
    # if it doesn't already have one.
    local existing_prompt_command
    if [[ -n "$trimmed" ]]; then
        existing_prompt_command=${trimmed%${trimmed##*[![:space:]]}}
        existing_prompt_command=${existing_prompt_command%;}
        existing_prompt_command=${existing_prompt_command/%/;}
    else
        existing_prompt_command=""
    fi

    echo -n "$existing_prompt_command"
}

__bp_install() {

    # Remove setting our trap from PROMPT_COMMAND
    PROMPT_COMMAND="${PROMPT_COMMAND//$__bp_trap_install_string}"

    # Remove this function from our PROMPT_COMMAND
    PROMPT_COMMAND="${PROMPT_COMMAND//__bp_install;}"

    # Exit if we already have this installed.
    if [[ "$PROMPT_COMMAND" == *"__bp_precmd_invoke_cmd"* ]]; then
        return 1;
    fi

    # Adjust our HISTCONTROL Variable if needed.
    __bp_adjust_histcontrol

    # Set so debug trap will work be invoked in subshells.
    set -o functrace > /dev/null 2>&1
    shopt -s extdebug > /dev/null 2>&1


    local existing_prompt_command
    existing_prompt_command=$(__bp_prompt_command_with_semi_colon)

    # Install our hooks in PROMPT_COMMAND to allow our trap to know when we've
    # actually entered something.
    PROMPT_COMMAND="__bp_precmd_invoke_cmd; ${existing_prompt_command} __bp_interactive_mode;"
    trap '__bp_preexec_invoke_exec' DEBUG;

    # Add two functions to our arrays for convenience
    # of definition.
    precmd_functions+=(precmd)
    preexec_functions+=(preexec)

    # Since this is in PROMPT_COMMAND, invoke any precmd functions we have defined.
    __bp_precmd_invoke_cmd
    # Put us in interactive mode for our first command.
    __bp_interactive_mode
}

# Sets our trap and __bp_install as part of our PROMPT_COMMAND to install
# after our session has started. This allows bash-preexec to be inlucded
# at any point in our bash profile. Ideally we could set our trap inside
# __bp_install, but if a trap already exists it'll only set locally to
# the function.
__bp_install_after_session_init() {

    # Make sure this is bash that's running this and return otherwise.
    if [[ -z "$BASH_VERSION" ]]; then
        return 1;
    fi

    local existing_prompt_command
    existing_prompt_command=$(__bp_prompt_command_with_semi_colon)

    # Add our installation to be done last via our PROMPT_COMMAND. These are
    # removed by __bp_install when it's invoked so it only runs once.
    PROMPT_COMMAND="${existing_prompt_command} $__bp_trap_install_string __bp_install;"
}

# Run our install so long as we're not delaying it.
if [[ -z "$__bp_delay_install" ]]; then
    __bp_install_after_session_init
fi;
