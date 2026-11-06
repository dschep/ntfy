import os
import shutil
import subprocess
from pathlib import Path
from unittest import TestCase, skipUnless


BASH_PREEXEC = (
    Path(__file__).resolve().parents[1]
    / "ntfy" / "shell_integration" / "bash-preexec.sh"
)


@skipUnless(shutil.which("bash"), "Bash is required for shell integration tests")
class BashPreexecHistoryControlTests(TestCase):
    def run_bash(self, script):
        env = os.environ.copy()
        env.pop("HISTCONTROL", None)
        return subprocess.run(
            ["bash", "--noprofile", "--norc", "-c", script, "bash", str(BASH_PREEXEC)],
            env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=True,
        ).stdout.strip()

    def test_ignorespace_is_removed_from_value_but_remembered(self):
        output = self.run_bash(
            'HISTCONTROL=ignorespace; '
            '__bp_delay_install=1; source "$1"; '
            '__bp_adjust_histcontrol; '
            'printf "%s|%s" "$HISTCONTROL" "$__bp_ignorespace"',
            )
        self.assertEqual(output, "|yes")

    def test_ignoreboth_keeps_ignoredups_and_remembers_space_policy(self):
        output = self.run_bash(
            'HISTCONTROL=ignoreboth; '
            '__bp_delay_install=1; source "$1"; '
            '__bp_adjust_histcontrol; '
            'printf "%s|%s" "$HISTCONTROL" "$__bp_ignorespace"',
        )
        self.assertEqual(output, "ignoredups|yes")

    def test_other_histcontrol_options_are_preserved(self):
        output = self.run_bash(
            'HISTCONTROL=ignorespace:erasedups:ignoredups; '
            '__bp_delay_install=1; source "$1"; '
            '__bp_adjust_histcontrol; printf "%s" "$HISTCONTROL"',
        )
        self.assertEqual(output, "erasedups:ignoredups")
