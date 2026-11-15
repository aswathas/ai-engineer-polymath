---
name: curriculum-graph
description: Use when the prerequisite order of the curriculum is needed, or when a check is required for cycles in the module graph.
---

# Curriculum Graph

## When to use

Use this skill when a question is about the order the modules run in, the prerequisites
of one module, or whether the curriculum graph contains a cycle.

## Inputs

- The repository root, defaulting to the current directory.
- The module file `curriculum/curriculum.yaml`.

## Procedure

1. Run the shipped script from the repository root:
   `python skills/curriculum-graph/scripts/graph.py --repo . --order`
2. Read the printed order. It is a topological order of the prerequisite graph.
3. To inspect one module, run
   `python skills/curriculum-graph/scripts/graph.py --repo . --module P3`
   and read its direct prerequisites.
4. If the script reports a cycle, stop and fix the entry in `curriculum/curriculum.yaml`
   that creates it before teaching the affected module.
5. If the script reports that `curriculum/curriculum.yaml` is missing, the curriculum
   has not been created yet and there is no order to report.

## Outputs

- The modules in prerequisite order, one per line.
- The direct prerequisites of the requested module.
- A cycle report naming the modules that form the cycle, or a clean result.

## Verification

- `python skills/curriculum-graph/scripts/graph.py --repo . --order` exits 0 and lists
  every module exactly once.
- The script exits 1 with a clear message when `curriculum/curriculum.yaml` is missing
  or when the graph contains a cycle.
- Every module that the order lists appears in `curriculum/curriculum.yaml`.
