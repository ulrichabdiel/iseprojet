import sqlite3
from tkinter import Tk, Label, Button, Entry, Toplevel, messagebox
from tkinter.ttk import Notebook, Frame
import face_recognition
import cv2
from datetime import datetime


# Fonction pour créer une connexion à la base de données
def get_connection():
    return sqlite3.connect("gestion_presence.db")


# Classe principale de l'application
class GestionPresenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Présence et Retard des Étudiants ISE")
        
        # Onglets
        self.tabs = Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")
        
        # Onglet pour enregistrer les étudiants
        self.register_student_tab = Frame(self.tabs)
        self.tabs.add(self.register_student_tab, text="Enregistrer Étudiants")
        self.create_register_student_tab()
        
        # Onglet pour enregistrer les présences et retards
        self.attendance_tab = Frame(self.tabs)
        self.tabs.add(self.attendance_tab, text="Enregistrer Présences")
        self.create_attendance_tab()
        
        # Onglet pour la reconnaissance faciale
        self.face_recognition_tab = Frame(self.tabs)
        self.tabs.add(self.face_recognition_tab, text="Reconnaissance Faciale")
        self.create_face_recognition_tab()
        
        # Onglet pour générer les rapports
        self.report_tab = Frame(self.tabs)
        self.tabs.add(self.report_tab, text="Générer Rapports")
        self.create_report_tab()
        
    # 1. Onglet pour enregistrer les informations des étudiants
    def create_register_student_tab(self):
        Label(self.register_student_tab, text="Nom:").grid(row=0, column=0)
        self.nom_entry = Entry(self.register_student_tab)
        self.nom_entry.grid(row=0, column=1)
        
        Label(self.register_student_tab, text="Prénom:").grid(row=1, column=0)
        self.prenom_entry = Entry(self.register_student_tab)
        self.prenom_entry.grid(row=1, column=1)
        
        Label(self.register_student_tab, text="Classe:").grid(row=2, column=0)
        self.classe_entry = Entry(self.register_student_tab)
        self.classe_entry.grid(row=2, column=1)
        
        Button(self.register_student_tab, text="Enregistrer Étudiant", command=self.save_student).grid(row=3, column=0, columnspan=2)

    def save_student(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        classe = self.classe_entry.get()
        
        if not (nom and prenom and classe):
            messagebox.showwarning("Validation", "Veuillez remplir tous les champs.")
            return
        
        cursor.execute("INSERT INTO Etudiants (nom, prenom, classe) VALUES (?, ?, ?)", (nom, prenom, classe))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Succès", f"Étudiant {nom} {prenom} ajouté avec succès.")
        self.nom_entry.delete(0, 'end')
        self.prenom_entry.delete(0, 'end')
        self.classe_entry.delete(0, 'end')

    # 2. Onglet pour enregistrer les présences et retards
    def create_attendance_tab(self):
        Label(self.attendance_tab, text="ID Étudiant:").grid(row=0, column=0)
        self.student_id_entry = Entry(self.attendance_tab)
        self.student_id_entry.grid(row=0, column=1)
        
        Label(self.attendance_tab, text="ID Session:").grid(row=1, column=0)
        self.session_id_entry = Entry(self.attendance_tab)
        self.session_id_entry.grid(row=1, column=1)
        
        Button(self.attendance_tab, text="Enregistrer Présence", command=self.record_attendance).grid(row=2, column=0, columnspan=2)

    def record_attendance(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        student_id = self.student_id_entry.get()
        session_id = self.session_id_entry.get()
        heure_arrivee = datetime.now()
        
        # Statut de l'étudiant en fonction de l'heure d'arrivée
        cursor.execute("SELECT heure_debut FROM Sessions WHERE id_session = ?", (session_id,))
        result = cursor.fetchone()
        
        if result:
            heure_debut = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
            statut = "Présent" if heure_arrivee <= heure_debut else "En retard"
            cursor.execute("INSERT INTO Presences (id_etudiant, id_session, statut, heure_arrivee) VALUES (?, ?, ?, ?)", (student_id, session_id, statut, heure_arrivee))
            conn.commit()
            messagebox.showinfo("Succès", f"Présence enregistrée : {statut}")
        else:
            messagebox.showerror("Erreur", "Session introuvable")
        
        conn.close()

    # 3. Onglet pour la reconnaissance faciale
    def create_face_recognition_tab(self):
        Label(self.face_recognition_tab, text="Lancer la reconnaissance faciale").pack()
        Button(self.face_recognition_tab, text="Démarrer", command=self.start_face_recognition).pack()

    def start_face_recognition(self):
        # Démarrage de la webcam et utilisation de face_recognition pour identifier les étudiants
        video_capture = cv2.VideoCapture(0)
        
        while True:
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for face_encoding in face_encodings:
                # Comparer avec les visages enregistrés dans la base de données
                # Logique de reconnaissance faciale à implémenter ici
                
                # Pour ce prototype, on suppose une correspondance trouvée
                messagebox.showinfo("Reconnaissance", "Étudiant reconnu.")
                video_capture.release()
                cv2.destroyAllWindows()
                return

            cv2.imshow("Reconnaissance Faciale", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    # 4. Onglet pour générer des rapports de présence
    def create_report_tab(self):
        Button(self.report_tab, text="Générer le Rapport", command=self.generate_report).pack()

    def generate_report(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''SELECT E.nom, E.prenom, S.classe, P.statut, P.heure_arrivee
                          FROM Presences P
                          JOIN Etudiants E ON P.id_etudiant = E.id_etudiant
                          JOIN Sessions S ON P.id_session = S.id_session
                          ORDER BY S.classe, P.heure_arrivee''')
        rows = cursor.fetchall()
        report_text = "\n".join([f"{nom} {prenom} ({classe}): {statut} à {heure_arrivee}" for nom, prenom, classe, statut, heure_arrivee in rows])
        report_window = Toplevel(self.root)
        report_window.title("Rapport de Présence")
        Label(report_window, text=report_text).pack()
        
        conn.close()


# Exécution de l'application
root = Tk()
app = GestionPresenceApp(root)
root.mainloop()
