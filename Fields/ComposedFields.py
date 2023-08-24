from enum import Enum

# Champ tourinsoft identifié en tant que champ composé.
# Exemples : <value>#<value>#<value>... , <value-1-1>|<value-1-2>|<value-1-3>#<value-2-1>|<value-2-2>|<value-2-3>...
class ComposedFields(Enum):

    # constantes ayant pour valeur les clés pour accéder à l'attribut

    TARIFS = "Tarifs"
    MODES_PAIEMENTS = "ModesPaiements"
    HANDICAP = "Handicap"
    PERIODE_OUVERTURE = "PeriodeOuverture"
    PHOTOS = "Photos"
    MOYEN_DE_COM = "MoyenDeCom"
    PRESTATIONS_CONFORTS = "PrestationsConforts"
    PRESTATIONS_EQUIPEMENTS = "PrestationsEquipements"
    PRESTATIONS_ACTIVITES = "PrestationsActivites"
    PRESTATIONS_SERVICES = "PrestationsServices"
    CLASSIFICATION3 = "Classification3"
    CLASSIFICATION = "Classification"
    CLASSIFICATION2 = "Classification2"
    CHAINES = "Chaines"
    LABELS = "Labels"
