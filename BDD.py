import MySQLdb
from config import HOST_MYSQL,USER_MYSQL,PASS_MYSQL,DB_MYSQL,TABLE_PREFIX, AUTHOR_ID
import logging

class BDD:

    def __init__(self):
        logging.debug("Création de la connexion à la base de données")
        self.nombreNouvelArticle = 0
        self.nombreMAJArticle = 0
        self.nombreArticleDeleted = 0
        self.nombreImageDeleted = 0
        self.nombreImageAjoute = 0
        self.prefix = TABLE_PREFIX
        try:
            self.db = MySQLdb.connect(HOST_MYSQL,USER_MYSQL,PASS_MYSQL,DB_MYSQL, charset="utf8mb4")
            self.db.autocommit(True)
        except MySQLdb.Error as err:
            logging.critical(err)
            exit(-1)

    def get_post_id(self, slug):
        logging.debug("Récupération de l'id du post %s", slug)
        req = "SELECT id FROM "+self.prefix+"_posts WHERE post_name = %s AND post_type = 'post'"
        params = (slug,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]
    
    def get_relationship_post_to_term_count(self, post_id):
        logging.debug("Récupération du nombre de relations du post avec l'id %s", post_id)
        req = "SELECT count(*) FROM "+self.prefix+"_term_relationships WHERE object_id = %s"
        params = (post_id,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]
    
    def get_slug_post(self, post_id):
        logging.debug("Récupération du slug d'un post à partir de l'id %s", post_id)
        req = "SELECT post_name FROM "+self.prefix+"_posts WHERE id = %s"
        params = (post_id,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]
    
    def is_tourinsoft_post(self, post_id):
        logging.debug("Check si l'offre fait partie des flux tourinsoft")
        slug = self.get_slug_post(post_id)
        return slug.startswith(("RESNOR", "PCUNOR", "HOTNOR", "LOINOR", "HLONOR", "HPANOR", "FMANOR"))

    def insert_post(self, contenu, titre, extrait, slug):
        logging.debug("Insertion dans la base des données : %s %s %s %s", contenu, titre, extrait, slug)
        params = (contenu, titre, extrait, slug)
        req = "INSERT INTO "+self.prefix+"_posts (post_date, post_author, post_content, post_title, post_excerpt, post_name, post_modified, post_password, to_ping, pinged, post_content_filtered) VALUES (NOW(), "+str(AUTHOR_ID)+", %s, %s, %s, %s, NOW(), '', '', '', '')"
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        self.nombreNouvelArticle += 1
        return mycursor
    
    def insert_meta_date(self, post_id, date):
        logging.debug("Insertion dans la base de %s dans le champ meta pour l'article avec l'id %s", date, post_id)
        params = (post_id, date)
        req = "INSERT INTO "+self.prefix+"_postmeta (post_id, meta_key, meta_value) VALUES (%s, 'wp_event_date', %s)"
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor
    
    def update_meta_date(self, post_id, date):
        logging.debug("Mise à jour dans la base du champ meta avec %s pour l'article avec l'id %s", date, post_id)
        params = (date, post_id)
        req = "UPDATE "+self.prefix+"_postmeta SET meta_value = %s where post_id = %s"
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor
    
    def delete_meta_date(self, post_id):
        logging.debug("Suppression du champ meta pour l'article avec l'id %s", post_id)
        params = (post_id,)
        req = "DELETE FROM "+self.prefix+"_postmeta where post_id = %s"
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor
    
    def already_in_database(self, slug):
        if self.get_posts_count(slug) > 0:
            return True
        else:
            return False
        
    def already_linked(self, post_id, term_id):
        logging.debug("Regarde si le post avec l'id %s est déjà lié au term avec l'id %s", post_id, term_id)
        req = "SELECT count(*) FROM "+self.prefix+"_term_relationships WHERE object_id = %s AND term_taxonomy_id = (SELECT term_taxonomy_id FROM "+self.prefix+"_term_taxonomy WHERE term_id = %s)"
        params = (post_id, term_id)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        if mycursor.fetchone()[0] > 0:
            return True
        else:
            return False
    
    def get_term_id(self, categorie):
        logging.debug("Récupération de l'id du term %s", categorie)
        req = "SELECT term_id FROM "+self.prefix+"_terms WHERE slug = %s LIMIT 1"
        params = (categorie,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]
    
    def insert_term_relationship(self, post_id, term_id):
        logging.debug("Insertion de la relation entre le post avec l'id %s et le term avec l'id %s", post_id, term_id)
        req = "INSERT INTO "+self.prefix+"_term_relationships (object_id, term_taxonomy_id) VALUES (%s, (SELECT term_taxonomy_id FROM "+self.prefix+"_term_taxonomy WHERE term_id = %s))"
        params = (post_id, term_id)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor
    
    def get_posts_id_of_category(self, term_id):
        logging.debug("Récupération des id des posts liés au term avec l'id %s", term_id)
        req = "SELECT object_id FROM "+self.prefix+"_term_relationships WHERE term_taxonomy_id = (SELECT term_taxonomy_id FROM "+self.prefix+"_term_taxonomy WHERE term_id = %s)"
        params = (term_id,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor
        
    def delete_term_relationship(self, post_id, term_id):
        logging.debug("Suppression du lien entre le post avec l'id %s et le term avec l'id %s", post_id, term_id)
        req = "DELETE FROM "+self.prefix+"_term_relationships WHERE object_id = %s AND term_taxonomy_id = (SELECT term_taxonomy_id FROM "+self.prefix+"_term_taxonomy WHERE term_id = %s)"
        params = (post_id, term_id)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor

    def get_posts_count(self, slug):
        logging.debug("Récupération du nombre de posts ayant pour slug %s", slug)
        req = "SELECT count(*) FROM "+self.prefix+"_posts where post_name = %s AND post_type = 'post'"
        params = (slug,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]
    
    def get_modification_date(self, post_id):
        logging.debug("Récupération de la date de la dernière modification du post avec l'id %s", post_id)
        req = "SELECT post_modified FROM "+self.prefix+"_posts WHERE id = %s AND post_type = 'post'"
        params = (post_id,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        return mycursor.fetchone()[0]

    def update_post(self, contenu, titre, extrait, post_id):
        logging.debug("Update dans la base des données : %s %s %s %s", contenu, titre, extrait, post_id)
        params = (contenu, titre, extrait, post_id)
        req = "UPDATE "+self.prefix+"_posts SET post_content = %s, post_title = %s, post_excerpt = %s, post_modified = NOW() WHERE id = %s"
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        self.nombreMAJArticle += 1
        return mycursor

    def delete_post(self, post_id):
        logging.debug("Suppression dans la base des données : %s ",post_id)
        req = "DELETE FROM "+self.prefix+"_posts WHERE id = %s"
        params = (post_id,)
        mycursor = self.db.cursor()
        mycursor.execute(req, params)
        self.nombreArticleDeleted += 1
        return mycursor

    def close(self):
        logging.debug("Fermeture de la connexion à la base de données")
        try:
            self.db.close()
        except Exception as err:
            logging.error(err)

        logging.info("Nombre d'articles ajoutés : %s", self.nombreNouvelArticle)
        logging.info("Nombre d'articles mis à jour : %s", self.nombreMAJArticle)
        logging.info("Nombre d'articles supprimés : %s", self.nombreArticleDeleted)

if __name__ == '__main__':
    db = BDD()
