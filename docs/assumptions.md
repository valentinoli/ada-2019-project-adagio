---
layout: page
title: Assumptions
image: /img/flag.gif
---

The following list is the detailed set of assumptions made when handling the data from Impex.

**Cereals**
* Cereals imported for alcohol manufacturing, a category specified by Impex, were not included in the analysis since alcohol is not a recommended food group and cannot be used for nutrition purposes.
* While nearly all grain types in the Impex data specified when they were imported/exported for human consumption, rice was the one exception to this rule. Rice is generally consumed in large quantities and thus could not be exluded from the analysis. Thus, the rice data was assumed to be for human consumption purposes when it was listed as `"rice (excluding rice for the manufacture of brewers' malt or beer or for animal feeding)"`.
* Impex provided data for rice in several categories. One of these categories was `"rice in the husk"`, specifically listed as being for human consumption. Humans cannot eat risk husks, but we assumed that Switzerland processes this rice and removes its husk after importing it. It was thus included in edible rice, despite the fact that it might also be a weight overestimation due to the weight of the husk.
* Impex offers data for `"durum wheat"` as well as `"wheat and meslin (excluding durum wheat)"`. To ensure compatibility with the FAO data, which only has `"wheat"`, we combined these categories together into simply `"wheat"`.
* While Impex does have several subcategories of its data on beans, these subcategories were not based on species and thus could not be matched up to the emissions data nor to FAO data. We therefore decided to combine all beans and lentils data from Impex into one `"beans"` category to ensure compatibility across our datasets.

**Meats**
* Impex offered data for imports and exports of **live animals**. While most of these animals (all except poultry/fowl) were specified whether or not they were for slaughter, we decided to exclude these from our data. This is because according to the metadata of FAO on meat, `"Data relate to animals slaughtered within national boundaries, irrespective of their origin."` Thus, the meat produced from these animals is counted as domestically produced meat by FAO.
* Edible **offal** (organs and other non-standard cuts of meat) was excluded from our analysis; this is because offal can in a way be considered a by-product of standard meat production. While we have carbon intensities for "bone-free meat", we have no way of quantifying the carbon cost of offal. The one exception to this rule was poultry, where offal was included since the data for offal cannot be separated from the data for cut-up poultry meat.
* Meat from very **rare, non-standard animals** (e.g. hares, guinea fowl) were not accounted for, since there is no carbon intensity data for these animals and no comparable animal with which to infer the carbon intensity. These rare meats are also hardly consumed in Switzerland, so we assumed excluding them would not make an impact on our analysis.
* Meat from geese and ducks were combined together, since we had the carbon emissions of duck meat but not for goose meat. These animals were assumed to be similar enough to make that combination.

**Seafood**
* Several types of crustaceans were combined into the lobster category since there is no data on carbon emissions of these other animals. Thus, the lobster consumption data includes lobster, crab, crawfish, rock lobster, and any other crustacean that is not shrimp or prawns.
* Similarly, squid, octopus, and cuttlefish were combined under one category, since the only available carbon intensities for these animals was the average of all three.
* All molluscs (mussels, clams, snails, oysters, scallops, abalone) were lumped together and assumed to have the carbon intensities of mussels, the only value available for this group of animals.

**Vegetables**
* A handful of vegetables which were available in Impex were not included in the analysis since they were not available in the FAO data. This was acceptable since these vegetables are not staples. They included parsley, rhubarb, and cardoons, among others. We decided that it was better to never include these vegetables in the analysis rather than assuming that their production in Switzerland is zero, because FAO does list items which have zero production. These items were not even listed, which would indicate that their production is not tracked.
* Conversion of fresh onion emissions to dried onion emissions based on weight:
  1 cup dried onion = 143.8g => equivalent fresh onion = 1388g => multiply fresh emission values by (9.65) 10
* We have no information regarding the growing methods of vegetables, therefore where we have values for different methods, e.g. outside vs. in greenhouses (heated and passive), we average these values, assuming that there is a relatively even distribution of these growing methods.

