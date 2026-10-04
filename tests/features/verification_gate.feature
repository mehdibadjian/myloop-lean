Feature: Pre-Completion Verification Gate
  As an autonomous orchestrator
  I want to verify that tests pass and git changes are cleanly committed
  So that untested or half-finished code is never marked done

  Scenario: Verification succeeds when test command exits 0 and commit exists
    Given a working directory with a passing test suite
    And a git commit recorded for the current story
    When I run the verification gate
    Then verification should pass

  Scenario: Verification fails when test command fails
    Given a working directory with a failing test suite
    When I run the verification gate
    Then verification should fail with test failure output

  Scenario: Verification warns or halts on uncommitted dirty working tree
    Given uncommitted tracked changes in the working directory
    When I run the verification gate
    Then verification should report uncommitted modifications
