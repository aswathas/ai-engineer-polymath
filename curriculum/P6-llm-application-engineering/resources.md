# LLM Application Engineering resources

## Must read

- *AI Engineering*, Chip Huyen - the chapters on prompting, structured output, tool use
  and guardrails are the working reference for this module.
  https://aiengineering.chiphuyen.com/
- "ReAct: Synergizing Reasoning and Acting in Language Models", Yao et al. - the
  reasoning-and-acting loop that the tool interface is built on.
  https://arxiv.org/abs/2005.11401
- The JSON Schema specification - you will write the schema your response must satisfy,
  so read the parts on validation and on the difference between what is required and what
  is merely typed.
  https://json-schema.org/
- Simon Willison's writing on prompt injection - the clearest available account of why
  injection is an architectural problem and not a prompt-wording problem.
  https://simonwillison.net/tags/prompt-injection/

## Watch

- "Building Effective Agents", Anthropic - a short talk that distinguishes a workflow
  from an agent, and shows how much machinery each one needs.
- The OWASP Top 10 for Large Language Applications - read the injection and the
  excessive-agency entries; they are the two that will be tested in this module.
- The Guardrails documentation - useful for the mechanics of validating model output
  against a schema.
  https://www.guardrailsai.com/

## Skip

- Fine-tuning and LoRA - the module is about the model you did not train, and P4 already
  covered the training loop.
- Multi-agent frameworks and agent orchestration frameworks - one service with two tools
  teaches the same lessons with less to install.
- Vendor-specific SDK feature tours - your service must work against a mock provider,
  and a feature tour is where that requirement goes to die.
