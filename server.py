# -*- Mini-projet -*-
# Author: Paolo De Keyzer/Thibault Kiss
# Version: 14/11/2015

from bottle import route, run, template, static_file, error, post, request
import json


def page(url,name,dbname):
    #ouvrir fichier contenant la database
    with open('database.json','r+') as SettingsData:
        settings=json.load(SettingsData)

    #code et style de n'importe quelle page
    return '''
    <link rel="stylesheet" type="text/css" href="../static/style.css" />
    <style>
    body{{background-image:url({});
    background-attachment:scroll;
    background-position:top center;
    background-size:100%;}}
    </style>
    <head>
    <title>
    {}
    </title>
    </head>
    <body>
    <table height="100%" width="40%" align="center" valign="center" cellspacing="0" cellpadding="0" style="border-radius: 25px" >
    <tr style="height: 30%"><td></td></tr><tr class="titres">
    <div class="success">
    <td align="center" valign="center" style="background: rgba(0, 0, 0, 0.7); border-radius: 25px" >
    {}<br>Saison {} episode {}<br><br>
    <form action="/modif/{}" method="get">
    <input type="submit" value ="Modifier" /></form >
    </td></tr>
    </div>
    <tr style="height:30%"><td></td></tr>
    </table>
    </body>'''.format(url,name,name,settings[dbname]["Season"],settings[dbname]["episode"],dbname)
    #au dessus: variables possibles pour les différentes pages. Url:url de l'image, name:Nom ,color:couleur du texte,
    #Settings[dbname]["season"]et["serie"]:récupération du statut de la série dans la base de données.
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root='./static')

@route('/serie/<abbrev>')
def serie(abbrev):
    with open('database.json','r+') as data:
        dico=json.load(data)
    #appel de la fonction page() pour créer la page
    return page(dico[abbrev]["urlimage"],dico[abbrev]["name"],dico[abbrev]["pagename"])





# Page d'accueil
@route('/')
def app():
    #unordered list contenant les différentes séries
    links = '<ul>'
    #ouverture de la database
    with open('database.json','r+') as SettingsData:
        settings=json.load(SettingsData)
    for serie in settings:
        links += '<li><a href="{}">{}</a></li>'.format(settings[serie]['url'],settings[serie]['name'])
    links+='<li><a href={}>Ajouter serie</a></li>'.format("http://localhost:1320/ajout")
    links += '</ul>'
    #code et style de la page
    return '''

    <head>
    <title>Ou j\n'en suis?</title>
    </head>
    <style>
    body{{background-image:url("http://imageshack.com/a/img911/5514/0nBnHO.png");
    background-size:90%;
    background-attachment:scroll;
    background-position:top center;}}
    td.impact {{
    font-family:Impact, Charcoal, sans-serif;
    font-size:200%;}}
    </style>
    <body>
    <table width="18%" height="100%" align="left" valign="top">
    <tr><td>
    <tr><td class="impact" align="center" bgcolor="orange" valign="top">
    Liste de Series<br>{}</td></tr></table>

    </body>


    '''.format(links)

@route('/modif/<abbrev>')
def modif(abbrev):
    return '''
    <head><title>Modifier série</title></head>
    <link rel="stylesheet" type="text/css" href="../static/style.css" />
    <body><p>
    <table height="100%" align="center" valign="center">
    <form action="/yay" method="post">
    <tr>
    <td valign="bottom"><input type ="hidden" name ="NomDeLaSerieAModifier" value="{}" /> </br></td></tr>
    <td align="center">Saison</td>
    <td align="center"><input type ="text" name ="Saison" /> </br></td></tr>
    <td align="center" valign="top">Episode</td>
    <td align="center" valign="top"><input type ="text" name ="Episode" /> </br></td></tr>
    <tr align="center"><td>
    <input type="submit" value ="Changer" /></form ></td>
    </tr></table></p>
    </body>
    '''.format(abbrev)

