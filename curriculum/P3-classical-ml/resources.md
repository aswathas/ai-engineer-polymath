# Classical ML resources

## Must read

- *An Introduction to Statistical Learning*, James, Witten, Hastie and Tibshirani - the
  chapters on model assessment, regularisation and classification cover this module. The
  free PDF is the same book as the printed one.
  https://www.statlearning.com/
- The scikit-learn user guide on model selection, calibration and evaluation - the
  cross-validation and calibration sections are the ones to have open while you work.
  https://scikit-learn.org/stable/user_guide.html
- *The Elements of Statistical Learning*, Hastie, Tibshirani and Friedman - use it as the
  reference when you want to know why a regulariser behaves the way it does, not as
  reading.
  https://hastie.su.domains/ElemStatLearn/
- "On Calibration of Modern Neural Networks", Guo et al. - the temperature-scaling method
  the calibration step in this module is based on.
  https://arxiv.org/abs/1706.04599

## Watch

- "Rules of Machine Learning", Google - the rules on the first model, on feature
  engineering, on measuring training-serving skew, and on watching for silent failures.
  https://developers.google.com/machine-learning/guides/rules-of-ml
- "A Unified Approach to Interpreting Model Predictions", Ribeiro, Singh and Guestrin - the
  LIME paper, for the habit of asking why the model said that.
  https://arxiv.org/abs/1610.01350
- StatQuest with Josh Starmer - one short episode on calibration and one on ROC versus
  PR curves. Short enough to finish in a coffee break.

## Skip

- Ensembles beyond gradient boosting - one strong learner plus one baseline is the whole
  comparison this module needs.
- Symbolic regression, genetic programming and other auto-ML curiosities - they hide the
  error analysis the module is actually about.
- Counting-sort implementations of AUC by hand - you already have libraries for the
  arithmetic; spend the time on the threshold instead.
