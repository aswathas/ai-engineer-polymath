# Math for ML resources

## Must read

- *Mathematics for Machine Learning*, Marc Deisenroth, Aad van Baalens and Carl
  Rasmussen - chapters 2 to 6 cover exactly the ground of this module, and the book is
  free to read.
  https://mml-book.github.io/
- *Convex Optimization*, Boyd and Vandenberghe - do not read it cover to cover. Read the
  intuition chapter and the gradient descent chapter, then come back to it in P4.
  https://web.stanford.edu/~boyd/cvxbook/
- The NumPy broadcasting and indexing documentation - most "the maths is wrong" bugs in
  the first hour are shape bugs.
  https://numpy.org/doc/stable/user/basics.indexing.html

## Watch

- *Essence of Calculus* and *Essence of Linear Algebra*, 3Blue1Brown - visual intuition
  for derivatives, gradients and vector spaces. Watch them before the reading, not after.
- *Gradient descent, how neural networks learn*, 3Blue1Brown - a short treatment of the
  update rule and the loss surface that maps directly onto the gate questions.
- *The spelled-out intro to neural networks*, Andrej Karpathy - a patient build-up of
  forward and backward passes; useful here because it slows down the part that is usually
  skipped.
  https://github.com/karpathy/nn-zero-to-hero

## Skip

- Measure theory, functional analysis and rigorous probability axioms - none of it is
  used in this series.
- Symbolic differentiation tools such as SymPy for the final implementation - derive by
  hand once, then check numerically forever.
- The convex analysis chapters of Boyd and Vandenberghe - read them when P4 asks for
  regularisation theory, not now.
