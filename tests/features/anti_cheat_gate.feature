Feature: Anti-Cheat Test Protection Gate
  As an autonomous engineering lead
  I want the verification gate to detect test tampering
  So that agents cannot delete or weaken test assertions to fake a passing build

  Scenario: Clean test execution with anti-cheat verification
    Given a working directory with valid tests and zero deleted assertions
    When I run verification with the anti-cheat flag
    Then verification should pass

  Scenario: Detecting deleted or weakened test assertions
    Given a diff containing deleted assertion statements in test files
    When the anti-cheat analyzer inspects the diff
    Then it should flag test tampering and reject verification
