# ADR-IA-1C-003: CI Gating Semantics

- Status: Accepted
- Date: 2026-09-20
- Scope: Repository-wide CI policy affecting IA-1C and later milestones

## Context

The repository's standing development rule requires completion gates to be tied to a specific Git HEAD and verified against the CI system.

The alternative of skipping documentation-only commits creates two different meanings for CI green on HEAD: a commit may have no CI run, even though the repository gate is phrased as though every HEAD has been verified.

Documentation is part of the governed project artifact. Even when a documentation change does not alter executable code, the repository at that commit should remain in a known healthy state.

## Decision

Choose Answer B: CI verifies repository health after every push to main, including documentation-only commits.

The current workflow will therefore not add paths-ignore for Markdown files.

The existing trigger semantics remain:

- push to main;
- pull requests.

Any future path filtering requires a separate architectural/development-process decision.

## Gate semantics

The standing rule is:

A milestone implementation or documentation batch is not complete until the resulting HEAD SHA has a directly verified CI result appropriate to the workflow configuration.

For every committed batch, reporting must identify:

1. exact HEAD SHA;
2. whether CI was triggered;
3. workflow run ID;
4. job results;
5. failures and their root causes, if any.

A documentation-only commit still receives a CI run under this policy.

This avoids treating no CI run as equivalent to CI passed.

## Rationale

The cost of running the existing backend/frontend checks on documentation-only pushes is small relative to the governance benefit.

Uniform CI semantics also reduce ambiguity between engines and preserve the project's existing completion-gate language.

## Consequences

Positive:
- Every main-branch HEAD has an explicit CI result.
- CI green on HEAD has one consistent meaning.
- Documentation changes cannot accidentally leave the repository in an unverified state.
- Future engines do not need to infer whether CI was expected for a particular commit.

Tradeoff:
- Documentation-only pushes consume CI minutes.

If CI cost becomes material, the project may revisit this ADR using observed usage/cost data rather than adopting path filtering by default.

## Non-decision

This ADR does not require CI to validate prose quality or documentation semantics. Review remains responsible for those concerns. CI establishes repository health at the committed revision.
