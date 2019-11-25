
# Reducing the Swiss "Foodprint": How An Individual Can Adjust Their Carbon Output


# Introduction
As is slowly becoming a widely-known fact, the meat and animal product industry is significantly more carbon-intensive than plant-based foods. The amount of CO2 produced per kg (or even kcal) of meat/animal product is much higher than the amount of CO2 for the same mass/energy equivalent of plants, e.g., fruits, vegetables, legumes. (Center for Sustainable Systems, 2018) One might think, then, that the best way to reduce one's "carbon foodprint" (carbon footprint due to food production) is to take on a vegetarian or vegan diet.

What is intriguing is that this may not be the answer in all cases. Based on where food is sourced, what time of year it is grown, and how it is produced, the carbon emissions can change drastically. A hot house tomato grown out of season can produce less carbon than pasture-fed goat meat, for example.

An important question that data can answer, then, is how an eco-friendly citizen can best adapt their diet, based on their specific living circumstances, to reduce their carbon foodprint. Here, we will perform an in-depth analysis on Switzerland, providing a consumer with the knowledge necessary to produce less carbon emissions due to their diet. This will include an analysis of carbon intensities by food type and the various types and sources of food that are imported into Switzerland. After all, since Switzerland has a fairly dense population for its small size, it imports a significant amount of its food:

"According to the Federal Agriculture Office, Switzerland’s gross self-sufficiency rate in 2015 was 59%. The degree of self-sufficiency is defined as the ratio of domestic production to total domestic consumption. With imported animal feed taken into account, the net level of self-sufficiency was 51% that year. But a closer look at the data reveals major differences across products. The country has been able to produce almost 100% of its animal foodstuffs for years, yet has managed only about 40% self-sufficiency for plant-based foods, a rate that fluctuates year on year as harvests are highly weather-dependent." (From swissinfo.ch)

Depending on where and what types of food Switzerland is importing its non-meat food products from, this raises the possibility that a Swiss citizen might have a smaller carbon foodprint by eating more meat, contradicting the typical recommendation. Would living with a vegan diet require an excessive amount of imported foods, outweighting the carbon offset of not eating meat? Or is there a large enough amount of carbon produced by the meat industry that eating a plant-based diet is still more sustainable?

This project will attempt to answer the following question:

> ### How can a Swiss consumer best adapt their diet to reduce their carbon "foodprint", based on all the factors that go into the carbon emissions of food production?

Note that we are assuming this analysis will be utilized by a Swiss consumer, and not by the government or any authoritative figure. Therefore, the utility of this analysis comes while assuming that nothing about the given situation will change (for example, Switzerland will not make a policy to start domestically producing more bananas); rather, we are looking to give an individual consumer insight into their carbon levels.

# Sub-questions
* Among Swiss consumption, how much of the various food types (e.g. bananas, beef, oats) are domestically produced versus imported?
* How far away do these imports come from? (The farther food is imported from, generally the higher the associated carbon "cost" of transporting the food to Switzerland.)
* Among the various meats and animal products, which ones are more carbon-efficient? This must include both the carbon cost of the animals themselves as well as whether feed is imported or grown domestically.
* Ultimately, using data specific to Switzerland that we gather, what is the carbon foodprint of (1) A typical Swiss diet, (2) The Swiss government-recommended diet, and (3) A diet optimized for the lowest carbon foodprint possible?

# Datasets

There are two primary sets of data which we are using to drive our analysis. 

The first is the [FAO](http://www.fao.org/faostat/en/#data) (Food and Agriculture Organisation of the United Nations) statistics dataset, which provides us with data specific to Switzerland regarding its crop and other food production. Since the latest available year for Swiss crop production is 2017, we will use 2017 data for all of our sources.

The second is [Swiss Impex](https://www.gate.ezv.admin.ch/swissimpex/index.xhtml), a site hosted by the Swiss Federal Customs Administration which gives detailed datasets of imports and exports for many food items, among other traded goods.

Note that size is not an issue with our datasets, so we will be processing all data locally (not using Spark).

There are certain mismatches between data available from FAO and Impex. In these cases, we performed an outer join of dataframes, such that any food type which is listed in one but not the other is kept, filling in 0 values for the part of the joined dataframe in which it was empty/no value was provided.

We will use very small amounts of additional data, such as [this federal report](https://www.blv.admin.ch/dam/blv/en/dokumente/lebensmittel-und-ernaehrung/ernaehrung/schweizer-ernaehrungsstrategie-2017-2024.PDF.download.PDF/Ernaehrungsstrategie_Brosch_EN.PDF) on the recommended and current actual consumption levels by food groups in Switzerland.

# Assumptions
Several assumptions had to be made to distill this massive question into a feasible project.

As mentioned above, this analysis is a consumer insight tool. We assume that no changes are made on the large scale of this data.

The most notable of all assumptions is the source of carbon intensities data. Many sources explain the impossibility of estimating the carbon intensities by crop type per country, since the amount of carbon that a crop's production causes depends on a _massive_ number of factors, and these factors vary widely even within a single country, from farm to farm. Thus, there is no data available for carbon intensities of all crops by country. To circumvent this, we will use the global average carbon intensities sourced from [this article](https://www.sciencedirect.com/science/article/pii/S0959652616303584).

Certain difficulties with the datasets were navigated by excluding or combining certain categories. For example, Impex provides data on imported (and exported) live animals for slaughter, but it is unknown whether these imported animals are already accounted for in the FAO's meat production data. It is also unknown how much of the weight of a live animal equates to meat. We therefore excluded the category of live animals, along with other similar categories such as animal offal.

Also, we have included food waste as food consumption. That is, we calculated `Swiss food consumption` as `domestic production` - `exports` + `imports`.

We are only looking at _carbon dioxide_ output. CO2 is only one of many greenhouse gases. So while this gives an informative picture, it is not all-encompassing.

Certain minor food groups, such as oils and sweets, were excluded from the analysis, since they are not necessarily "recommended" foods to consume.

Finally, animals are often fed with by-products of human food production. If a consumer were to eat fewer meat/animal products, there would potentially be additional food waste to dispose of. The impact of this waste is not incorporated in this analysis.

# Tasks to finish
* Finish loading in all datasets from FAO and Impex (e.g. nuts, fish, etc. which have been downloaded but were not yet incorporated into the mega dataframe)
* While there are no by-country datasets for carbon intensities of all foods, FAO does offer a dataset of intensities by country for a select number of animal products (meats and non-meat animal products). We will replace the global averages currently used with the data available from FAO, and leave the global averages for anything not provided by the FAO.
* We need to select (among those we have found) a dataset which details the carbon cost of each type of transport for imported foods. For example, what percentage of apples are imported by plane versus by train, and what is the carbon output per kilometer for both methods of transport?
* Continue to explore whether there is a way to incorporate seasonality data (crops grown out of season are much more carbon-intensive than in season).
* Some animals are fed with a different mixture of feed than others; for example, most of cattle feed is grown domestically, but the majority of chicken feed is imported. Try to find a way to distinguish between these categories, more accurately representing the carbon cost of each meat type.
* Is there a way to optimize a diet for carbon output while still having a varied, delicious diet? Explore more methods of data processing and perhaps machine learning for this task.

