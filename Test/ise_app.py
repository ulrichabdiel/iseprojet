import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import sqlite3
from datetime import datetime

# Fonction pour créer la base de données et les tables en utilisant le fichier SQL
def creer_base_donnees():
    conn = sqlite3.connect("taches.db")
    cursor = conn.cursor()
    
    # Lire et exécuter le fichier SQL
    with open("tache.sql", "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    print("Base de données et tables créées avec succès.")

# Classe Etudiant pour gérer les informations des étudiants
class Etudiant:
    def __init__(self, nom, prenom, classe, heure_arrivee):
        self.nom = nom
        self.prenom = prenom
        self.classe = classe
        self.heure_arrivee = heure_arrivee

    def ajouter_etudiant(self):
        conn = sqlite3.connect("taches.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Etudiants (nom, prenom, classe, heure_arrivee) VALUES (?, ?, ?, ?)
        ''', (self.nom, self.prenom, self.classe, self.heure_arrivee))
        
        conn.commit()
        conn.close()
        print(f"Étudiant {self.nom} {self.prenom} arrivé à {self.heure_arrivee} ajouté avec succès.")
        messagebox.showinfo("Succès", f"Étudiant {self.nom} {self.prenom} ajouté avec succès.")

    @staticmethod
    def ajouter_nouvel_etudiant():
        def submit():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            classe = entry_classe.get()
            heure_arrivee = datetime.now()  # Supposons l'heure d'arrivée comme étant l'heure actuelle

            nouvel_etudiant = Etudiant(nom, prenom, classe, heure_arrivee)
            nouvel_etudiant.ajouter_etudiant()
            window.destroy()

        window = tk.Tk()
        window.title("Ajouter un nouvel étudiant")

        tk.Label(window, text="Nom").grid(row=0)
        tk.Label(window, text="Prénom").grid(row=1)
        tk.Label(window, text="Classe").grid(row=2)

        entry_nom = tk.Entry(window)
        entry_prenom = tk.Entry(window)
        entry_classe = tk.Entry(window)

        entry_nom.grid(row=0, column=1)
        entry_prenom.grid(row=1, column=1)
        entry_classe.grid(row=2, column=1)

        tk.Button(window, text='Soumettre', command=submit).grid(row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(window, text='Quitter', command=window.quit).grid(row=3, column=1, sticky=tk.W, pady=4)

        window.mainloop()

# Classe SessionCours pour gérer les informations des sessions de cours
class SessionCours:
    def __init__(self, classe, matiere, heure_debut, heure_fin):
        self.classe = classe
        self.matiere = matiere
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin

    def ajouter_session(self):
        conn = sqlite3.connect("taches.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Sessions (classe, matiere, heure_debut, heure_fin) VALUES (?, ?, ?, ?)
        ''', (self.classe, self.matiere, self.heure_debut, self.heure_fin))
        
        conn.commit()
        conn.close()
        print(f"Session pour {self.classe} de {self.matiere} qui commence à {self.heure_debut} et prend fin à {self.heure_fin} ajoutée avec succès.")
        messagebox.showinfo("Succès", f"Session de {self.matiere} ajoutée avec succès.")

    @staticmethod
    def ajouter_session_responsable():
        def submit():
            mot_de_passe = entry_mdp.get()
            if mot_de_passe == "admin123":  # Mot de passe du responsable
                classe = entry_classe.get()
                matiere = entry_matiere.get()
                # Boucle pour s'assurer que l'utilisateur entre les heures correctes
                try:
                    heure_debut_str = entry_heure_debut.get()
                    heure_fin_str = entry_heure_fin.get()

                    # Convertir les entrées en objets datetime
                    date_aujourdhui = datetime.now().date()  # Utilisation de la date actuelle pour les sessions du jour
                    heure_debut = datetime.strptime(f"{date_aujourdhui} {heure_debut_str}", "%Y-%m-%d %H:%M")
                    heure_fin = datetime.strptime(f"{date_aujourdhui} {heure_fin_str}", "%Y-%m-%d %H:%M")

                    nouvelle_session = SessionCours(classe, matiere, heure_debut, heure_fin)
                    nouvelle_session.ajouter_session()
                    window.destroy()
                except ValueError:
                    messagebox.showerror("Erreur", "Format de l'heure incorrect. Veuillez réessayer.")
            else:
                messagebox.showerror("Erreur", "Mot de passe incorrect. Accès refusé.")
        
        window = tk.Tk()
        window.title("Ajouter une session de cours")

        tk.Label(window, text="Mot de passe").grid(row=0)
        tk.Label(window, text="Classe").grid(row=1)
        tk.Label(window, text="Matière").grid(row=2)
        tk.Label(window, text="Heure de début (HH:MM)").grid(row=3)
        tk.Label(window, text="Heure de fin (HH:MM)").grid(row=4)

        entry_mdp = tk.Entry(window, show='*')
        entry_classe = tk.Entry(window)
        entry_matiere = tk.Entry(window)
        entry_heure_debut = tk.Entry(window)
        entry_heure_fin = tk.Entry(window)

        entry_mdp.grid(row=0, column=1)
        entry_classe.grid(row=1, column=1)
        entry_matiere.grid(row=2, column=1)
        entry_heure_debut.grid(row=3, column=1)
        entry_heure_fin.grid(row=4, column=1)

        tk.Button(window, text='Soumettre', command=submit).grid(row=5, column=0, sticky=tk.W, pady=4)
        tk.Button(window, text='Quitter', command=window.quit).grid(row=5, column=1, sticky=tk.W, pady=4)

        window.mainloop()

# Exemple d'utilisation
if __name__ == "__main__":
    creer_base_donnees()  # Assurez-vous que cette fonction est appelée pour créer les tables

    root = tk.Tk()
    root.title("Gestion des présences")

    tk.Label(root, text="Options disponibles :").grid(row=0, column=0)
    tk.Button(root, text="Ajouter un nouvel étudiant", command=Etudiant.ajouter_nouvel_etudiant).grid(row=1, column=0, sticky=tk.W, pady=4)
    tk.Button(root, text="Ajouter une session de cours (réservé au responsable)", command=SessionCours.ajouter_session_responsable).grid(row=2, column=0, sticky=tk.W, pady=4)
    tk.Button(root, text="Quitter", command=root.quit).grid(row=3, column=0, sticky=tk.W, pady=4)

    root.mainloop()
