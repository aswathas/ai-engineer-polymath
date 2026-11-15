# Data and Features resources

## Must read

- *Hidden Technical Debt in Machine Learning Systems*, Sculley et al. - the sections on
  entanglement, data dependencies and feedback loops describe exactly the failures this
  module prevents.
  https://arxiv.org/abs/1610.02024
- *Designing Machine Learning Systems*, Chip Huyen - the chapters on data pipelines and
  on training-serving skew are the practical version of the same warnings.
  https://chiphuyen.com/book/
- The scikit-learn user guide on pipelines and the API on column transformers - this is
  the tool that makes "fit on train only" a one-liner instead of a discipline.
  https://scikit-learn.org/stable/user_guide.html
- The pandas user guide on merging and reshaping - most broken datasets are a join that
  multiplied the rows.

## Watch

- "Rules of Machine Learning", Google - the rules on pipeline complexity, on the smell of
  a feature, and on starting with a simple model are the operating manual for this
  module.
  https://developers.google.com/machine-learning/guides/rules-of-ml
- "Data Cascades in High-Stakes AI", Nadeem et al. (NeurIPS 2021) - a short paper on how
  bad upstream data becomes a bad model, and why the fix is upstream.
- The Talk Like a Graph podcast episodes on retrieval and graph data - useful later, in
  P6, but the episode on entity resolution is worth one listen now.

## Skip

- Manual feature engineering encyclopaedias - the module teaches the pipeline and the
  audit, not a catalogue of tricks.
- Big-data tooling: Spark, Dask, Airflow - a single machine and a single script teach the
  same lesson here.
- Datasets with more than 100,000 rows - you will not be able to look at them, and
  looking at your data is half the module.
