from OffreManager import OffreManager
import logging
from BDD import BDD
from config import URL_SITE, GEOJSON_PATH
from Fields.SingleFields import SingleFields
from Fields.ComposedFields import ComposedFields
from Fields.PeriodeOuverture import PeriodeOuverture
from PhotosManager import PhotosManager
from mako.template import Template
import json


class App:

    @staticmethod
    def run(flux):
        
        logging.debug("Lancement de la boucle de récupération des offres")
        db = BDD()
        photos_manager = PhotosManager()

        
        json_file = open(GEOJSON_PATH, "w+", encoding='utf8')

        # Debut du fichier JSON au format GeoJSON
        data_json = {
            "type": "FeatureCollection",
            "features": []
        }

        # Liste des offres traitées dans les flux
        processed_offres = []

        try:
            template_extrait = Template(filename=f'./templates/extrait.html')
            # Boucle pour itérer sur chaque flux tourinsoft
            for id_flux,infos in flux.items():
                offre_manager = OffreManager(infos["url"], id_flux)
                offre_manager.load_offres()
                term_ids = []
                for categorie in infos["categorie"]:
                    term_ids.append(db.get_term_id(categorie))

                template_content = Template(filename=f'./templates/{id_flux}_template.html')


                # Boucle pour itérer sur les offres du flux
                for offre in offre_manager.get_offres():

                    # Si on est dans le flux des gites/chambre d'hôtes et que la classification de l'offre est "Chambre d'hôtes", alors on ne la traite pas
                    if id_flux == "HLO" and offre_manager.get_field(offre, ComposedFields.CLASSIFICATION)[0][0] == "Chambre d'hôtes":
                        continue

                    post_slug = offre_manager.get_field(offre, SingleFields.ID)

                    # Si l'offre n'est pas dans la base de données, on le créé
                    if not db.already_in_database(post_slug):
                        contenu = template_content.render(offre=offre)
                        extrait = template_extrait.render(offre=offre)
                        db.insert_post(contenu, offre_manager.get_field(offre, SingleFields.NOM_OFFRE), extrait, post_slug)
                        post_id = db.get_post_id(post_slug)

                        # Insertion des relations de catégories
                        for term_id in term_ids:
                            db.insert_term_relationship(post_id, term_id)
                        
                        photos_manager.download_photos(offre, post_slug)

                        # Si l'offre est un événement, alors on récupère sa date de début pour l'insérer dans la table des métadonnées
                        if id_flux == "FMA":
                            # Formatage de la date. Exemple : 28/02/2023 vers 20230228
                            date = offre_manager.get_field(offre, ComposedFields.PERIODE_OUVERTURE)
                            date = date[0][PeriodeOuverture.DATE_DEBUT.value].split('/')
                            date = str(date[2]+date[1]+date[0])
                            db.insert_meta_date(post_id, date)

                        processed_offres.append(post_id)

                    else:
                        # L'offre n'est pas dans la base

                        post_id = db.get_post_id(post_slug)
                        date_updated_offre = offre_manager.get_field(offre, SingleFields.UPDATED)

                        # Si l'offre doit être mis à jour, alors le fait dans la base
                        if db.get_modification_date(post_id).replace(tzinfo=date_updated_offre.tzinfo) < date_updated_offre: # tzinfo permet de spécifier la timezone pour une date (timezone différent des flux tourinsoft et de la bdd)
                            contenu = template_content.render(offre=offre)
                            extrait = template_extrait.render(offre=offre)
                            db.update_post(contenu, offre_manager.get_field(offre, SingleFields.NOM_OFFRE), extrait, post_id)
                            photos_manager.download_photos(offre, post_slug)
                            if id_flux == "FMA":
                                date = offre_manager.get_field(offre, ComposedFields.PERIODE_OUVERTURE)
                                date = date[0][PeriodeOuverture.DATE_DEBUT.value].split('/')
                                date = str(date[2]+date[1]+date[0])
                                db.update_meta_date(post_id, date)

                        # On ajoute des liens de l'offre à ses catégories dans le cas où le fichier config a été édité
                        for term_id in term_ids:
                            if not db.already_linked(post_id, term_id):
                                db.insert_term_relationship(post_id, term_id)
                        processed_offres.append(post_id)

                    # Création de l'objet geojson d'une offre pour le faire apparaitre sur la carte intéractive
                    geojson_object = {
                        "type": "Feature",
                        "properties": {
                            "categorie": infos['filtre'],
                            "nom": offre_manager.get_field(offre, SingleFields.NOM_OFFRE),
                            "url": '<a href="'+URL_SITE+post_slug+'">Consulter l\'article</a>',
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                offre_manager.get_field(offre, SingleFields.GOOGLE_MAP_LONGITUDE),
                                offre_manager.get_field(offre, SingleFields.GOOGLE_MAP_LATITUDE)
                            ]
                        },
                    }
                    data_json["features"].append(geojson_object)

        except Exception as e:
            logging.critical(str(e))
            print(str(e))
            exit(-1)
        
        # On retire les offres qui sont dans la bdd mais pas dans les flux
        logging.info("Suppression des offres ne se trouvant plus dans les flux")
        for infos in flux.values():
            term_ids = []
            for categorie in infos["categorie"]:
                term_ids.append(db.get_term_id(categorie))

            # Pour chaque catégorie liée à un flux, on récupére tous les articles
            for term_id in term_ids:
                cursor = db.get_posts_id_of_category(term_id)
                while True:
                    post_id_db = cursor.fetchone()
                    if post_id_db is None:
                        break
                    post_id_db = post_id_db[0]
                    # Si l'article récupéré est une offre de tourinsoft et n'est pas dans les flux traités, alors on le supprime
                    if db.is_tourinsoft_post(post_id_db) and post_id_db not in processed_offres:
                        db.delete_term_relationship(post_id_db, term_id)
                        if db.get_relationship_post_to_term_count(post_id_db) < 1:
                            post_slug = db.get_slug_post(post_id)
                            photos_manager.delete_photos(post_slug)
                            db.delete_meta_date(post_id_db)
                            db.delete_post(post_id_db)

        # Ecriture des objets GeoJSON
        json.dump(data_json, json_file, ensure_ascii=False)
        json_file.close()
        db.close()
        photos_manager.log_results()