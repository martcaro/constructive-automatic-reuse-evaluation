# Evaluation Metric Library to evaluate Explanation Strategies & their use to check Constructive Reuse applied on explanation strategies performance

This repository contains the following:

- explanation_strategy_evaluation_metrics.py --> the evaluation metric library to evaluate explanation strategies. This code contains the implementation of the following metrics:
*Timeliness*. It returns the explanation strategy computational complexity, i.e., the highest computational complexity of all the explainers within the explanation strategy in a normalised format ([0,1]).
*Popularity*. It returns the mean popularity of all the explainers in the strategy.
*Completeness*. It returns a score that decides the level of the strategy uniformity in terms of explanations provided, and it returns a value between 0 (totally diverse) and 1 (totally complete).
*Diversity*. This metric is symmetric with completeness and it measures the variability of the explanations shown by the strategy. Again, this metric returns a value between 0 (totally complete in this case) and 1 (totally diverse).
*Serendipity*. Serendipity is a metric that measures whether the explanation strategy has a surprising element that users may like.
*Granularity*. This measure measures the level of detail of the strategy considering its types of nodes and connections: the more the number of connections are and the more the number of nodes are, the higher the granularity score is. This measure requires the explanation strategy to have graph format (list of nodes and adjacency list).

- All the files used to evaluate the automatic constructive reuse implemented for the iSee project (information available about the project on its [website](https://isee4xai.com/) and [GitHub](https://github.com/isee4xai))
*Trees_Random folder* -> contains random Behaviour Trees (randomly generated as solutions for different iSee use cases) in json format. These BTs are proper structured solutions, but not applicable for those use cases. The automatic constructive reuse was applied to make those random BTs applicable in three ways: replacing only non-applicable explainers, replacing the whole tree by another applicable tree, replacing first only non-applicable explainers and later the whole tree by another applicable tree. The resulting BTs from those three types os reuse are in this folder as well (in json format).
*constructive_automatic_reuse_evaluation.ipynb* --> notebook where we apply the evaluation metric library to evaluate the previous BTs (random ones and the results from the reuse).
*local_explainer_catalog.csv* --> the iSee explainer library catalog and their properties according to iSeeOnto (iSee ontology). This is needed to try our evaluation metrics within the previous notebook.
*results.csv* --> the results obtained with our evaluation metrics for the BTs mentioned previously.
