Feature: Model-Agnostic Story Dispatch
  As an AI software engineering orchestrator
  I want to dispatch tasks to heterogeneous models (DeepSeek, Qwen, Gemini, OpenAI, Ollama)
  So that personas execute tasks with the best-suited model and unified context rules.

  Scenario: Compiling prompt context with persona, rules, and skill
    Given a project workspace with rules and the "build" skill
    When prompt context is compiled for persona "developer" and story "1-2-model-agnostic-dispatch"
    Then the system prompt contains "tdd-discipline"
    And the system prompt contains "Kent Beck"
    And the system prompt contains the persona instructions

  Scenario: Resolving model configurations by persona and tier
    Given the model registry
    When resolving the model for persona "reviewer" and tier "pro"
    Then the resolved provider is "deepseek"
    And the resolved model is "deepseek-reasoner"

  Scenario: Executing dispatch in dry-run mode
    Given a story directory with valid artifacts
    When dispatch is executed with "--dry-run"
    Then it outputs a valid JSON request payload
    And no network requests are attempted
