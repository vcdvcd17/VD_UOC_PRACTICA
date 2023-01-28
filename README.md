# VD_UOC_PRACTICA
# Visualització dades bicing <br>
Aquest projecte conté el codi per crear una visualització de les dades de l'estat de les estacions del Bicing de Barcelona.

Les dades amb llicència Creative Commons 4.0 es poden trobar aquí:<br> - https://opendata-ajuntament.barcelona.cat/data/ca/dataset/estat-estacions-bicing<br>
I l'informació de l'ubicació de les estacions aquí:<br>  - https://opendata-ajuntament.barcelona.cat/data/ca/dataset/informacio-estacions-bicing<br>
En els dos casos la freqüència d'informació es d'aproximadament 5 minuts per estació. Per a la creació del projecte es necessita descomprimir els arxius descàrregats i executar l'arxiu Preprocessing.ipynb per a preprocessar les dades.

# Descripció d'arxius
**app.py:** Codi de l'aplicació<br>
**data:** Carpeta amb els arxius amb les dades preprocessades.<br>
**Preprocessing.ipynb:**  Codi per al preprocessament de les dades originals.<br>
**Dockerfile:** Arxiu per a la realització del deployment de l'aplicació.<br>
**requirements.txt:** Arxiu amb les llibreries necessaries per executar l'aplicació.<br>
**.mapbox_token_EMPTY:** Arxiu on guardar el mapbox token privat per a la correcta visualització de l'aplicació. S'ha d'omplir amb la clau privada i guardar-lo com a ".mapbox_token.<br>

