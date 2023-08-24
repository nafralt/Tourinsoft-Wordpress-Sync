from OffreManager import OffreManager
from config import FLUX


if __name__ == '__main__':
    for id_flux,infos in FLUX.items():
        offre_manager = OffreManager(infos["url"], id_flux)
        print("Pour le flux "+id_flux+" : ")
        offre_manager.show_fields()
        print("---------------------------")