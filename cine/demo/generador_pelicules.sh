#!/bin/bash

echo '<openerp><data>' > pelis.xml

for i in *.jpg; do
    id="$(echo $i | cut -d"." -f1)"
    nombre="$(echo $id | tr "_" " ")"
    poster="$(base64 $i)"
    echo -e  '<record id="'$id'" model="cine.pelicula">\n<field name="name">'$nombre'</field>\n<field name="poster">'"$poster"'</field></record>' >> pelis.xml
done

echo '</data></openerp>' >> pelis.xml
