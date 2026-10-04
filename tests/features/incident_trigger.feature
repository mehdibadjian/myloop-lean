Feature: Autonomous Incident Maintenance Loop
  As an autonomous system maintainer
  I want an incident trigger command to scaffold intent.md and register the task
  So that bugs and error spikes immediately re-enter the development loop

  Scenario: Creating an incident scaffolds intent.md and registers in sprint ledger
    Given a clean sprint status ledger
    When I trigger an incident with description "Checkout API returns 500 on valid token"
    Then an incident intent.md file should be created under docs/stories/incidents/
    And the incident should be registered in the sprint ledger as "ready-for-dev"
