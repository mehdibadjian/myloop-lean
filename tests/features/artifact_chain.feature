Feature: Three-Stage Artifact Chain
  As a software engineer pair programming with an AI agent
  I want each story to follow an intent.md -> spec.md -> plan.md progression
  So that every phase is committed to Git with clear provenance before code is written

  Scenario: Validating the artifact chain directory and schema
    Given a story directory with intent.md, spec.md, and plan.md
    When the artifact chain validator inspects the directory
    Then it should confirm all three stages exist and are non-empty
