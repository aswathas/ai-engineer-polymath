"""Tests for the agent-pack validator (``tools/validators/validate_agents.py``).

The fixtures live in this file on purpose: the agent validator's contract is asserted in
one place, without touching the shared ``tests/conftest.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.validators.validate_agents import validate

AGENT_NAMES = (
    "polymath-tutor",
    "polymath-reviewer",
    "polymath-quiz-master",
    "polymath-curator",
    "polymath-project-supervisor",
    "polymath-eval-auditor",
)

SECTION_ORDER = (
    "Role",
    "Triggers",
    "Hard Rules",
    "Workflow",
    "Output Contract",
    "Refusals",
)

DEFAULT_DESCRIPTION = (
    "Teaches a module of the curriculum, explains the concepts behind it, and quizzes the "
    "learner instead of writing the implementation for them."
)

SECTION_BODIES: dict[str, str] = {
    "Role": "Teaches one module of the curriculum to a learner who writes the code themselves.",
    "Triggers": (
        '- "teach me P3"\n'
        '- "explain <concept>"\n'
        '- "I am stuck on <task>"'
    ),
    "Hard Rules": (
        "1. The learner writes the code; the agent never does.\n"
        "2. After two requests for an implementation, give a worked trace instead of code."
    ),
    "Workflow": (
        "1. Read the module note.\n"
        "2. Teach one concept.\n"
        "3. Ask one diagnostic question."
    ),
    "Output Contract": "Returns the sections Concept, Your turn and Check, in that order.",
    "Refusals": "- Refuses to write the implementation the learner is asked to write.",
}


def agent_text(
    name: str,
    *,
    description: str | None = DEFAULT_DESCRIPTION,
    order: tuple[str, ...] = SECTION_ORDER,
    overrides: dict[str, str] | None = None,
    extra_frontmatter: str = "",
) -> str:
    """Render a syntactically valid agent file.

    Returns the file text. Every argument moves exactly one part of the contract, so a
    test can break one rule at a time. The cost is a string join.
    """
    bodies = dict(SECTION_BODIES)
    if overrides:
        bodies.update(overrides)

    lines: list[str] = ["---", f"name: {name}"]
    if description is not None:
        lines.append(f"description: {description}")
    if extra_frontmatter:
        lines.append(extra_frontmatter)
    lines.extend(["---", "", f"# {name}", ""])

    for section in order:
        lines.append(f"## {section}")
        lines.append("")
        body = bodies.get(section, "")
        if body:
            lines.append(body)
            lines.append("")

    return "\n".join(lines) + "\n"


@pytest.fixture
def agent_repo(tmp_path: Path) -> Path:
    """Build a fake repository that holds a valid agent pack.

    Returns the repository root. The cost is writing seven small files.
    """
    root = tmp_path / "repo"
    agents = root / "agents"
    agents.mkdir(parents=True)
    (agents / "README.md").write_text("# Agent pack\n\nSix agents.\n", encoding="utf-8")
    for name in AGENT_NAMES:
        (agents / f"{name}.md").write_text(agent_text(name), encoding="utf-8")
    return root


def codes(issues: list) -> list[str]:
    """Return the issue codes of a validator result, in order."""
    return [issue.code for issue in issues]


def write_agent(root: Path, name: str, text: str) -> Path:
    """Write one agent file into the fake repository and return its path."""
    path = root / "agents" / f"{name}.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_agent_pack_has_no_issues(agent_repo: Path) -> None:
    """A complete, well-formed pack validates with no issues at all."""
    assert validate(agent_repo) == []


def test_missing_section_is_reported_agt001(agent_repo: Path) -> None:
    """A dropped required section is reported as AGT001 and nothing else."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text(
            "polymath-tutor",
            order=("Role", "Hard Rules", "Workflow", "Output Contract", "Refusals"),
        ),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT001"]
    assert "Triggers" in issues[0].message


