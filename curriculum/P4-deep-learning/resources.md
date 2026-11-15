# Deep Learning resources

## Must read

- *The Deep Learning Book*, Goodfellow, Bengio and Courville - the free online version.
  Read chapter 5 (machine learning basics), chapter 7 (regularisation) and the
  optimisation section of chapter 6. The rest is for later modules.
  http://www.deeplearningbook.org/
- "Understanding the difficulty of training deep feedforward neural networks",
  Glorot and Bengio - a short paper that explains why initialisation matters, and it is
  the one piece of theory that changes what you write.
  https://arxiv.org/abs/1212.0121
- "Layer Normalization", Ba, Kiros and Hinton - the normalisation you will actually use
  in transformers.
  https://arxiv.org/abs/1607.06450
- The PyTorch tutorials - the ones on datasets and dataloaders, on saving and loading,
  and on transfer learning cover the mechanics this module needs.
  https://pytorch.org/tutorials/

## Watch

- The Practical Deep Learning for Coders course, fast.ai - watch the first lessons, then
  go back to your own loop. It teaches the top-down style; this module teaches the
  bottom-up one.
  https://course.fast.ai/
- "The spelled-out intro to neural networks", Karpathy - the build-up of forward and
  backward passes, one line at a time.
  https://github.com/karpathy/nn-zero-to-hero
- "Let's build GPT: from scratch, in code, spelled out" - Karpathy's video series. Watch
  it in P5, not now; the module order exists for a reason.

## Skip

- Every paper on a new attention variant - the module is about control, not architecture
  search.
- Mixed-precision and distributed training - both are throughput work, and neither is
  what this module is for.
- Compilation graphs, CUDA kernels and custom operators - one GPU-less training loop
  teaches more per hour.
