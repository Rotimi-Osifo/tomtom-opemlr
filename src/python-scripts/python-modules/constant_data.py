# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:45:07 2022

@author: OOSIFO
"""

selected_road_names = ["Oscarsleden", "Andréegatan", "Götatunneln", "Mårten Krakowgatan", "Marieholmsleden", \
                       "Marieholmstunneln", "Västerleden", "Gnistängstunneln", "Gnistängsmotet", \
                       "Lundbytunneln", "Hisingsleden", "Söderleden", "Åbromotet", "Sisjömotet", \
                       "Askim", "Järnbrottsmotet", "Tynneredsmotet", "Fiskebäcksmotet", "Hagenmotet", "Bräckemotet", \
                       "Ivarsbergmotet", "Eriksbergsmotet", "Lundbyleden", "Brantingsmotet", "Leråkersmotet", \
                       "Brunnsbomotet", "Tingstadstunneln", "Gullbergsmotet", "Olskroksmotet", "Kungsbackaleden", \
                       "E6", "E20", "E45", "E21", "Ovärdersgatan", "Hjalmar Brantingsgatan", "Hisingsbron", \
                       "Yrvädersgatan", "Kråketorpsgatan", "kungsbackavägen", "Nämndemansgatan", "Göteborgsvägen", \
                       "Gamlakungsbackavägen", "Mölndalsbro", "Broslättsgatan", "kungsbackaleden", "Kungsbackaleden",\
                       "Boråsleden", "Nellickevägen", "Mölndalsvägen", "Örgrytevägen"]
    
road_ref_list = ["E 6;E 20", "E 6;E 21", "E 45;E 21", "E 6.21", "E 6", "E 20", "E 45", "O 533", "O 514", "O 518"]

road_id_list = [10906540, 4267338, 10958242]

osm_road_type_list = ["motorway_link", "motorway", "trunk_link", "trunk", "residential", "primary", "secondary", "tertiary"]

highway_frc_mapping = {
        'motorway': 0,
        'motorway_link': 0,
        'trunk': 1,
        'trunk_link': 1,
        'primary': 2,
        'primary_link': 2,
        'secondary': 3,
        'secondary_link': 3,
        'tertiary': 4,
        'tertiary_link': 4,
        'road': 5,
        'road_link': 5,
        'unclassified': 5,
        'residential': 5,
        'living_street': 6,
    }

highway_fow_mapping = {
        'motorway': 1,
        'motorway_link': 6,
        'trunk': 2,
        'trunk_link': 6,
        'primary': 3,
        'primary_link': 6,
        'secondary': 3,
        'secondary_link': 6,
        'tertiary': 3,
        'tertiary_link': 6,
        'road': 3,
        'road_link': 6,
        'unclassified': 0,
        'residential': 3,
        'living_street': 3,
    }