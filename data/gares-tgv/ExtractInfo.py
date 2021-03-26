# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:24:33 2021

@author: loulo
"""

import rdflib
from math import *
from rdflib import Namespace
import sys
from operator import itemgetter



def getTrainStationByPosition(latt, long, departement, type_request):
    
    g = rdflib.Graph()
    g.namespace_manager.bind('rdf', Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    g.namespace_manager.bind('rdfs', Namespace('http://www.w3.org/2000/01/rdf-schema#'))
    g.namespace_manager.bind('owl', Namespace('http://www.w3.org/2002/07/owl#'))
    g.namespace_manager.bind('tgv', Namespace('http://www.owl-ontologies.com/unnamed.owl#'))
    g.parse("data/gares-tgv/gares.owl")
    query = 'SELECT DISTINCT ?lat ?long ?nomGare  WHERE { ?gare tgv:Latitude ?lat . ?gare tgv:Longitude ?long . ?gare tgv:Nom_Gare ?nomGare }'
    res = g.query(query)
    
    response = []
    euclid = []
    
    for row in res:
       element =  row.asdict()
       response.append([element['nomGare'].toPython(),element['lat'].toPython(),element['long'].toPython()])
    for elt in response:
        euclid.append(sqrt( (latt - elt[1])**2 + (long - elt[2])**2))
    for i in range(len(euclid)):
        response[i].append(euclid[i])
    response = sorted(response, key=itemgetter(3))
    
    ToHtml = ""
    ToJs = ""

    response = response[:10]
    for i in range(len(response)):
        ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + " — " + str(round(response[i][3]*111, 2)) + " km</li>"
        ToJs += "L.marker([" + str(response[i][1]) + ", " + str(response[i][2]) + "]).addTo(mymap).bindPopup('TGV station<br><b>" + str(response[i][0]) + "</b><br>lat. " + str(response[i][1]) + "; lon: " + str(response[i][2]) + "<br>" + str(round(response[i][3]*111, 2)) + " km away');\n"

    return (ToHtml, ToJs)


getTrainStationByPosition(45,4)







