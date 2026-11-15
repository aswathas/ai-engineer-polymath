# Evaluation resources

## Must read

- *AI Engineering*, Chip Huyen - the chapter on evals is the practical spine of this
  module: case set construction, judge design, and where the numbers come from.
  https://aiengineering.chiphuyen.com/
- "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", Zheng et al. - the paper that
  made LLM judges mainstream, and the one that measures the biases you have to control
  for: position, verbosity and self-preference.
  https://arxiv.org/abs/2305.17926
- "Your AI Product Needs Evals", Hamel Husain - a short, blunt essay on building an eval
  set before you build the product. Read it first.
  https://hamel.dev/blog/posts/evals/
- The EleutherAI evaluation harness documentation - read it for the shape of a benchmark
  runner, not to use the harness itself.
  https://github.com/EleutherAI/lm-evaluation-harness

## Watch

- "LLM-as-a-Judge", Hamel Husain - a short walkthrough of writing a rubric and the
  agreement study that goes with it.
  https://hamel.dev/blog/posts/llm-judge/
- The Inspect AI documentation - a concrete example of an eval framework that treats
  graders, transcripts and limits as first-class objects.
  https://inspect.aisi.org.uk/
- "A Survey on Evaluation of Large Language Models" - use it to find the names of the
  benchmarks you have not heard of, and to decide which of them to ignore.

## Skip

- Leaderboard culture and benchmark chasing - public benchmarks do not measure your
  product, and the moment they do, they measure your data.
- Reward models and RLHF internals - the module is about judging outputs against a
  written rubric, not about training a judge.
- Every metric library at once - one good metric with a slice breakdown beats a dashboard
  of forty.
