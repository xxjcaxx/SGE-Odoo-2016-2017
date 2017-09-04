#!/bin/bash

echo '<openerp><data>' > salas.xml
echo '<openerp><data>' > butaques.xml
echo '<openerp><data>' > sessions.xml
echo '<openerp><data>' > entrades.xml

for i in cine1 cine2;do
	for j in {1..6}; do
		echo '<record id="sala_'$i'_'$j'" model="cine.sala"><field name="name">Sala '$i' '$j'</field><field name="cine" ref="'$i'"></field></record>' >> salas.xml
		for k in {1..10}; do
		 for l in {1..10}; do
			echo '<record id="butaca_'$i'_'$j'_'$k'_'$l'" model="cine.butaca"><field name="fila">'$k'</field><field name="butaca">'$l'</field><field name="sala" ref="sala_'$i'_'$j'"></field></record>' >> butaques.xml
		 done
		done
 		
		echo '<delete model="cine.sessio" id="sessio_'$i'_'$j'"></delete><record id="sessio_'$i'_'$j'" model="cine.sessio"><field name="name">Sessio '$i' '$j'</field><field name="sala" ref="sala_'$i'_'$j'"></field><field name="pelicula" ref="agitese_antes_de_usarla"></field><field name="hora" eval="(datetime.now()+timedelta(+'$j')).strftime('\''%Y-%m-%d %H:%M:%S'\'')"></field></record>' >> sessions.xml

		for k in {1..9}; do
				echo '<delete id="entrada_'$i$j'_'$k'" model="cine.entrada"/><record id="entrada_'$i$j'_'$k'" model="cine.entrada"><field ref="butaca_'$i'_'$j'_1_'$k'" name="butaca"></field><field name="sessio" ref="sessio_'$i'_'$j'"></field></record>' >> entrades.xml
		done
	done
done

echo '</data></openerp>' >> salas.xml
echo '</data></openerp>' >> butaques.xml
echo '</data></openerp>' >> sessions.xml
echo '</data></openerp>' >> entrades.xml






