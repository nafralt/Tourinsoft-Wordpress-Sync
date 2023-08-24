from Fields.ComposedFields import ComposedFields
from OffreManager import OffreManager
from Fields.Photo import Photo
from config import PHOTOS_PATH
from urllib import request
import glob
import os
import logging

class PhotosManager:

    def __init__(self):
        self.deleted_photos = 0
        self.downloaded_photos = 0
    
    def download_photos(self, offre, slug):
        logging.info("Téléchargement des photos pour %s", slug)
        for data in OffreManager.get_field(offre, ComposedFields.PHOTOS):
            logging.debug("Téléchargement de la photo %s", data[Photo.URL.value])
            request.urlretrieve(data[Photo.URL.value], PHOTOS_PATH+"\\"+slug+"-"+data[Photo.URL.value].replace("http://cdt61.media.tourinsoft.eu/upload/", ""))
            self.downloaded_photos += 1

    def delete_photos(self, slug):
        logging.info("Suppression des photos pour %s", slug)

        # Supprime tous les fichiers commençant par l'id de l'offre (slug Worpress)
        for filename in glob.glob(PHOTOS_PATH+"\\"+slug+"*"):
            logging.debug("Suppression de la photo %s", str(filename))
            os.remove(filename)
            self.deleted_photos += 1

    def log_results(self):
        logging.info("Nombre de photos téléchargées : %s", self.downloaded_photos)
        logging.info("Nombre de photos supprimés : %s", self.deleted_photos)