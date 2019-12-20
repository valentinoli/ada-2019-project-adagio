# -*- coding: utf-8 -*-
"""Plotting functions"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objects as go
import holoviews as hv
from holoviews import opts
import networkx as nx
from networkx.algorithms import bipartite

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge

HTML_DIR = "../docs/_includes/"

def plot_consumption_per_type(data):
    source = ColumnDataSource(data=data)
    # output_file(HTML_DIR + "consumption_per_type.html")

    title = "Swiss Domestic vs. Imported Consumption"
    p = figure(x_range=data.index.tolist(), y_range=(0, 100), plot_height=250, plot_width=700,
               title=title, toolbar_location=None, y_axis_label="ratio (%)")

    r1 = p.vbar(x=dodge("type", -0.125, range=p.x_range), top="domestic_consumption", 
                width=0.2, source=source, color="#b7eebc")

    r2 = p.vbar(x=dodge("type",  0.125, range=p.x_range), top="imported_consumption",
                width=0.2, source=source, color="#ca041e")

    legend_items = [
        ("domestic consumption", [r1]),
        ("imported consumption", [r2]),
    ]

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None

    legend = Legend(items=legend_items, location=(5, 0))
    legend.click_policy="mute"
    p.add_layout(legend, 'right')

    show(p)

    
def preprocess_for_stacked_plot(stacked, emissions):
    food_CO2_consumption = pd.DataFrame(stacked.groupby('subtype').sum()) # put 'stacked' df here
    food_CO2_consumption = food_CO2_consumption.drop(columns=['imports'])
    emissions_median = pd.DataFrame(emissions['Median'])
    lefton = emissions_median.index.to_numpy()
    
    # merge everything of interest for this plot into one df for easy processing
    inherent_and_swiss = emissions_median.merge(food_CO2_consumption, right_index=True, left_on = lefton)
    inherent_and_swiss.drop(labels="key_0", axis=1, inplace=True)
    
    # since a food item could have a high amount of CO2 just because a lot of it is consumed, normalize
    # by the amount consumed in Switzerland (so this new column is kg CO2e per kg food)
    inherent_and_swiss['norm_CO2e'] = inherent_and_swiss['total_kg_CO2e'] / inherent_and_swiss['swiss_consumption']
    
    # make a column of CO2e due to just the inherent production costs
    inherent_and_swiss['kg_CO2e_inherent'] = inherent_and_swiss['total_kg_CO2e'] - inherent_and_swiss['kg_CO2e_transport']
    inherent_and_swiss['total_kg_CO2e_nl'] = inherent_and_swiss['kg_CO2e_inherent'] + inherent_and_swiss['kg_CO2e_transport_via_nl']
    
    return inherent_and_swiss


def preprocess_for_double_stacked_plot(inherent_and_swiss):
    transport = inherent_and_swiss[['total_kg_CO2e','total_kg_CO2e_nl']]
    transport.columns = ['transport','transport_nl']
    transport = pd.DataFrame(transport.stack())
    transport.reset_index(inplace=True)
    transport.columns = ['product','transport','kg_CO2e']

    inherent = inherent_and_swiss[['kg_CO2e_transport','kg_CO2e_transport_via_nl']]
    inherent.columns = ['inherent','inherent_nl']
    inherent = pd.DataFrame(inherent.stack())
    inherent.reset_index(inplace=True)
    inherent.columns = ['product','transport','total_kg_CO2e']
    inherent = inherent.merge(inherent_and_swiss[['kg_CO2e_inherent']].reset_index(), left_on='product', right_on='name').drop(columns=['name'])
    inherent = inherent.drop(columns=['total_kg_CO2e'])
    inherent.columns = ['product','transport','kg_CO2e']

    return transport, inherent


def plot_stacked(inherent_and_swiss):
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 6))

    # Plot the total carbon cost (background)
    sns.set_color_codes("muted")
    sns.barplot(x=inherent_and_swiss.total_kg_CO2e, y=inherent_and_swiss.index, orient = 'h',
                label="Transport", color="b")

    # Plot just the inherent carbon cost of production on top
    sns.set_color_codes("pastel")
    sns.barplot(x=inherent_and_swiss.kg_CO2e_inherent, y=inherent_and_swiss.index, orient = 'h',
                label="Inherent", color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    plt.xticks(fontsize=15)
    plt.yticks(rotation='horizontal')
    plt.xlabel('CO2e (kg)', fontsize=18)
    plt.ylabel('food', fontsize=18)
    plt.title('Inherent vs Transport Carbon Costs', fontsize=20)
    sns.despine(left=True, bottom=True)
    # plt.savefig("../docs/img/stacked_plot_meta.png", dpi=100, bbox_inches='tight')
    

def plot_stacked_double(transport, inherent):
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(9, 9))

    # Plot the total carbon cost (background)
    sns.set_color_codes("pastel")
    sns.barplot(x='kg_CO2e', y='product', hue='transport', data=transport, orient = 'h', palette=['r','b'])

    # Plot just the inherent carbon cost of production on top
    sns.set_color_codes("muted")
    sns.barplot(x='kg_CO2e', y='product', hue='transport', data=inherent, orient = 'h', palette=['r','b'])

    
def plot_total_impex(df):
    plt.figure(figsize=(12, 4))
    ax = sns.barplot(
        x=df.index.get_level_values("type"),
        y=df.values / 1000,  # kg --> tonnes
        hue=df.index.get_level_values("indicator"),
    )

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=13)
    plt.xlabel('commodity', fontsize=18)
    plt.ylabel('quantity (tonnes)', fontsize=18)
    plt.title('Total imports vs. exports', fontsize=20)

    sns.despine()
    # plt.savefig("../docs/img/total_imports_vs_exports.jpg", dpi=100, bbox_inches='tight')


def plot_impex_animal_prods(df):
    plt.figure(figsize=(12, 4))
    ax = sns.barplot(
        x=df.index.get_level_values("subtype"),
        y=df.values / 1000,  # kg --> tonnes
        hue=df.index.get_level_values("indicator"),
    )

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=13)
    plt.xlabel('commodity', fontsize=18)
    plt.ylabel('quantity (tonnes)', fontsize=18)
    plt.title('Imports vs. exports of animal products', fontsize=20)

    sns.despine()
    # plt.savefig("../docs/img/imports_vs_exports_animal_products.jpg", dpi=100, bbox_inches='tight')
    

def bipartite_food_continent(impex):
    # make the nodes: continents on the left, food groups on the right
    continents = impex.index.get_level_values(0).unique().array
    meta_food_groups = impex.columns.levels[0].array
    bi = nx.Graph()
    bi.add_nodes_from(continents, bipartite=1)
    bi.add_nodes_from(meta_food_groups, bipartite=0)

    # make an edge between each continent and each food group
    edges = []
    for continent in continents:
        for food in meta_food_groups:
            edges.append((continent, food))

    bi.add_edges_from(edges, weight=3)
    
    # calculate the initial raw weights, which is the total amount of food for each continent-food pair
    weights = []
    for continent in continents:
        for food in meta_food_groups:
            total_food_amount = impex.xs(continent)[food].xs('imports', level=1, axis=1).to_numpy().sum()
            weights.append(total_food_amount)

    # incorporate these weights into the data for each edge
    for num, name in enumerate(bi.edges(data=True)):
        name[2]['weight'] = weights[num]
        
    
    # make a list of all the weights so can edit them
    all_weights = []
    for (node1,node2,data) in bi.edges(data=True):
        all_weights.append(data['weight'])

    # normalize the weights so they are appropriate for the graph
    for num, wt in enumerate(all_weights):
        all_weights[num] = wt*len(continents)*5/sum(weights)

    # incorporate the normalized weights into the edge data for use in the graph
    for num, name in enumerate(bi.edges(data=True)):
        name[2]['weight'] = all_weights[num]


    top = nx.bipartite.sets(bi)[0]
    pos = nx.bipartite_layout(bi, top)
    
    # make an interactive bipartite graph with Holoviews and Bokeh
    bipartite = hv.Graph.from_networkx(bi, pos, width=all_weights)

    # create text labels for each of the nodes
    labs = ['Africa', 'America', 'Asia', 'Europe','Oceania','animal products', 'cereals', 'fruits', 'meat', 'seafood', 'vegetables']
    labels = hv.Labels({('x', 'y'): bipartite.nodes.array([0,1]), 'text': labs}, ['x', 'y'], 'text')

    # plot the graph with labels
    hv.extension('bokeh')

    (bipartite*labels).relabel("Food Type Imports by Continent").opts(
        opts.Labels(text_color='text', cmap='Category20', yoffset=0.13, fontsize=14, padding=0.2),
        opts.Graph(node_size=30, inspection_policy='edges', fontsize={'title':20},
                   node_hover_fill_color='red', edge_line_width='weight', xaxis=None, yaxis=None, node_fill_color='lightgray',
                   edge_hover_fill_color='red', frame_height=400, frame_width=600, padding=((0.1, 0.15), (0.1, 0.2))))

    # plotting and saving the Sankey diagram to html
    labels = ['Africa', 'America', 'Asia', 'Europe','Oceania','animal_products', 'cereals', 'fruits', 'meat', 'seafood', 'vegetables']
    colors = ['skyblue', 'yellow', 'orange', 'violet', 'green', 'maroon', 'darkblue', 'seashell', 'lavenderblush', 'lightpink', 'turquoise']

    sources = []
    targets = []
    weights = []
    link_colors = []
    for (left_node, right_node, data) in bi.edges(data=True):
        weight = data['weight']
        sources.append(labels.index(left_node))
        targets.append(labels.index(right_node))
        weights.append(weight)
    #    link_colors.append(colors[labels.index(left_node)])

    import plotly.graph_objects as go

    fig = go.Figure(data=[
        go.Sankey(
            node = dict(
                pad=10,
                thickness=10,
                line=dict(color = "black", width = 0.5),
                label=labels,
                color = colors),
            link = dict(
                source=sources,
                target=targets,
                value=weights,
            )
        )
    ])

    fig.update_layout(title_text="Food Type Imports by Continent", 
                      font_size=12)
    fig.show()

    # from plotly.offline import plot
    # plot(fig, filename='../docs/_includes/sankey_diagram.html', include_plotlyjs='directory')

    
def plot_carbon_cost_norm_by_consumption(meta_normalized_CO2):
    plt.figure(figsize=(12, 4))

    ax = sns.barplot(
        x=meta_normalized_CO2.index.get_level_values("type"),
        y=meta_normalized_CO2.values 
    )

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=13)
    plt.xlabel('commodity', fontsize=18)
    plt.ylabel('kg CO2e per kg food', fontsize=18)
    plt.title('Carbon cost normalized by consumption', fontsize=20)
    sns.despine()
    # plt.savefig("../docs/img/carbon_normalized_consumption.jpg", dpi=100, bbox_inches='tight');

    
def plot_fruits_co2(fruits_co2):
    plt.figure(figsize=(12, 4))
    ax = sns.barplot(
        x=fruits_co2.index.get_level_values("subtype"),
        y=fruits_co2['total_kg_CO2e'] / fruits_co2['swiss_consumption'],
    )

    ax.set(
        title="Carbon cost of fruits normalized by their consumption", xlabel="fruit", ylabel="CO2e per kg fruit consumed"
    )
    plt.xticks(rotation=90)
    sns.despine();


def plot_tomatoes(df):
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(
        x=df.index.get_level_values(1),
        y=df.values,
        hue=df.index.get_level_values(0),
    )

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=13)
    plt.xlabel('country of production', fontsize=18)
    plt.ylabel('monthly CO2e emitted (kg)', fontsize=18)
    plt.title('Comparison of growing methods and location for tomatoes', fontsize=20)

    plt.setp(ax.get_legend().get_texts(), fontsize='16') # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='18') # for legend title

    sns.despine()
    # plt.savefig("../docs/img/tomatoes.jpg", dpi=100, bbox_inches='tight')


def plot_emmissions_foodgroup(animal_prods, meat_seafood, vegan_sourced):
    bins = np.linspace(0, 35, 40)

    plt.figure(figsize=(12,6))

    plt.hist(meat_seafood, bins, alpha=0.9, label='meat_seafood')
    plt.hist(vegan_sourced, bins, alpha=0.5, label='vegan')
    plt.hist(animal_prods, bins, alpha=0.5, label='animal_prods')

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('kg CO2e per kg food', fontsize=18)
    plt.ylabel('number of food items', fontsize=18)
    plt.title('Total carbon cost of meats, animal products, and plant-based foods', fontsize=20)

    plt.yscale('log')
    plt.legend(loc='upper right', fontsize=16)
    # plt.savefig("../docs/img/histogram.jpg", dpi=100, bbox_inches='tight')
