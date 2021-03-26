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



def getTrainStationByPosition(latt,long):
    
    
    
    
    print("PARAM")
    g = rdflib.Graph()
    g.namespace_manager.bind('rdf', Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    g.namespace_manager.bind('rdfs', Namespace('http://www.w3.org/2000/01/rdf-schema#'))
    g.namespace_manager.bind('owl', Namespace('http://www.w3.org/2002/07/owl#'))
    g.namespace_manager.bind('tgv', Namespace('http://www.owl-ontologies.com/unnamed.owl#'))
    g.parse("gares.owl")
    query = 'SELECT DISTINCT ?lat ?long ?nomGare  WHERE { ?gare tgv:Latitude ?lat . ?gare tgv:Longitude ?long . ?gare tgv:Nom_Gare ?nomGare }'
    #queryWithParam = query.replace("param",departementParam)
    res = g.query(query)
    #res = g.query('SELECT * WHERE { ?x ecole:secteur ?secteur FILTER regex(?secteur, "^Privé")}')
    #res = g.query('SELECT * WHERE { ?x ecole:code_dep ?code_dep FILTER regex(?code_dep, "^94")}')
    
    response = []
    euclid = []
    
    for row in res:
       element =  row.asdict()
       response.append([element['nomGare'].toPython(),element['lat'].toPython(),element['long'].toPython()])
    for elt in response:
        #print("testzoa",elt,elt[1],elt[2])
        euclid.append(sqrt( (latt - elt[1])**2 + (long - elt[2])**2))
    for i in range(len(euclid)):
        response[i].append(euclid[i])
    response = sorted(response, key=itemgetter(3))
    
    Html = "<li><b>nomGare</b> — lat: latitude; lon: longitude — d*111 km</li>"
    ToHtml = ""
    response = response[:2]
    for i in range(len(response)):
        ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + " — " + str(round(response[i][3]*100)) + " km</li>"


        
    
    
    print(ToHtml)
    
    
    
    #print(response[:10])
    return response

#<li><b>nomGare</b> — lat: latitude; lon: longitude — d*111 km</li>


getTrainStationByPosition(45,4)







