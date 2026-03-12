"""Custom help panels for the paude CLI."""

from __future__ import annotations

from typing import Any

import typer.rich_utils
from rich.console import Console, Group
from rich.padding import Padding
from rich.table import Table
from rich.text import Text
from typer.core import TyperGroup

HELP_WIDTH = 120

_HelpSection = tuple[str, list[tuple[str, str]] | str]

_HELP_SECTIONS: list[_HelpSection] = [
    (
        "Workflow (Quick Start)",
        [
            (
                "paude create my-project --git",
                "Create, start, push code+tags, set origin",
            ),
            (
                "paude connect my-project",
                "Connect to running session",
            ),
        ],
    ),
    (
        "Workflow (Manual)",
        [
            (
                "paude create my-project",
                "Create and start session",
            ),
            (
                "paude remote add --push my-project",
                "Init git repo + push code",
            ),
            (
                "paude connect my-project",
                "Connect to running session",
            ),
        ],
    ),
    (
        "Workflow (Later)",
        [
            (
                "paude connect",
                "Reconnect to running session",
            ),
            (
                "git push paude-<name> main",
                "Push more changes to container",
            ),
            (
                "paude stop",
                "Stop session (preserves data)",
            ),
            (
                "paude delete NAME --confirm",
                "Delete session permanently",
            ),
        ],
    ),
    (
        "Syncing Code (via git)",
        [
            (
                "paude remote add [NAME]",
                "Add git remote (requires running container)",
            ),
            (
                "paude remote add --push [NAME]",
                "Add remote AND push current branch",
            ),
            (
                "paude remote list",
                "List all paude git remotes",
            ),
            (
                "paude remote remove [NAME]",
                "Remove git remote for session",
            ),
            (
                "paude remote cleanup",
                "Remove remotes for deleted sessions",
            ),
            (
                "git push paude-<name> main",
                "Push code to container",
            ),
            (
                "git pull paude-<name> main",
                "Pull changes from container",
            ),
        ],
    ),
    (
        "Copying Files (without git)",
        [
            (
                "paude cp ./file.txt my-session:file.txt",
                "Copy local file to session",
            ),
            (
                "paude cp my-session:output.log ./",
                "Copy file from session to local",
            ),
            (
                "paude cp ./src :src",
                "Auto-detect session, copy dir",
            ),
            (
                "paude cp :results ./results",
                "Auto-detect session, copy from",
            ),
        ],
    ),
    (
        "Egress Filtering",
        [
            (
                "paude allowed-domains NAME",
                "Show current domains",
            ),
            (
                "paude allowed-domains NAME --add DOMAIN",
                "Add domain to list",
            ),
            (
                "paude allowed-domains NAME --remove DOMAIN",
                "Remove domain",
            ),
            (
                "paude allowed-domains NAME --replace DOMAIN...",
                "Replace entire list",
            ),
            (
                "paude blocked-domains NAME",
                "Show blocked domains",
            ),
            (
                "paude blocked-domains NAME --raw",
                "Show raw proxy log",
            ),
        ],
    ),
    (
        "Examples",
        [
            (
                "paude create --yolo --allowed-domains all",
                "Full autonomy (DANGEROUS)",
            ),
            (
                "paude create --allowed-domains default "
                "--allowed-domains .example.com",
                "Add custom domain to defaults",
            ),
            (
                "paude create --allowed-domains .example.com",
                "Allow ONLY custom domain (replaces defaults)",
            ),
            (
                "paude create -a '-p \"prompt\"'",
                "Create session with initial prompt",
            ),
            (
                "paude create --dry-run",
                "Verify configuration without creating",
            ),
            (
                "paude create --backend=openshift",
                "Create session on OpenShift cluster",
            ),
        ],
    ),
    (
        "Security",
        "By default, paude runs with network restricted to Vertex AI, "
        "PyPI, and GitHub. Use --allowed-domains all to permit all network "
        "access (enables data exfil). Combining --yolo with "
        "--allowed-domains all is maximum risk mode. PAUDE_GITHUB_TOKEN is "
        "explicit only; host GH_TOKEN is never auto-propagated.",
    ),
    (
        "Agents",
        [
            ("--agent claude", "Claude Code (default)"),
            ("--agent cursor", "Cursor CLI"),
            ("--agent gemini", "Gemini CLI"),
        ],
    ),
]


class PaudeGroup(TyperGroup):
    """Click group that appends extra reference panels to help."""

    def format_help(self, ctx: Any, formatter: Any) -> None:
        terminal_width = Console().width
        width = min(terminal_width, HELP_WIDTH)
        typer.rich_utils.MAX_WIDTH = width
        super().format_help(ctx, formatter)
        console = Console(width=width)
        for title, content in _HELP_SECTIONS:
            if isinstance(content, str):
                body: Table | Padding = Padding(
                    Text(content), (0, 1)
                )
            else:
                body = Table(
                    highlight=True,
                    show_header=False,
                    expand=True,
                    box=None,
                    padding=(0, 1),
                )
                body.add_column(ratio=3, style="green")
                body.add_column(ratio=2)
                for cmd, desc in content:
                    body.add_row(cmd, desc)
            heading = Text(f" {title}\n", style="bold")
            console.print(
                Padding(Group(heading, body), (1, 0, 0, 0))
            )
