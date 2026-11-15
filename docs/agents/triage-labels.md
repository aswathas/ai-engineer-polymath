# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the
label strings used in this repository's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning |
| -------------------------- | -------------------- | ------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue |
| `needs-info`               | `needs-info`         | Waiting on the learner for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation |
| `wontfix`                  | `wontfix`            | Will not be actioned |

When a skill mentions a role (for example "apply the AFK-ready triage label"), use the
corresponding label string from this table.

**One rule beats the label.** An issue labelled `ready-for-agent` that asks the agent to write
the learner's implementation is still refused. The labels route work; the rule in
[AGENTS.md](../../AGENTS.md) decides what the work may be.