**Fruits**
* Impex lumps raspberries, blackberries, mulberries, and loganberries together. These were thus all included under the category of `"raspberries"`. Similarly, the `"cranberries"` category includes both cranberries and bilberries.

**Method of Transport**
* All data provided in the method of transport is based on **country of origin**, _not_ country of production. While this is not ideal for our analysis since a food item may have traveled amongst other countries before reaching the country that sent it to Switzerland, we had to accept it and assume that the country of origin is the same as the country of production since there was no way to impute data to make up for this missing information.
* The most unfortunate aspect of the transport data from Impex is that it only gives the **method of transport by which a food item crossed the Swiss border**. For example, if beef was taken by boat from New Zealand to Rotterdam (the largest shipping port in Europe), then taken by train from Rotterdam to Switzerland, that beef is listed as coming by train from New Zealand. While we had hoped to find a dataset which was more detailed, the Impex data already had far more detail than any other source available. One option we had to get around this issue was to use the continent classification that we added to our dataset: we could have assumed that anything listed as coming by rail or road from outside Europe first comes to Rotterdam by boat, then travels by the road/rail method the rest of the way. We did not process the data in this way, however, because we felt it assumed too much. We have no reason to believe food comes to Rotterdam by boat, rather than going to China by boat first, getting flown part of the way, or any other number of variations that are unpredictable. We therefore instead decided to take the data at face-value; that is, we assume that food coming from countries across the ocean by rail or road indeed travel that entire way by rail or road. This is completely unrealistic and we know it greatly affects the analysis, but we did not have a good way to get around the lack of data.


**Miscellaneous**
* We did not include data on live animals imported for breeding, nor for crops imported for sowing. These items are not _directly_ implicated in the food chain, and thus they did not fit into our analysis. They do, however, indirectly contribute to the carbon cost of food in Switzerland; the offspring of these breeding animals and imported crops will technically have a higher carbon cost than offspring from Swiss-bred animals and crops, due to the transport required to bring their parent to Switzerland.
* Data which contained multiple food groups and could not be broken down further, such as `"Fruit and nuts, uncooked or cooked by steaming or boiling in water, frozen"` were excluded since we did not want unintentional overlap of various food types within one food category of our data.
* In order to avoid excessive complication and mismatching amongst the datasets, we decided to only examine fresh foods from Impex (where "fresh" includes chilled and frozen). We thus excluded anything preserved by chemical means, such as pickled or dried (other than beans for data compatibility reasons).



The following list is the detailed set of assumptions made when handling the data from FAO.

**Meats**
* "Game" meat was excluded; while it was not an insignificant amount of meat produced (1891 tonnes in 2017), there is no way of knowing what animals this meat came from, so it is useless for our analysis.
* Rabbit meat was excluded because we do not have a value of carbon emissions for it or any similar animal (the same reason why it was excluded from Impex data), but it was a small amount of meat (971 tonnes in 2017) so it will not greatly skew the analysis.
* According to the FAO metadata, `"Data relate to animals slaughtered within national boundaries, irrespective of their origin."` This means that if we chose to analyze our data with the country-specific emissions for meats, our analysis may be wildly inaccurate due to there being carbon-influencing events which are beyond the reach of our data. Luckily this does not pose an issue when using global average emissions values for meats, but it does impede any more specific analysis.
* From the metadata, the definition for chicken meat is `"Fresh, chilled or frozen. May include all types of poultry meat if national statistics do not report separate data."` When we downloaded the meat production data from FAO, we noticed that there was zero production of duck and goose meat. This would indicate that Switzerland combines all domestic birds under the `chicken` category. We assumed that this was the case since that seemed more likely than Switzerland not producing any poultry meat other than chicken. Due to this, we combined meat from all domestic birds (ducks, geese, turkeys, and chickens) into one category and labeled it as `chicken`.

