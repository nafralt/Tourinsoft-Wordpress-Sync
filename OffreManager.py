from Fields.SingleFields import SingleFields
import pyodata
import requests
import logging

class OffreManager:

    def __init__(self, url, categorie):
        self.url = url # URL tourinsoft depuis lequel on charge les offres
        self.categorie = categorie # Catégorie des offres chargées
        self.offres = [] # Liste des offres

    def get_categorie(self):
        return self.categorie
    
    def get_offres(self):
        return self.offres

    # Montre le nom des champs utilisé par la catégorie de flux tourinsoft associé à OffreManager
    def show_fields(self):
        logging.debug("Récupération du nom des champs de la catégorie %s", self.categorie)
        champs = []

        try:
            HTTP_LIB = requests.Session()
            data = pyodata.Client(self.url, HTTP_LIB)
            champs = data.entity_sets.Fields.get_entities().execute()

            for champ in champs:
                print(champ.SyndicFieldName)

        except Exception as err:
            logging.critical(err)
            print(str(err))
            raise Exception("ERREUR : Impossible de récupérer les champs")

    # Charge la liste des offres
    def load_offres(self):
        logging.debug("Chargement des offres de la catégorie %s", self.categorie)
        try:
            HTTP_LIB = requests.Session()
            data = pyodata.Client(self.url, HTTP_LIB)
            self.offres = data.entity_sets.Objects.get_entities().execute()
        except Exception as err:
            logging.critical(err)
            print(str(err))
            self.offres = []
            raise Exception("ERREUR : Impossible de charger les offres")


    @staticmethod
    def is_empty(offre, field):
        logging.debug("Vérification si le champ spécifié est contenu dans l'offre")
        try:
            if type(field) == SingleFields:
                if len(getattr(offre, field.value)) == 0:
                    return True
                return False
            else:
                res_objects = []
                champ = ""
                champ = getattr(offre, field.value)
                if len(champ) > 0:
                    objects = champ.split("#")
                    if len(objects) > 0:
                        for object in objects:
                            if len(object) > 0:
                                infos = object.split("|")
                                if len(infos) > 0:
                                    res_objects.append(infos)
                                else :
                                    res_objects.append(object)
                if len(res_objects) == 0:
                    return True
                return False
        except Exception as err:
            logging.WARNING(err)
            return True

    # Retourne une liste de tableau contenant les informations formattées d'un champ d'une offre.
    # Exemple : ModesPaiements = "Cartes de paiement#Espèces#Chèques", résultat  = [["Cartes de paiements"],["Espèces"], ["Chèques"]]
    @staticmethod
    def get_field(offre, field):
        logging.debug("Récupération du champ %s", field.value)
        try:
            if type(field) == SingleFields:
                return getattr(offre, field.value)
            else:
                res_objects = []
                champ = ""
                champ = getattr(offre, field.value)
                if len(champ) > 0:
                    objects = champ.split("#")
                    if len(objects) > 0:
                        for object in objects:
                            if len(object) > 0:
                                infos = object.split("|")
                                if len(infos) > 0:
                                    res_objects.append(infos)
                                else :
                                    res_objects.append(object)

                return res_objects
        except Exception as err:
            logging.WARNING(err)
            return ""