def test_missing_frontmatter_key_is_reported_agt002(agent_repo: Path) -> None:
    """Frontmatter without a description is reported as AGT002."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text("polymath-tutor", description=None),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT002"]
    assert "description" in issues[0].message


def test_extra_frontmatter_key_is_reported_agt003(agent_repo: Path) -> None:
    """A third frontmatter key is reported as AGT003."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text("polymath-tutor", extra_frontmatter="model: test-model"),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT003"]
    assert "model" in issues[0].message


def test_section_order_is_reported_agt004(agent_repo: Path) -> None:
    """Sections out of the required order are reported as AGT004."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text(
            "polymath-tutor",
            order=("Role", "Workflow", "Triggers", "Hard Rules", "Output Contract", "Refusals"),
        ),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT004"]


def test_duplicated_section_is_reported_agt004(agent_repo: Path) -> None:
    """A section that appears twice is reported as AGT004."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text(
            "polymath-tutor",
            order=(
                "Role",
                "Triggers",
                "Triggers",
                "Hard Rules",
                "Workflow",
                "Output Contract",
                "Refusals",
            ),
        ),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT004"]
    assert "Triggers" in issues[0].message


def test_name_mismatch_is_reported_agt005(agent_repo: Path) -> None:
    """A frontmatter name that differs from the filename stem is reported as AGT005."""
    write_agent(agent_repo, "polymath-tutor", agent_text("some-other-agent"))
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT005"]
    assert "polymath-tutor" in issues[0].message


def test_short_description_is_reported_agt006(agent_repo: Path) -> None:
    """A description under 40 characters is reported as AGT006."""
    write_agent(agent_repo, "polymath-tutor", agent_text("polymath-tutor", description="Short."))
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT006"]


def test_empty_agent_file_is_reported_agt007(agent_repo: Path) -> None:
    """An empty agent file is reported as AGT007 and stops there."""
    write_agent(agent_repo, "polymath-tutor", "")
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT007"]


def test_empty_section_is_reported_agt008(agent_repo: Path) -> None:
    """A heading with nothing under it is reported as AGT008."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        agent_text("polymath-tutor", overrides={"Triggers": ""}),
    )
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT008"]
    assert "Triggers" in issues[0].message


def test_missing_readme_is_reported_agt001(agent_repo: Path) -> None:
    """A missing agents/README.md is reported as AGT001 against that path."""
    (agent_repo / "agents" / "README.md").unlink()
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT001"]
    assert issues[0].path == "agents/README.md"


def test_missing_agent_file_is_reported_agt001(agent_repo: Path) -> None:
    """A missing required agent file is reported as AGT001 against that path."""
    (agent_repo / "agents" / "polymath-reviewer.md").unlink()
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT001"]
    assert issues[0].path == "agents/polymath-reviewer.md"


def test_malformed_frontmatter_is_reported_not_raised(agent_repo: Path) -> None:
    """Unparseable YAML is reported as AGT002 instead of raising."""
    write_agent(
        agent_repo,
        "polymath-tutor",
        "---\nname: [unclosed\n---\n\n# Tutor\n\n## Role\nSomething.\n",
    )
    issues = validate(agent_repo)
    assert "AGT002" in codes(issues)


def test_unreadable_file_is_reported_not_raised(agent_repo: Path) -> None:
    """A file that is not UTF-8 text is reported as AGT007 instead of raising."""
    (agent_repo / "agents" / "polymath-tutor.md").write_bytes(b"\xff\xfe\x00\x01binary")
    issues = validate(agent_repo)
    assert codes(issues) == ["AGT007"]


def test_issue_paths_are_repository_relative(agent_repo: Path) -> None:
    """Issue paths are repository-relative POSIX strings."""
    write_agent(agent_repo, "polymath-tutor", agent_text("wrong-name"))
    issues = validate(agent_repo)
    assert issues[0].path == "agents/polymath-tutor.md"
