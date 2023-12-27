# In bash this requires https://github.com/rcaloras/bash-preexec
# If sourcing this via ntfy auto-done, it is sourced for you.

# Default to ignoring some well known interactive programs
set -x AUTO_NTFY_DONE_IGNORE $AUTO_NTFY_DONE_IGNORE ntfy emacs htop info less mail man meld most mutt nano screen ssh tail tmux top vi vim watch
# Bash option example
#AUTO_NTFY_DONE_OPTS='-b default'
# Zsh option example
#AUTO_NTFY_DONE_OPTS=(-b default)
# notify for unfocused only (Used by ntfy internally)
#AUTO_NTFY_DONE_UNFOCUSED_ONLY=-b
# notify for commands runing longer than N sec only (Used by ntfy internally)
#set -x AUTO_NTFY_DONE_LONGER_THAN -L60

function _ntfy_precmd --on-event fish_postexec
    set -l ret_value $status
    test $ntfy_start_time || return
    set -l appname (basename (string split ' ' $argv)[1])
    contains $appname $AUTO_NTFY_DONE_IGNORE && return
    set -l ntfy_command $argv
    set -l duration (math (date +%s) - $ntfy_start_time)

    ntfy $AUTO_NTFY_DONE_OPTS done \
        $AUTO_NTFY_DONE_UNFOCUSED_ONLY $AUTO_NTFY_DONE_LONGER_THAN \
        --formatter $ntfy_command $ret_value $duration &
end

function _ntfy_preexec --on-event fish_preexec 
    set -g ntfy_start_time (date +%s)
end