@post('/yay')
def yay():

    with open("database.json","r+") as Dbseries:
        dicoSeries = json.load(Dbseries)
        #remplacement des anciennes valeurs par celles insérées dans les Entry
        Season=request.forms.get("Saison")
        Episod=request.forms.get("Episode")
        try:
            S=int(Season)
            E=int(Episod)

            dicoSeries[str(request.forms.get("NomDeLaSerieAModifier"))]['Season'] = S
            dicoSeries[str(request.forms.get("NomDeLaSerieAModifier"))]['episode'] = E
            Dbseries.seek(0)
            Dbseries.write(json.dumps(dicoSeries,indent=2,sort_keys=True))
            Dbseries.truncate()
            texte="Vous avez correctement modifié votre progression dans cette serie!"
            image="http://soocurious.com/fr/wp-content/uploads/2014/09/homme-reussite.jpg"
        except:
            texte="Erreur d'entrée"
            image="http://www.reveservices.com/uploads/news/sante_ftigue.jpg"
    return '''
    <head><title>Bravo!</title></head>
    <link rel="stylesheet" type="text/css" href="static/style.css" />
    <style>
    body{{background-image:url({});
    background-attachment:scroll;
    background-position:top center;
    background-size:100%;}}
    </style>
    <body>
    <h1 align="center"><font color="black">{}</font></h1>
    <p align="center"><a href = "http://localhost:1320"> Retour </a></p>
    </body>


    '''.format(image,texte)
@route('/ajout')
def ajout():
    return '''
    <head><title>Modifier série</title></head>
    <link rel="stylesheet" type="text/css" href="static/style.css" />
    <body><p>
    <table height="100%" align="center" valign="center">
    <tr style="height: 30%"><td></td></tr>
    <form action="/success" method="post">
    <tr><td></td></tr>
    <tr>
    <td align="center" valign="bottom">Nom de la série à ajouter</td>
    <td valign="bottom"><input type ="text" name ="NomDeLaSerieAAjouter" /> </br></td></tr>
    <td align="center">Url de l'image de fond</td>
    <td align="center"><input type ="text" name ="urlimage" /> </br></td></tr>
    <td align="center">Saison</td>
    <td align="center"><input type ="text" name ="Saison" /> </br></td></tr>
    <td align="center">Episode</td>
    <td align="center"><input type ="text" name ="Episode" /> </br></td></tr>
    <td align="center" valign="center">Nom De l'url de la page<br> p.ex.:"localhost:1320/serie/<nomdelurl>"</td>
    <td align="center" valign="center"><input type ="text" name ="abbrev" /> </br></td></tr>
    <tr align="center"><td>
    <input type="submit" value ="Changer" /></form ></td>
    </tr>
    <tr style="height: 30%"><td></td></tr>
    </table></p>
    </body>
    '''
@post('/success')
def success():

    with open("database.json","r+") as Dbseries:
        dicoSeries = json.load(Dbseries)
        #remplacement des anciennes valeurs par celles insérées dans les Entry
        name=request.forms.get("NomDeLaSerieAAjouter")
        abbrev=request.forms.get("abbrev")
        urlimage=request.forms.get("urlimage")
        couleurtexte=request.forms.get("couleurtexte")
        Season=request.forms.get("Saison")
        Episod=request.forms.get("Episode")
        try:
            S=int(Season)
            E=int(Episod)
            dicoSeries[str(request.forms.get("abbrev"))]={}
            dicoSeries[str(request.forms.get("abbrev"))]['urlimage'] = urlimage
            dicoSeries[str(request.forms.get("abbrev"))]['couleurtexte'] = couleurtexte
            dicoSeries[str(request.forms.get("abbrev"))]['name'] = name
            dicoSeries[str(request.forms.get("abbrev"))]['url'] = ("http://localhost:1320/serie/{}".format(abbrev))
            dicoSeries[str(request.forms.get("abbrev"))]['pagename']=abbrev
            dicoSeries[str(request.forms.get("abbrev"))]['Season'] = Season
            dicoSeries[str(request.forms.get("abbrev"))]['episode'] = Episod
            Dbseries.seek(0)
            Dbseries.write(json.dumps(dicoSeries,indent=2,sort_keys=True))
            Dbseries.truncate()
            texte="Vous avez correctement ajouté cette serie!"
            image="http://soocurious.com/fr/wp-content/uploads/2014/09/homme-reussite.jpg"
        except:
            texte="Erreur d'entrée"
            image="http://www.reveservices.com/uploads/news/sante_ftigue.jpg"
    return '''
    <head><title>Bravo!</title></head>
    <link rel="stylesheet" type="text/css" href="static/style.css" />
    <style>
    body{{background-image:url({});
    background-attachment:scroll;
    background-position:top center;
    background-size:100%;}}
    </style>
    <body>

    <h1 align="center">{}</h1>
    <p align="center"><a href = "http://localhost:1320"> Retour </a></p>
    </div>
    </body>

    '''.format(image,texte)


# Add a new link
@post('/addlink')
def addlink():
    newentry = json.loads(request.body.read().decode('utf-8'))
    database['Series'].append(newentry)


# Launch the server
run(host='localhost', port=1320)
