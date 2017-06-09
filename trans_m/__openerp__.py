# -*- coding: utf-8 -*-
{
    'name': "transM",

    'summary': """
        Modul de Containers per al prijecte de 2DAM SGE 2016
        containers""",

    'description': """
        Una empresa de transport marítim vol gestionar el seu negoci amb Odoo. Quasi tot és útil, però hi ha coses que no suporta directament Odoo. 
Cal adaptar Odoo amb un mòdul per a l’empresa de transport amb les següents funcionalitats:

Aquest mòdul tindrà una bona descripció i un logo a l’hora d’instal·lar-se.
Models:
L’unitat mínima en la que treballa l’empresa de transport és el “container”. Pot ser de diferents tipus amb diferents preus. 
L’empresa dona el servici de guardar el container fins a que el client el tinga ple. Cal mostrar el progrés del 0% al 100% d’ompliment. 
Un container pot ser enviat encara que no estiga al 100% o no estiga pagat encara fincant manualment el estat de disponible. 
En un container s’ha de guardar el client que envia, el que rep la mercaderia, un identificador, el viatge en el que va, preu, pes.
Un viatge té un orige, destí, llista de containers, pes total, vaixell.
Al crear un container, cal afegir-lo al viatge. No pot existir un container sense viatge associat.
Per començar a treballar, l’empresa ens dona uns fitxer de text amb dades bàsiques. Cal transformar-lo en un xml per importar cada vegada que s’instal·la o actualitza el mòdul: Contenidors, paisos, viatges, vaixells 
Vista:
En la vista tree dels containers, els que estiguen disponibles tindran fons verd, els que estiguen sense plenar tindran color groc, els que estiguen plens però no pagats tindran fons roig.
En la vista tree dels vaixells, tidran color blau els que estan de viatge en este moment.
En la vista tree dels viatges s’indicarà amb una barra de progrés el % del viatge que duu. 
Els viatges ja fets no eixiran per defecte en la vista tree, encara que es pot indicar en els filtres que si apareguen.
Es pot filtrar per containers plens, a mitges, pagats o no i disponibles.

    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/containers.xml',
        'views/ships.xml',
        'views/travels.xml',
        'views/templates.xml',        
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
  #      'demo/vaixell.xml',
  #      'demo/viatges.xml',
  #      'demo/cont.xml',
#        'demo/servicio.xml',
    ],
}
