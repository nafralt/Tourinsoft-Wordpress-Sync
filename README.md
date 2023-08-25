# Tourinsoft Wordpress Synchronisation

Ce module permet la synchronisation des offres de Tourinsoft de l'Orne (61) liés à la Communauté de communes des Pays de L'Aigle sous forme d'articles (création, modification, suppression).
Il permet également l'écriture d'un fichier JSON au format GeoJSON contenant les coordonnées géographiques ainsi que les options de filtrage pour l'intégrer avec le plugin <a href="https://github.com/bozdoz/wp-plugin-leaflet-map">Leaflet Map</a> et <a href="https://github.com/hupe13/extensions-leaflet-map-github/">Extension For Leaflet Map</a>.
Les flux traités sont au format ODATA (Syndication v0.8 Tourinsoft).

# Installation
Requis : Python 3.x

Installation des dépendances :
```bash
pip install requirements.txt
```


Veillez à éditer le fichier "**config.py**" :
```python
PHOTOS_PATH = "" # Chemin du dossier où les photos téléchargées depuis Tourinsoft seront stockés
LOG_PATH = "" # Chemin du fichier à créer pour écrire les logs
GEOJSON_PATH = "" # Chemin du fichier JSON au format GeoJSON à créer
URL_SITE = "" # URL du site internet
HOST_MYSQL = "" # Adresse IP ou nom de domaine
DB_MYSQL = "" # Nom de la base de données Wordpress
USER_MYSQL = "" # Utilisateur MySQL
PASS_MYSQL = "" # Mot de passe MySQL
TABLE_PREFIX = "" # Prefix des tables Wordpress. Exemple : "wp"
AUTHOR_ID = "" # ID de l'utilisateur sur lequel les articles sont attachés

FLUX = {
    "CDH": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/cd667e03-292f-436f-834b-c642b74ffdea", # URL du flux tourinsoft
        "categorie": ["chambres-dhotes"], # Catégories Wordpress (slug) auxquelles les offres seront associées
        "filtre": "Chambres d'hôtes" # Nom du champ lié au filtre GeoJSON
    },
...
```

Exemple de configuration :
```python
PHOTOS_PATH = "/var/www/tourinsoft/img" # Chemin du dossier où les photos téléchargées depuis Tourinsoft seront stockés
LOG_PATH = "/var/www/tourinsoft/log/wp_sync.log" # Chemin du fichier à créer pour écrire les logs
GEOJSON_PATH = "/var/www/tourinsoft/coordonnees.json" # Chemin du fichier JSON au format GeoJSON à créer
URL_SITE = "https://my.wordpress.website/" # URL du site internet
HOST_MYSQL = "256.256.256.256" # Adresse IP ou nom de domaine
DB_MYSQL = "my_wordpress_database" # Nom de la base de données Wordpress
USER_MYSQL = "super_user" # Utilisateur MySQL
PASS_MYSQL = "super_passwd" # Mot de passe MySQL
TABLE_PREFIX = "wp" # Prefix des tables Wordpress. Exemple : "wp"
AUTHOR_ID = "2" # ID de l'utilisateur sur lequel les articles sont attachés

FLUX = {
    "CDH": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/cd667e03-292f-436f-834b-c642b74ffdea", # URL du flux tourinsoft
        "categorie": ["hébergements"], # Catégories Wordpress (slug) auxquelles les offres seront associées
        "filtre": "Hébergements locatifs" # Nom du champ lié au filtre GeoJSON
    },
...
```

# Utilisation

Voir les options de lancement :
```bash
python3 run.py -h
```
```
usage: run.py [-h] [-c {CDH,CHE,FMA,HLO,HOT,HPA,LOI,PCU,RES}] [-l {INFO,DEBUG}]
optional arguments:
  -h, --help            show this help message and exit
  -c {CDH,CHE,FMA,HLO,HOT,HPA,LOI,PCU,RES}, --categorie {CDH,CHE,FMA,HLO,HOT,HPA,LOI,PCU,RES}
                        Lance le programme sur la catégorie d'offres choisie. Par défaut, le programme s'exécute sur
                        toutes les catégories.
  -l {INFO,DEBUG}, --log {INFO,DEBUG}
                        Définit le niveau des logs. Par défaut, le niveau des logs est INFO.
```
