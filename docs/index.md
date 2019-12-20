---
layout: page
title: Reducing the Swiss "Foodprint"
subtitle: How An Individual Can Adjust Their Carbon Output
image: /img/flag.gif
bigimg: /img/path.jpg
---

## Introduction
As is slowly becoming a widely-known fact, the meat and animal product industry is significantly more carbon-intensive than plant-based foods. The amount of CO2 produced per kg (or even kcal) of meat/animal product is much higher than the amount of CO2 for the same mass/energy equivalent of plants, e.g., fruits, vegetables, legumes (Center for Sustainable Systems, 2018). One might think, then, that the best way to reduce one's "carbon foodprint" (carbon footprint due to food production) is to take on a vegetarian or vegan diet.

What is intriguing is that this may not be the answer in all cases. Based on where food is sourced, what time of year it is grown, and how it is produced, the carbon emissions can change drastically. A hot house tomato grown out of season can produce less carbon than pasture-fed goat meat, for example.

An important question that data can answer, then, is how an eco-friendly citizen can best adapt their diet, based on their specific living circumstances, to reduce their carbon foodprint. Here, we will perform an in-depth analysis on Switzerland, examining how a consumer's dietary choices affect their individual carbon emissions. This will include an analysis of carbon intensities by food type and the various types and sources of food that are imported into Switzerland. After all, since Switzerland has a fairly dense population for its small size, it imports a significant amount of its food; as of 2015, Switzerland's food self-sufficiency rate, [defined by the FAO](http://www.fao.org/3/a-i5222e.pdf) as "the extent to which a country can satisfy its food needs from its own domestic production", was [approximately 59%](https://www.swissinfo.ch/eng/fact-check_does-switzerland-produce-half-of-all-the-food-it-needs-/44380058). A large amount of the foods imported are plant-based.

Depending on what types of food Switzerland is importing and from where, this raises the possibility that a Swiss citizen might have a smaller carbon foodprint by eating more meat, contradicting the typical recommendation. Would living with a vegan diet require an excessive amount of imported foods, outweighting the carbon offset of not eating meat? Or is there a large enough amount of carbon produced by the meat industry that eating a plant-based diet is still more sustainable?

This project will attempt to answer the following question:

> ### How can a Swiss consumer best adapt their diet to reduce their carbon "foodprint", based on several factors that go into the carbon emissions of food production?

Note that we are assuming this analysis will be utilized by a Swiss consumer, and not by the government or any authoritative figure. Therefore, the utility of this analysis comes while assuming that nothing about the given situation will change (for example, Switzerland will not make a policy to start domestically producing more bananas); rather, we are looking to give an individual consumer insight into their carbon levels.

Some of the sub-questions we will attempt to answer in this analysis include:

* Among Swiss consumption, how much of the various food types (e.g. bananas, beef, oats) are domestically produced versus imported?
* How far away do these imports come from? (The farther food is imported from, generally the higher the associated carbon "cost" of transporting the food to Switzerland.)
* Among the various meats and animal products, which ones are more carbon-efficient? How do these compare to the carbon efficiency of plant-based foods?

Data for this project was sourced from the [Food and Agriculture Organization of the United Nations (FAO)](http://www.fao.org/faostat/en/#data) and [Swiss Impex](https://www.gate.ezv.admin.ch/swissimpex/index.xhtml). More details on these datasets can be found in the project github README. Note that the most recent data available from FAO for food production in Switzerland was 2017, so all data is from this year.

## Imports and Exports

Let's first start by digging into Swiss imports and exports. We can categorize all the foods based on 6 metacategories: fruits, vegetables, cereals, meats, seafood, and animal products.

![total_imports_vs_exports](/img/total_imports_vs_exports.jpg){: .center-block :}

As can be seen in this plot, Switzerland imports far more than it exports overall. This fits with a general knowledge of the country; Switzerland is rather small and has a relatively dense population, and thus must import significant amounts of food to sustain its citizens. Furthermore, since it has such a low food self-sufficiency, it does not have a lot of food to spare to export.

The animal products category on this graph - that is, non-meat animal-derived products such as dairy products - is rather intriguing compared to the others, since the import and export quantities are about equal. Why might this be? We can take a further look into the specific subcategories of the animal products foods: 

![imports_vs_exports_animal_products](/img/imports_vs_exports_animal_products.jpg){: .center-block :}

This graph brings more light to the topic. Although the animal products metacategory had roughly equal imports and exports, the subcategories reveal a different story. Switzerland is indeed importing and exporting different products, rather than simply acting as a transport hub for food items traveling through. Cheese, a category of which there are many different flavors and consumers like variety, is both heavily imported and exported, likely giving consumers access to a wider variety of cheese types.

Dairy products are one of the few items of which Switzerland has enough excess production to also export some of it, most notably [whey](https://en.wikipedia.org/wiki/Whey) and cheese. Eggs, on the other hand, are nearly exclusively imported.

At first glance, butter might puzzle the reader; the values of imports and exports are both low, so is it possible that the Swiss do not eat butter? Of course, this is hardly the case. Imports and exports are only part of the broader picture of what the Swiss consume, which also includes domestic production. It is likely that Swiss demand for butter is approximately equal to the amount produced within the country, and thus imports and exports are both low. We will return to the topic of how domestic consumption affects our analysis later on.

### Incorporating Location

We have taken a glance at the imports and exports of food by category in Switzerland. In regards to analyzing the carbon foodprint of Swiss consumers, another extremely important aspect of this trading is where all the imported food comes from. Foods that are transported from farther across the globe have a higher carbon cost associated with their transport. Thus, if certain types of food consistently come from distant countries, those foods would be better off avoided by an eco-conscious consumer. We can plot the imports by the continent it comes from and the metacategory of food, weighted by how much of that food is imported.

{% include sankey_diagram.html %}

It turns out that Switzerland imports a vast majority of its food from other countries within Europe. From our analysis, we calculated that 76% of all Swiss food imports come from countries within a 1000 km radius of Switzerland. America, from which Switzerland imports significantly less than from Europe, is the next biggest trading partner. 

## Domestic Production and Consumption

The next step in the Swiss foodprint analysis is to incorporate the FAO data about the food that Switzerland produces. By combining the data on imports, exports, and domestic production, we can calculate how much the Swiss population consumes, and of that consumption, how much of each food is produced in Switzerland versus imported. Our calculation for the total amount of food consumed in Switzerland (including food waste) can be calculated via:

`Swiss consumption = domestic production + imports - exports`

From this figure, we can also calculate how much of what is consumed by the Swiss population is produced domestically versus imported. 

{% include consumption_per_type.html %}

Other than seafood and fruit, Switzerland feeds its citizens more with domestically-produced foods than imported foods. The two exceptional categories make sense; Switzerland is a land-locked country with a cooler climate than most fruit grows in, so it is only natural that the country imports more of these foods than it produces.

Note that in our analysis, we assumed that exports were first sourced from the Swiss-produced foods, then if there were more exports than produced in Switzerland, imports were also opened up to the possibility of exportation. The fact that most of these items show a higher percentage of domestically produced consumption means that this was likely a valid assumption; even with Swiss production being prioritized for exports, there is still more domestically produced food available to Switzerland's citizens than imported food (for every category except fruit and seafood).

## Carbon Emissions

Now that we have gathered the information about where the food eaten in Switzerland is sourced from, we can begin to consider the carbon impact of these foods. Emissions of a food product can be expressed as CO2e ([carbon dioxide equivalent](https://www.theguardian.com/environment/2011/apr/27/co2e-global-warming-potential)), condensing the impact of all greenhouse gases into a single number. For the remainder of this analysis, we will refer to the emissions of food items as carbon-related, though all numbers are CO2 equivalents.

The CO2e of a food item comes from both its inherent carbon cost of production as well as the carbon cost of transporting that item from its country of origin to where it is consumed. The method by which a food item is transported greatly influences the carbon cost of importing; planes, boats, trains, and trucks [each have different emissions](http://shrinkthatfootprint.com/food-miles) in terms of amount of CO2 produced per distance traveled and amount of food transported. Luckily, [data is available](https://www.gate.ezv.admin.ch/swissimpex/index.xhtml) on how various foods enter and exit Switzerland, opening up the possibility of calculating the carbon cost of each type of food based on what countries it comes from and by which transport method. Aggregating the results into the metacategories of food, we can see the following trend of total CO2e normalized by how much of that food item is consumed in Switzerland:

![carbon_normalized_consumption](/img/carbon_normalized_consumption.jpg){: .center-block :}

This begins to answer our research question of how a Swiss consumer can reduce their carbon impact. Even though our analysis has shown that very little meat is imported compared to the other food groups, meat is still by far the most carbon-intensive food group. All three animal-based categories are in fact higher than the three plant-based food groups. This leads us to the question of looking further into transport. How important is transport actually in the carbon intensities of foods? Clearly the transport carbon costs did not overwhelm the inherently high carbon cost of producing meat, so perhaps it is not actually important relative to the inherent carbon cost.

### Closer Look: Transport Carbon Costs

something

# Put here: stacked bar plot of meat

# Put here: stacked bar plot of vegetables

### Correcting the Transport Data

Although Switzerland has an impressive amount of data available on its imports, exports, and production of food, there is one major flaw with the data. The data that [Swiss Impex](https://www.gate.ezv.admin.ch/swissimpex/index.xhtml) provides on the transport methods only details the method by which the food items _crossed the Swiss border_. Hence, if a food item was brought by boat from its country of origin to [Rotterdam, the largest European shipping port](https://en.wikipedia.org/wiki/Port_of_Rotterdam) and then by train from Rotterdam to Switzerland, the Swiss transport data lists the item as coming from its country of origin by train.

For our original analysis, we took the data at face value; that is, if apples were listed as coming to Switzerland by train from New Zealand, we calculated the carbon cost of transport assuming that the apples traveled by train the distance between Switzerland and New Zealand. In an attempt to correct for this strange assumption, we implemented a change to our analysis: for all items coming from outside Europe to Switzerland by rail or road, we first calculate the carbon cost of sending these items by boat to Rotterdam, then traveling the rest of the way from Rotterdam to Switzerland by the original transport method provided. We can compare how this change affects the carbon costs of various foods. Let's take a look at vegetables:

![NL_CH_transport](/img/NL_CH_transport.jpg){: .center-block :}

As we had seen earlier, the inherent production cost of vegetables is far more influential on the total carbon emissions than the carbon contribution from transport. What comes to light from this graph, however, is that it hardly makes a difference that the original data is inaccurate. Considering that vegetables come through Rotterdam makes such a small impact on the analysis because transport has so little to do with the carbon cost, even for low-carbon food items like vegetables.

## Conclusion

![histogram](/img/histogram.jpg){: .center-block :}
![tomatoes](/img/tomatoes.jpg){: .center-block :}
