
# Changing Agricultural Landscape as a Result of Changing Dietary Preferences


# Abstract
The goal of our project is to analyze if and how the agricultural landscape has changed or will change as a result of changing dietary preferences of populations. For our analysis we will be using a subset UN's Global Food & Agriculture Statistics dataset. In the past decade or so, an increasing number of people have decided to restrict their diet to vegetarian and vegan foods, partially due to increasing awareness of climate change. Global markets have simultaneously had to adapt to this change.

**A 150 word description of the project idea, goals, dataset used. What story you would like to tell and why? What's the motivation behind your project?**

# Research questions
* How is land currently partitioned among resources devoted to meat, non-meat animal products, other food products, and non-food vegetation? What are the variations among countries/regions?
* Is there a better way (to help with data analysis) to separate types of agricultural land use into distinct categories?
* Using these categories, how has land use evolved over time? Are there any trends in land use which might reflect changes in human consumption preferences, or technological developments?
* How might the changing trends in land use impact carbon emissions? Is it feasible to think that changing dietary preferences might have an impact on the climate crisis?

# Dataset
**List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.**

We will primarily use the FAO (Food and Agriculture Organisation of the United Nations) statistics dataset to look at aspects such as land use (agricultural land, permanent crops, pasture etc.), crop productions and primary livestock (e.g. meat, milk, eggs etc.). 

In addition, the ‘Food Supply - Livestock and Fish Primary Equivalent’ subset of the FAO statistics contains global data about the food supply quantity (e.g. kg/capita/yr) which could be used to observe the evolution of meat and animal product consumption vs. consumption of plant based products.

Within the FAO stat dataset, there are also annual population statistics which will permit normalisation of some of the data in terms of population. 
Eventually, we would also like to find statistics on self-declared vegetarian/vegan numbers, to be able to investigate how these figures correspond to the observed agricultural data.

The dataset is available in csv format, therefore can be easily imported into python using the ‘read_csv’ function. One issue is that the entire dataset is immense, and provides a lot of unnecessary and irrelevant data, so we need to select which subsets we would like to work with and download these specifically. The data is relatively uniform, and a list of definitions and standards, as well as metadata for each subset is available on the FAO website. This will help to understand the data and formats provided. 

# A list of internal milestones up until project milestone 2
| No. | Milestone | Deadline |
| 1 | Collect the data: decide on what subsets of data we want to work with, analyze the sources | Oct 31 |
| 2 | Look at the collected data to narrow down the questions (more specific statistics, regions, population, etc.) that we want to answer with this project | Nov 5 |
| 3 | Clean the data (as much as we can at this level) | Nov 10 |
| 4 | Descriptive analysis of the data, including additional cleaning of the data, to understand what other or more specific questions we could be answering | Nov 20 |
| 5 | Prepare the notebook for submission | Nov 25 |

# Questions for TAa
Add here some questions you have for us, in general or project-specific.



### Notes below should be removed before submission
Data description: [http://www.fao.org/faostat/en/#data/QC/metadata](http://www.fao.org/faostat/en/#data/QC/metadata)

### Ideas
* Use a weather patterns data set and correlating it with food crop productivity in an effort to predict future food shortages based on current weather trends. [Potential weather dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels-monthly-means?tab=overview)
* Evaluate the distribution of crops across continents, perhaps explaining why some countries are richer/healthier/something else related to their crop production.
* Analyze changes in forested land in recent years. In some countries, there has been a big push recently to re-forest dairy and sheep + beef farms to offset carbon. We would be intrigued to see how this has evolved, the trend in other countries trying to lower CO2 emissions, and also the contrast with the many countries where deforestation is still an issue.
* Analyze increases in food production to see if we will be able to meet predicted global demand in the next few decades. Possibly also combining a data set of how much meat/fish/dairy people consume (e.g. look at those trends in the US over time, and extrapolate those trends to other emerging countries probably having them over the next few decades)
* Analyze the vegan trend and meat consumption. For example, we could analyze how interest in vegan lifestyle and decreasing meat consumption has evolved. We could check how this has evolved in parallel to increasing interest in global warming and the impact of meat consumption, for example by using the Wikipedia dataset. 
* Compare increasing interest in vegan lifestyle and see if this is reflected in cooking recipes or grocery shopping. Another idea is to compare it to development in agriculture. We could analyze how demand for vegan food in wealthier countries can put some pressure on agriculture in poorer countries. Thereby underscoring the fact that global market structures and national relations need to similarly and simultaneously undergo a transformation for that change in lifestyle to be sustainable.
