# LLM Mechanics resources

## Must read

- "Attention Is All You Need", Vaswani et al. - read it once with the module note open,
  focusing on the attention block and the scaling factor, not the results tables.
  https://arxiv.org/abs/1706.03762
- "Neural Machine Translation of Rare Words with Subword Units", Sennrich, Haddow and
  Birch - the original BPE paper; short, and it explains the merge table you are about to
  build.
  https://arxiv.org/abs/1508.07909
- The nanoGPT repository, Karpathy - a small, readable implementation of tokenisation,
  the model and the sampling code, in the order this module teaches.
  https://github.com/karpathy/nanoGPT
- The Hugging Face tokenizers documentation - use it to compare your implementation
  against a production one on the same text.
  https://huggingface.co/docs/tokenizers/

## Watch

- "The Illustrated Transformer", Jay Alammar - the best explanation of attention that
  exists. Read it before the paper.
  https://jalammar.github.io/illustrated-transformer/
- "Let's build GPT: from scratch, in code, spelled out", Karpathy - the video series that
  turns the module into an afternoon. The parts on attention and sampling are the ones
  you need.
- "The spelled-out intro to neural networks", Karpathy - the slow build-up of the
  background that the GPT video assumes.

## Skip

- Papers on sparse, linear or state-space alternatives to attention - the module is about
  the mechanism you will actually meet.
- KV-cache and inference-optimisation papers - the cache appears in P6 as a cost line,
  not as an implementation task.
- Anything about fine-tuning or instruction tuning - P6 and P7 are about the model you
  did not train.
