import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
from config import LOG_PATH, FLUX
from App import App

def get_args():

    global LOG_PATH, FLUX

    # Définition des arguments possibles au lancement du programme
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--categorie", 
        type=str, 
        choices=FLUX.keys(), default="ALL",
        help="Lance le programme sur la catégorie d'offres choisie. Par défaut, le programme s'exécute sur toutes les catégories."
    )

    parser.add_argument(
        "-l",
        "--log",
        type=str,
        choices=["INFO", "DEBUG"], default="INFO",
        help="Définit le niveau des logs. Par défaut, le niveau des logs est INFO."
    )

    args = parser.parse_args()

    if args.categorie != "ALL":
        FLUX = {args.categorie : FLUX[args.categorie]}

    handler = TimedRotatingFileHandler(LOG_PATH, when="d", interval=1, backupCount=30, encoding='utf-8') # Création d'un fichier log par jour et ne garde que les 30 fichiers logs les plus récents
    logging.basicConfig(level=args.log, format='%(asctime)s -> %(levelname)s: %(message)s', datefmt='%I:%M:%S %p', handlers=[handler]) # Configuration du format de sortie des logs 


if __name__ == "__main__":
    get_args()
    logging.info("Lancement du programme")
    App.run(FLUX)
    logging.info("Fin du programme")