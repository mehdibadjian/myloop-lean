Feature: Skill Hygiene and Open Standards Compliance
  As a maintainer of myloop-lean
  I want all skills to conform to Antigravity and open agent standards
  So that skills run cleanly on Gemini, DeepSeek, and Qwen without legacy engine dependencies

  Scenario: All skills have valid YAML frontmatter
    Given the consolidated skills directory
    When I inspect each skill definition
    Then every skill should have valid YAML frontmatter with "name" and "description"

  Scenario: Zero legacy engine references in skills
    Given the consolidated skills directory
    When I scan all skill files
    Then no skill should reference "engine-rust", "render-skill", or "customize.toml"

  Scenario: Native rules are properly structured
    Given the rules directory ".agents/rules"
    When I inspect the rule files
    Then "tdd-discipline.md" and "architecture-rules.md" should exist and define non-negotiable invariants
