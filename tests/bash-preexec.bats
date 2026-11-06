#!/usr/bin/env bats

setup() {
    export __bp_delay_install=1
    source "${BATS_TEST_DIRNAME}/../ntfy/shell_integration/bash-preexec.sh"
}

test_preexec_echo() {
    echo "$1"
}

@test "space-prefixed commands are passed to preexec and removed from history" {
    preexec_functions+=(test_preexec_echo)
    HISTCONTROL=ignorespace:ignoreboth

    __bp_adjust_histcontrol
    [[ "$HISTCONTROL" == "ignoredups" ]]

    __bp_interactive_mode
    command1="this command is in the history"
    history -s "$command1"
    run __bp_preexec_invoke_exec
    [ "$status" -eq 0 ]
    [ "$output" = "$command1" ]
    last_history=$(HISTTIMEFORMAT= history 1 | sed '1 s/^ *[0-9][0-9]* *//')
    [ "$last_history" = "$command1" ]

    command2=" this sensitive command must not be retained"
    history -s "$command2"
    output=$(__bp_preexec_invoke_exec && printf "last_history: %s\n"         "$(HISTTIMEFORMAT= history 1 | sed '1 s/^ *[0-9][0-9]* *//')")
    [ "$output" = "$command2"$'\n'"last_history: $command1" ]
}

@test "ignoreboth and ignorespace are normalized without empty separators" {
    HISTCONTROL=ignorespace:ignoredups
    __bp_adjust_histcontrol
    [ "$HISTCONTROL" = "ignoredups" ]

    HISTCONTROL=ignoreboth
    __bp_adjust_histcontrol
    [ "$HISTCONTROL" = "ignoredups" ]

    HISTCONTROL=ignoreboth:erasedups
    __bp_adjust_histcontrol
    [ "$HISTCONTROL" = "ignoredups:erasedups" ]
}
