Feature: Sprint Status Ledger Management
  As an AI developer agent or orchestrator
  I want to track and advance story statuses in sprint-status.yaml
  So that autonomous iteration is deterministic and auditable

  Scenario: Querying the next ready-for-dev story
    Given a sprint ledger with stories:
      | story_key | status        | tier     |
      | 1-1-auth  | done          | standard |
      | 1-2-user  | ready-for-dev | pro      |
      | 1-3-post  | backlog       | flash    |
    When I query the next actionable story
    Then the result should return story "1-2-user" with tier "pro"

  Scenario: Validating status transition order
    Given a sprint ledger with story "1-2-user" in status "ready-for-dev"
    When I update story "1-2-user" to status "in-progress"
    Then the update should succeed
    And the story "1-2-user" should have status "in-progress"

  Scenario: Rejecting invalid status regressions or jumps
    Given a sprint ledger with story "1-3-post" in status "backlog"
    When I attempt to update story "1-3-post" to status "done"
    Then the update should be rejected with an invalid transition error

  Scenario: Updating story while preserving ledger structure
    Given a sprint ledger with comments and multiple epics
    When I update story "1-2-user" to status "review"
    Then the updated file should preserve original comments and structure
