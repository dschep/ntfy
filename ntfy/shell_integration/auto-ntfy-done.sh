# In bash this requires https://github.com/rcaloras/bash-preexec
# If sourcing this via ntfy auto-done, it is sourced for you.

# Default timeout is 10 seconds.
AUTO_NTFY_DONE_TIMEOUT=${AUTO_NTFY_DONE_TIMEOUT:-10}
# Default to ignoring some well known interactive programs
AUTO_NTFY_DONE_IGNORE=${AUTO_NTFY_DONE_IGNORE:-ntfy emacs info less mail man meld most mutt nano screen ssh sudo tail tmux vi vim}
# Bash option example
#AUTO_NTFY_DONE_OPTS='-b default'
# Zsh option example
#AUTO_NTFY_DONE_OPTS=(-b default)
# force emoji example
#AUTO_NTFY_DONE_EMOJI=true

function ntfy_precmd () {
    [ -n "$ntfy_start_time" ] || return
    local duration=$(( $(date +%s) - $ntfy_start_time ))
    ntfy_start_time=''
    [ $duration -gt $AUTO_NTFY_DONE_TIMEOUT ] || return

    local appname=$(basename "${ntfy_command%% *}")
    [[ " $AUTO_NTFY_DONE_IGNORE " == *" $appname "* ]] && return

    local human_duration=$(printf '%d:%02d\n' $(($duration/60)) $(($duration%60)))
    local human_retcode
    [ "$ret_value" -eq 0 ] && human_retcode='succeeded' || human_retcode='failed'
    local prefix
    if [[ "$AUTO_NTFY_DONE_EMOJI" == "true" ]]; then
        [ "$ret_value" -eq 0 ] && prefix=':white_check_mark: ' || prefix=':x: '
    fi
    ntfy $AUTO_NTFY_DONE_OPTS -l ERROR send "$prefix\"$ntfy_command\" $human_retcode in $human_duration minutes"
}

function ntfy_preexec () {
    ntfy_start_time=$(date +%s)
    ntfy_command=$(echo "$1")
}

function contains_element() {
    local e
    for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}

if ! contains_element ntfy_preexec "${preexec_functions[@]}"; then
    preexec_functions+=(ntfy_preexec)
fi

if ! contains_element ntfy_precmd "${precmd_functions[@]}"; then
    precmd_functions+=(ntfy_precmd)
fi
