# In bash this requires https://github.com/rcaloras/bash-preexec
# If sourcing this via ntfy auto-done, it is sourced for you.

# Default to ignoring some well known interactive programs
AUTO_NTFY_DONE_IGNORE=${AUTO_NTFY_DONE_IGNORE:-ntfy emacs info less mail man meld most mutt nano screen ssh tail tmux vi vim watch}
# Bash option example
#AUTO_NTFY_DONE_OPTS='-b default'
# Zsh option example
#AUTO_NTFY_DONE_OPTS=(-b default)
# notify for unfocused only (Used by ntfy internally)
#AUTO_NTFY_DONE_UNFOCUSED_ONLY=-b
# notify for commands runing longer than N sec only (Used by ntfy internally)
#AUTO_NTFY_DONE_LONGER_THAN=-L10

function _ntfy_precmd () {
    [ -n "$ntfy_start_time" ] || return
    local duration=$(( $(date +%s) - $ntfy_start_time ))
    ntfy_start_time=''

    local appname=$(basename "${ntfy_command%% *}")
    [[ " $AUTO_NTFY_DONE_IGNORE " == *" $appname "* ]] && return

    ntfy $AUTO_NTFY_DONE_OPTS done \
        $AUTO_NTFY_DONE_UNFOCUSED_ONLY $AUTO_NTFY_DONE_LONGER_THAN \
        --formatter "$ntfy_command" $__bp_last_ret_value $duration
}

function _ntfy_preexec () {
    ntfy_start_time=$(date +%s)
    ntfy_command=$(echo "$1")
}

function _contains_element() {
    local e
    for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}

if ! _contains_element _ntfy_preexec "${preexec_functions[@]}"; then
    preexec_functions+=(_ntfy_preexec)
fi

if ! _contains_element _ntfy_precmd "${precmd_functions[@]}"; then
    precmd_functions+=(_ntfy_precmd)
fi