**Seafood**


The FAO data on seafood production had to be harvested from another site than where the rest of the production data was obtained from ([FAO fishery data](http://www.fao.org/fishery/statistics/global-commodities-production/query/en)). The data indicated that Switzerland produces fish, but there was no data available for production of other seafood from Switzerland. We assumed that, since Switzerland is landlocked, the only seafood it produces are lake fish, and the other values were nonexistent because they were zero. While the data provided were separated into one amount for freshwater fish and one amount for partly-fresh/partly-saltwater fish, we combined this into a single category and considered it simply as "fish".

The following assumptions, choices, and aggregations were made when merging Impex, FAO, and carbon intensities data.


**Animal Products**
* In both Impex and FAO, cheese is not separated by the animal from which the milk originated. Our carbon intensities data is also not specific to the animal. While it seems likely that cheese from cow milk would have a different carbon intensity than cheese from goat or sheep milk since the animals have different carbon costs for their meat, we chose to simply lump all the cheese together and use the provided global average for all cheese.

**Cereals**
* Beans can be imported and exported in either their dried or fresh form. While Impex and FAO specify when beans are dried or fresh, the emissions data was only available for either an average of all beans or for individual species. As mentioned above, species of beans were not available in Impex. We thus decided to use the average for all beans, and to assume that this average was for _fresh_ beans. With that decided, we had to deal with the fact that dried beans are much lighter in weight than fresh beans. Using a conversion factor found across the internet in various cooking recipes, we multiplied the weight of the dried beans by 2.5 to approximate their weight as if they were fresh/cooked.

**Meats**
* As stated previously, the data for meat from all domestic fowl was included under the category of `"chicken"`. The emissions intensity for chicken was used for all of this data.

**Vegetables**
* There were 3 items, all vegetables, which were in the Impex data but not in FAO: brussels sprouts, celery, and other edible roots. We decided to exclude these minor food items from the analysis since we have no way of inferring their domestic production values.

**Fruits**
* As stated earlier, the Impex data includes raspberries, blackberries, mulberries, and loganberries all under one category. FAO does not track the latter 3 berries. Thus, all of these berry types from Impex were assumed to be raspberries. Similarly, cranberries includes cranberries and bilberries.

**Miscellaneous**
* In all datasets, any data which was listed as part of a category, `"not elsewhere specified (nes)"` was not included. This is because we had no way of knowing what the carbon cost of such items would be or where they would fit in with the other food groups that were specified.
* We decided to exclude data from all sources on oils, seeds, and nuts, since these are not a major food group and would have added unnecessary complexity to our analysis.
* There were a few food items which were not listed in the Impex data but which had non-zero production. After excluding `"nes"` items and nuts and oils, this list included: blueberries, mixed grain, hops, lupins, green maize, and sugar beet. These items were exluded since it was safer to not include them rather than to assume they had zero imports and exports.

The following list is the detailed set of assumptions made when handling the emssions data.

* The emissions categories available were less comprehensive than the FAO/Impex categories. The items lacking emissions values were estimated using the closest available emissions category. For a full list, please see the last 15 lines of [this file](https://drive.google.com/open?id=1KDBiuJ4la_vW3X2_KnD18IQFb00Qoh6B) in the data folder.
* Clune, Crossin and Verghese's 2017 [review](https://www.sciencedirect.com/science/article/pii/S0959652616303584) collates carbon emissions data from ~1700 studies worldwide, a summary of which is available in this [file](https://drive.google.com/open?id=1TW0ZJdBG6ATQWRzMz4DFg4aa-_0OwNGl). These studies do not provide an even representation of the different food categories and thus some global emissions estimates are averages of several studies in different countries, while others are the result of a unique study. The median values used for estimation of carbon emissions linked to Swiss consumption are recorded in [this file](https://drive.google.com/open?id=1QSvMdbj8Nq-397NUZCM-HR4WfbrPSnrT).
