
# Changing Agricultural Landscape as a Result of Changing Dietary Preferences


# Abstract
The goal of our project is to analyze if and how the agricultural landscape has changed as a result of changing dietary preferences. For our analysis, we will be using a subset of the UN's Global Food & Agriculture Statistics dataset. This dataset contains a variety of categories for many countries, including partitioning of land among different uses, raising of livestock, and specific crop production levels. In the past few years, an increasing number of people have decided to restrict their diet to vegetarian and vegan foods, in part due to increasing awareness of climate change. Global markets have simultaneously had to adapt to this change. We wish to examine this adaptation and its potential consequences in more detail, as well as potentially try to theorize what changes may take place in the future.

# Research questions
* How is land currently partitioned among resources devoted to meat, non-meat animal products, other food products, and non-food vegetation? What are the variations among countries/regions?
* Is there a better way (to help with data analysis) to separate types of agricultural land use into distinct categories?
* Using these categories, how has land use evolved over time? Are there any trends in land use which might reflect changes in human consumption preferences or technological developments?
* Deciding to adjust one's diet is somewhat of a privilege for citizens of more modernized countries; can we see dietary trends reflected in agricultural differences between more modern versus third world nations?
* How might the changing trends in land use impact carbon emissions? Is it feasible to think that changing dietary preferences might have an impact on the climate crisis?

# Dataset

We will primarily use the FAO (Food and Agriculture Organisation of the United Nations) statistics dataset to look at aspects such as land use (agricultural land, permanent crops, pasture, etc.), crop productions and primary livestock (e.g. meat, milk, eggs, etc.). 

In addition, the ‘Food Supply - Livestock and Fish Primary Equivalent’ subset of the FAO statistics contains global data about the food supply quantity (e.g. kg/capita/yr) which could be used to observe the evolution of meat and animal product consumption vs. consumption of plant-based products.

Within the FAO stat dataset, there are also annual population statistics that will permit the normalization of some of the data in terms of population. 

Eventually, we would also like to find statistics on self-declared vegetarian/vegan numbers, to be able to investigate how these figures correspond to the observed agricultural data.

The dataset is available in CSV format, therefore it can easily be imported into Python using the `read_csv` function. One issue is that the entire dataset is immense, and provides a lot of unnecessary and irrelevant data, so we need to select which subsets we would like to work with and download these specifically. The data is relatively uniform, and a list of definitions and standards, as well as metadata for each subset, is available on the FAO website. This will help to understand the data and formats provided. 

# A list of internal milestones up until project milestone 2
| No. | Milestone | Deadline |
|---|---|---|
| 1 | Collect the data: decide on what subsets of data we want to work with, analyze the sources | Oct 31 |
| 2 | Look at the collected data to narrow down the questions (more specific statistics, regions, population, etc.) that we want to answer with this project | Nov 5 |
| 3 | Clean the data, make decisions about how to handle NaN values | Nov 10 |
| 4 | If desired, find an additional dataset about vegetarian/vegan rates and trends in the population | Nov 10 |
| 5 | Descriptive analysis of the data, including additional cleaning of the data, to understand what other or more specific questions we could be answering | Nov 20 |
| 6 | Prepare the notebook for submission | Nov 25 |

# Questions for TAs
* We don't want to over-complicate our project, but it might be interesting to pull in another dataset. Do you think using data about trends in the number of vegetarians and vegans over time would be a helpful addition to our project? The downside is that relating this to agricultural data would merely be correlational and not prove any causal connections.
