# Programme de création des classes et de la base de données
import sqlite3
from datetime import datetime, timedelta

# Fonction pour créer la base de données et les tables
def creer_base_donnees():
    conn = sqlite3.connect("gestion_presence.db")
    cursor = conn.cursor()
    
    # Suppression des tables existantes si elles existent
    cursor.execute('DROP TABLE IF EXISTS Etudiants')
    cursor.execute('DROP TABLE IF EXISTS Sessions')
    cursor.execute('DROP TABLE IF EXISTS Presences')
    
    # Création de la table des étudiants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Etudiants (
            id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            heure_arrivee DATETIME NOT NULL
        )
    ''')
    
    # Création de la table des sessions de cours
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sessions (
            id_session INTEGER PRIMARY KEY AUTOINCREMENT,
            classe TEXT NOT NULL,
            matiere TEXT NOT NULL,
            heure_debut DATETIME NOT NULL,
            heure_fin DATETIME NOT NULL
        )
    ''')
    
    # Création de la table des présences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Presences (
            id_presence INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            id_session INTEGER NOT NULL,
            statut TEXT NOT NULL,
            heure_arrivee DATETIME NOT NULL,
            FOREIGN KEY (id_etudiant) REFERENCES Etudiants(id_etudiant),
            FOREIGN KEY (id_session) REFERENCES Sessions(id_session)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données et tables créées avec succès.")

# Appeler la fonction pour créer la base de données et les tables
creer_base_donnees()

# Classe Etudiant pour gérer les informations des étudiants
class Etudiant:
    def __init__(self, nom, prenom, classe, heure_arrivee):
        self.nom = nom
        self.prenom = prenom
        self.classe = classe
        self.heure_arrivee = heure_arrivee

    def ajouter_etudiant(self):
        conn = sqlite3.connect("gestion_presence.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Etudiants (nom, prenom, classe, heure_arrivee) VALUES (?, ?, ?, ?)
        ''', (self.nom, self.prenom, self.classe, self.heure_arrivee))
        
        conn.commit()
        conn.close()
        print(f"Étudiant {self.nom} {self.prenom} arrivé à {self.heure_arrivee} ajouté avec succès.")

    @staticmethod
    def ajouter_nouvel_etudiant():
        nom = input("Entrez le nom de l'étudiant : ")
        prenom = input("Entrez le prénom de l'étudiant : ")
        classe = input("Entrez la classe de l'étudiant (ISE1, ISE2, ISE3) : ")
        heure_arrivee = datetime.now()  # Supposons l'heure d'arrivée comme étant l'heure actuelle

        nouvel_etudiant = Etudiant(nom, prenom, classe, heure_arrivee)
        nouvel_etudiant.ajouter_etudiant()

# Classe SessionCours pour gérer les informations des sessions de cours
class SessionCours:
    def __init__(self, classe, matiere, heure_debut, heure_fin):
        self.classe = classe
        self.matiere = matiere
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin

    def ajouter_session(self):
        conn = sqlite3.connect("gestion_presence.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Sessions (classe, matiere, heure_debut, heure_fin) VALUES (?, ?, ?, ?)
        ''', (self.classe, self.matiere, self.heure_debut, self.heure_fin))
        
        conn.commit()
        conn.close()
        print(f"Session pour {self.classe} de {self.matiere} qui commence à {self.heure_debut} et prend fin à {self.heure_fin} ajoutée avec succès.")

    @staticmethod
    def ajouter_sessions_journee():
        classe = input("Entrez la classe (ISE1, ISE2, ISE3) pour laquelle ajouter les sessions : ")
        ajouter_autre = "oui"
        
        while ajouter_autre.lower() == "oui":
            matiere = input("Veuillez entrer la matière : ")
            heure_debut_str = input("Entrez l'heure de début du cours (format HH:MM) : ")
            heure_fin_str = input("Entrez l'heure de fin du cours (format HH:MM) : ")
            # Convertir les entrées en objets datetime
            date_aujourdhui = datetime.now().date()  # Utilisation de la date actuelle pour les sessions du jour
            heure_debut = datetime.strptime(f"{date_aujourdhui} {heure_debut_str}", "%Y-%m-%d %H:%M")
            heure_fin = datetime.strptime(f"{date_aujourdhui} {heure_fin_str}", "%Y-%m-%d %H:%M")
            
            nouvelle_session = SessionCours(classe, matiere, heure_debut, heure_fin)
            nouvelle_session.ajouter_session()
            
            ajouter_autre = input("Souhaitez-vous ajouter une autre session pour aujourd'hui ? (oui/non) : ")

# Classe GestionPresence pour gérer la présence et le retard des étudiants
class GestionPresence:
    def __init__(self):
        self.conn = sqlite3.connect("gestion_presence.db")
        self.cursor = self.conn.cursor()

    def enregistrer_arrivee(self, id_etudiant, id_session, heure_arrivee):
        # Récupération des informations de la session
        self.cursor.execute('SELECT heure_debut FROM Sessions WHERE id_session = ?', (id_session,))
        result = self.cursor.fetchone()
        
        if not result:
            print("Session introuvable.")
            return
        
        heure_debut = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        # Définir le statut en fonction de l'heure d'arrivée
        if heure_arrivee <= heure_debut:
            statut = "Présent"
        elif heure_debut < heure_arrivee <= (heure_debut + timedelta(minutes=0)):  # Par exemple, aucun retard n'est autorisé
            statut = "En retard"
        else:
            statut = "Absent"
        # Enregistrer dans la base de données
        self.cursor.execute('''
            INSERT INTO Presences (id_etudiant, id_session, statut, heure_arrivee)
            VALUES (?, ?, ?, ?)
        ''', (id_etudiant, id_session, statut, heure_arrivee))
        
        self.conn.commit()
        print(f"Arrivée enregistrée pour l'étudiant {id_etudiant} : {statut} à {heure_arrivee}.")

    def fermer_connexion(self):
        self.conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    print("Options disponibles :")
    print("1. Ajouter un nouvel étudiant")
    print("2. Ajouter les sessions de cours pour la journée")
    choix = input("Entrez votre choix (1/2) : ")
    if choix == "1":
        Etudiant.ajouter_nouvel_etudiant()
    elif choix == "2":
        SessionCours.ajouter_sessions_journee()
    else:
        print("Choix non valide.")
