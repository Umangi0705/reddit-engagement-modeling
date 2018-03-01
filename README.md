# Project 3 - Project 3: Web Scraping & Classification

Michael Schillawski, February 23, 2018

General Assembly, Data Science Immersive

## Table of Contents

- [Repository Contents](#repository-contents) - Description of this repository's files
- [Data Description](#data-description) - Description of the Iowa liquor dataset
- [Project Overview](#project-overview) - Summary of the project's goals
- [Analysis Explanation](#analysis-explanation) - Explanation of project's methods and analysis
- [Project Concepts](#project-concepts) - Skills and concepts demonstrated

## Repository Contents

| FILENAME |     DESCRIPTION    |
|:-------------:|:--------------:|
|  [README](./README.md) | Project description |
| [Reddit Engagement Modeling](https://git.generalassemb.ly/mjschillawski/project-3/blob/master/Reddit%20Engagement%20Modeling.ipynb) |    Jupyter notebook with core project analysis    |
| [scrape.py](https://git.generalassemb.ly/mjschillawski/project-3/blob/master/scrape.py) | Reddit webscraper |
| [fast_scrape.py](https://git.generalassemb.ly/mjschillawski/project-3/blob/master/fast_scrape.py) | Fast (limited) Reddit webscraper |
|   [Presentation_Deck](https://docs.google.com/presentation/d/1leYDsorOnXZYO6Z4x6g6uOh5kP6r90iXnk5EQ_Pr_sU/edit?usp=sharing)    |    Results slide deck    |
| [presentation](./presentation) | Presentation images |

## Data Description

I built a webscraper to access information about the popular posts on Reddit (https://www.reddit.com/r/all) and the subreddits from which those posts were drawn. I gathered data and metadata about the posts, including title, number of comments, data score (net upvote-downvote), author, subreddit source, post time, etc.

## Project Overview

Using the data I gathered from Reddit over a week's span, my goal was to identify the characteristics of Reddit posts that had above expected engagement (number of comments) from the readers. During my initial analysis, I found that that post engagement was very flat: a post in the 75th percentile of comment quantity on r/all had received 61 comments. However, comments exploded above the 75th percentile. 

I developed a series of classifiers, including random forests, k-nearest neighbors, and logistic regression models to identify the post characteristics that contribute most to community interaction.

## Analysis Explanation

I took several approaches to modeling this problem: one where I sought to predict ±median number of comments, once where I tried to predict ±75th percentile. I also tried to predict ±90th percentile, as that's where the true inflection point of where post comments begin to accelerate approximately is. 

I settled on predicting ±75th percentile, as it seemed like a more interesting problem than ±median, that's when posts' quantities of comments start to become differentiated, even though there was a bit more predictive lift from predicting the median.

For example, if:

- predicting 50th percentile: baseline accuracy is 50% (20 comments). We expect to be right half the time. The basic model (using only subreddits) had an accuracy ~62%, while a more complex model (model 6 in the below) upped this to almost 69%. 

- predicting the 75th percentile: baseline accuracy is 75% (61 comments), but our majority class is predicting below 61 comments. These models started around 71% accuracy (just subreddits), to my complex model which nearly broke 80% (78.9%). 

- predicting 90th percentile: the true inflection point, failed to generate any predictive lift. In the basic model, accuracy was 78.5%. My complex model achieved 91.1% accuracy in the test sample. 

It is interesting to notice that just using subreddits in the 90th percentile case was by far the worst model. It suggests that in order to get better predictive lift at the margins, we need to know more about the specific content of the posts. Probably content beyond the title to improve the predictions any further.

## Project Concepts

Random forest classifiers; Term frequency-inverse document frequency vectorization; natural language processing; TF-IDF vectorization; logistic regression; k-nearest neighbors; webscraping; regex; xpath; crontab; amazon web services; cross-validation; exploratory data analysis; bagging; unbalanced classes; feature engineering.