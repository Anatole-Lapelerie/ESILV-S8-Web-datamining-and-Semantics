# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import rdflib
from rdflib import Namespace
import sys


g = rdflib.Graph()
g.namespace_manager.bind('rdf', Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
g.namespace_manager.bind('rdfs', Namespace('http://www.w3.org/2000/01/rdf-schema#'))
g.namespace_manager.bind('owl', Namespace('http://www.w3.org/XML/1998/namespace'))
g.namespace_manager.bind('ecole', Namespace('http://www.owl-ontologies.com/unnamed.owl#%27'))
g.parse("TgvGare.owl")
#res = g.query("SELECT ?lat ?long WHERE { ?gare tgv:Latitude ?lat . ?gare tgv:Longitude ?long .}")
#res = g.query('SELECT * WHERE { ?x ecole:secteur ?secteur FILTER regex(?secteur, "^Privé")}')
res = g.query('SELECT * WHERE { ?x ecole:code_dep ?code_dep FILTER regex(?code_dep, "^94")}')


for i in res:
    print(i.asdict()['code_dep'].toPython())

print(len(res))