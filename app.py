# Importing libraries

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify

import pickle
import json

import rdflib
from math import *
from rdflib import Namespace
import sys
from operator import itemgetter


# Creating data manipulation functions

def GetStarting(latt = None, long = None, departement = None, type_request = None):
    
    if (type_request == "tgv_station"):
        return getTrainStationByPosition(latt, long, departement)
    
    else:
        return getUniversitiesByPosition(latt, long, departement)
     
        
def getTrainStationByPosition(latt = None, long = None, departement = None):
    
    g = rdflib.Graph()
    g.namespace_manager.bind('rdf', Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    g.namespace_manager.bind('rdfs', Namespace('http://www.w3.org/2000/01/rdf-schema#'))
    g.namespace_manager.bind('owl', Namespace('http://www.w3.org/2002/07/owl#'))
    g.namespace_manager.bind('tgv', Namespace('http://www.owl-ontologies.com/unnamed.owl#'))
    g.parse("data/gares-tgv/gares.owl")
    
    response = []
    euclid = []
    ToHtml = ""
    ToJs = ""
    
    if (departement == None):
        query = 'SELECT DISTINCT ?lat ?long ?nomGare  WHERE { ?gare tgv:Latitude ?lat . ?gare tgv:Longitude ?long . ?gare tgv:Nom_Gare ?nomGare }'
        res = g.query(query)

        for row in res:
            element =  row.asdict()
            response.append([element['nomGare'].toPython(),element['lat'].toPython(),element['long'].toPython()])
        for elt in response:
            euclid.append(sqrt( (latt - elt[1])**2 + (long - elt[2])**2))
        for i in range(len(euclid)):
            response[i].append(euclid[i])
        response = sorted(response, key=itemgetter(3))    
        
        response = response[:10]
        print(response)
        for i in range(len(response)):
            ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + " — " + str(round(response[i][3]*111, 2)) + " km</li>"
            ToJs += "L.marker([" + str(response[i][1]) + ", " + str(response[i][2]) + "]).addTo(mymap).bindPopup('TGV station<br><b>" + str(response[i][0]) + "</b><br>lat. " + str(response[i][1]) + "; lon: " + str(response[i][2]) + "<br>" + str(round(response[i][3]*111, 2)) + " km away');\n"

    else:
        query = 'SELECT ?lat ?long ?nomGare  WHERE { ?gare tgv:Latitude ?lat . ?gare tgv:Longitude ?long . ?gare tgv:Nom_Gare ?nomGare . ?gare tgv:NOM_DEP ?nomDep FILTER regex(?nomDep, "^param") }'
        queryWithDepartement = query.replace("param",departement)
        res = g.query(queryWithDepartement)
        for row in res:
            element =  row.asdict()
            response.append([element['nomGare'].toPython(),element['lat'].toPython(),element['long'].toPython()])

        #print(response)
        for i in range(len(response)):
            ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + "</li>"
            ToJs += "L.marker([" + str(response[i][1]) + ", " + str(response[i][2]) + "]).addTo(mymap).bindPopup('TGV station<br><b>" + str(response[i][0]) + "</b><br>lat. " + str(response[i][1]) + "; lon: " + str(response[i][2]) + "');\n"

    return (ToHtml, ToJs)


def getUniversitiesByPosition(latt = None, long = None, departement = None):
    
    g = rdflib.Graph()
    g.namespace_manager.bind('rdf', Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    g.namespace_manager.bind('rdfs', Namespace('http://www.w3.org/2000/01/rdf-schema#'))
    g.namespace_manager.bind('owl', Namespace('http://www.w3.org/2002/07/owl#'))
    g.namespace_manager.bind('IDF_Univ', Namespace('http://www.owl-ontologies.com/unnamed.owl#'))
    g.parse("data/universites/universites.owl")
    
    response = []
    euclid = []
    ToHtml = ""
    ToJs = ""
    
    if (departement == None):
        query = 'SELECT DISTINCT ?latitude ?longitude ?nom  WHERE { ?x IDF_Univ:latitude ?latitude . ?x IDF_Univ:longitude ?longitude . ?x IDF_Univ:nom ?nom }'
        res = g.query(query)

        for row in res:
            element =  row.asdict()
            response.append([element['nom'].toPython(),element['latitude'].toPython(),element['longitude'].toPython()])
        for elt in response:
            euclid.append(sqrt( (latt - elt[1])**2 + (long - elt[2])**2))
        for i in range(len(euclid)):
            response[i].append(euclid[i])
        response = sorted(response, key=itemgetter(3))    
        
        response = response[:8]
        print(response)
        for i in range(len(response)):
            ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + " — " + str(round(response[i][3]*111, 2)) + " km</li>"
            ToJs += "L.marker([" + str(response[i][1]) + ", " + str(response[i][2]) + "]).addTo(mymap).bindPopup('University<br><b>" + str(response[i][0]) + "</b><br>lat. " + str(response[i][1]) + "; lon: " + str(response[i][2]) + "');\n"

    else:
        query = 'SELECT ?latitude ?longitude ?nom  WHERE { ?x IDF_Univ:latitude ?latitude . ?x IDF_Univ:longitude ?longitude . ?x IDF_Univ:nom ?nom . ?x IDF_Univ:dep ?dep FILTER regex(?dep, "^param") }'
        queryWithDepartement = query.replace("param",departement)
        res = g.query(queryWithDepartement)
        for row in res:
            element =  row.asdict()
            response.append([element['nom'].toPython(),element['latitude'].toPython(),element['longitude'].toPython()])

        response = response[:8]
        #print(response)
        for i in range(len(response)):
            ToHtml += "<li><b>" + str(response[i][0]) + "</b> — lat: "  + str(response[i][1]) + "; lon: " + str(response[i][2]) + "</li>"
            ToJs += "L.marker([" + str(response[i][1]) + ", " + str(response[i][2]) + "]).addTo(mymap).bindPopup('University<br><b>" + str(response[i][0]) + "</b><br>lat. " + str(response[i][1]) + "; lon: " + str(response[i][2]) + "');\n"

    return (ToHtml, ToJs)


# Creating API generation functions

app = Flask(__name__, template_folder='templates', static_url_path="/static", static_folder='static')

@app.route('/')

def home():

    return render_template("main.html")

@app.route('/result/', methods = ['POST'])

def predictSite():

    # Gathering input data

    if request.form['latitude'] == '':
        latitude = 46.30
    else:
        latitude = float(request.form['latitude'])
    if request.form['longitude'] == '':
        longitude = 2.30
    else:
        longitude = float(request.form['longitude'])
    if request.form['departement'] == '':
        departement = None
    else:
        departement = request.form['departement']
    if request.form['type_query'] == '':
        type_query = None
    else:
        type_request = request.form['type_query']
    data = [longitude, latitude, departement, type_request]
    type_text = ''
    if type_request == 'tgv_station':
        type_text = 'TGV stations'
    elif type_request == 'university':
        type_text = 'Universities'
    elif type_request == 'both':
        type_text = 'TGV stations and Universities'

    # Calculating by position

    output = GetStarting(latitude, longitude, departement, type_request)
    return render_template("result.html", output_text=output[0], output_map=output[1], latitude=latitude, longitude=longitude, type_text=type_text)

if __name__ == '__main__':
    
    app.run(debug = False, host='127.0.0.1')