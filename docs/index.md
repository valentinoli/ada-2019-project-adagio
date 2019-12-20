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

Data for this project was sourced from the [Food and Agriculture Organization of the United Nations (FAO)](http://www.fao.org/faostat/en/#data) and [Swiss Impex](https://www.gate.ezv.admin.ch/swissimpex/index.xhtml). More details on these datasets can be found in the project github README.

## Imports and Exports

Let's first start by digging into Swiss imports and exports. We can categorize all the foods based on 6 metacategories: fruits, vegetables, cereals, meats, seafood, and animal products.

![total_imports_vs_exports](/img/total_imports_vs_exports.jpg){: .center-block :}
![imports_vs_exports_animal_products](/img/imports_vs_exports_animal_products.jpg){: .center-block :}
{% include sankey_diagram.html %}
{% include consumption_per_type.html %}
![carbon_normalized_consumption](/img/carbon_normalized_consumption.jpg){: .center-block :}
![NL_CH_transport](/img/NL_CH_transport.jpg){: .center-block :}
![histogram](/img/histogram.jpg){: .center-block :}
![tomatoes](/img/tomatoes.jpg){: .center-block :}

## normalized carbon cost bar graph for all food groups

## comment that meat is high like expected
## then stacked bar plot of meat
## and stacked bar plot of fruit