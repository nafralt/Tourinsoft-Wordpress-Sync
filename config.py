PHOTOS_PATH = ".\img"

LOG_PATH = ".\wp_sync.log"

GEOJSON_PATH = ".\coordonnees.json"

URL_SITE = "https://my.wordpress.website/"

HOST_MYSQL = ""
DB_MYSQL = ""
USER_MYSQL = ""
PASS_MYSQL = ""
TABLE_PREFIX = "wp" # par défaut
AUTHOR_ID = ""

FLUX = {
    "CDH": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/cd667e03-292f-436f-834b-c642b74ffdea", # URL du flux tourinsoft
 
        "categorie": ["chambres-dhotes"],

        "filtre": "Chambres d'hôtes"

    },
    "CHE": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/90c9bf15-9fb7-47de-8b01-03bf07553300",
 
        "categorie": ["nature","plein-air"],

        "filtre": "Loisirs"
    },
    "FMA": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/8c508593-f403-416b-89f9-9eae671ee730",
 
        "categorie": ["agenda"],

        "filtre": "Evènements"
    },
    "HLO": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/a89a2d7f-3f46-4734-8fc9-d569971f9563",
 
        "categorie": ["gites"],

        "filtre": "Gîtes"
    },
    "HOT": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/f786a23c-4223-449c-b994-a963c59bda99",
 
        "categorie": ["hotels"],

        "filtre": "Hôtels"
    },
    "HPA": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/a9860f82-bfe9-407d-821e-20531152e674",
 
        "categorie": ["camping-et-aire-de-camping-car"],

        "filtre": "Camping / Air de camping"
    },
    "LOI": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/32654a43-f89e-41ec-b482-d170239a6682",
 
        "categorie": ["nature"],

        "filtre": "Loisirs"
    },
    "PCU": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/ef98a620-b5f2-43ce-af58-728d4c1abb5c",
 
        "categorie": ["patrimoine"],

        "filtre": "Patrimoine"
    },
    "RES": {
        "url" : "http://wcf.tourinsoft.com/Syndication/cdt61/b1af931e-4221-46c9-a630-9b0352fea8aa",
 
        "categorie": ["se-restaurer"],

        "filtre": "Restaurants"
    }
}
