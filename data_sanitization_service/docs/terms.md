# Terminology

| Term | Description |
|---|---|
| column scoring | Assign a score to each quasi-identifying attribute to choose the current best target of the Mondrian cut |
| data sanitization | Irreversible transformation of data to provide privacy guarantees |
| generalization | Transformation of the attribute values to achieve k-anonymity and/or l-diversity |
| identifying attribute | Attribute that identifies the individual data subject |
| information loss | Estimation of the utility loss of the sanitized data for statistical analyses by end users (lower is better) |
| k-anonymity | Dataset property where every set of rows with identical quasi-identifiers has at least *k* rows |
| l-diversity | Dataset property where, for every set of rows with identical quasi-identifiers, there are at least *l* distinct values for each sensitive attribute |
| mondrian | Efficient and effective greedy algorithm for achieving k-anonymity and/or l-diversity |
| partition | A split of the data to distribute the work across the cluster |
| quantiles | Values splitting sorted data distributions into equal parts |
| quasi-identifying attribute | Attribute that together with other attributes can identify the individual data subject |
| repartitioning | Redistribution of the data across a specified number of partitions |
| sampling | Selection of a portion of the dataset to limit CPU and memory consumption while progressing with the sanitization job |
| sensitive attribute | Attribute that should not be linkable to an individual subject |
| shuffling | Exchange of data between nodes to be able to perform a task |