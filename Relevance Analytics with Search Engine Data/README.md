# Relevance Analytics with Search Engine Data (Stanford STATS202 class project 2018)

In this project, I built a model to make relevance prediction for search engine data (only 10 attributes provided) and achieve good results.

The data and codes are provided.

## Objective

The goal of this class project is to give you experience in real life data mining.  By the end of the project, you will have learned how to identify and interpret types of different attributes in a dataset, visualize each attribute individually, visualize relationships between attributes of different types, understand how those relationships could affect your model, and finally build a binary classification model.  

## Data

The goal of a search engine is to return relevant documents for search queries that users enter.  Search engines typically use hundreds of signals to determine the relevance of a document and then return a list of documents in order of relevance.

You will be provided a training data set which includes 10 attributes and 80,046 observations from search engine query and  url data.  The dataset contains 10 different signals that could be used to help predict whether the url is relevant for the query.  Additionally, a test data set is provided which contains 30,001 observations.  Your goal is to make relevance predictions for each row (urls for a query) in the test data set.   Please download the data from the links provided at the bottom of the page.   

Your job is to create a text file containing one line per example in the test set.  On each line, give your prediction for the relevance (1 for relevant, 0 for not relevant) of that row in the test set.

## Result

The final test error of my model is 32.8%. It is a good preformence due to the limited data. 
