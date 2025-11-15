import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib
import tempfile
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# puis tes classes LoginApp, SignupWindow, etc.


# Nom du fichier utilisateurs
FICHIER_UTILISATEURS = "users.json"

# --- Gestion des utilisateurs  ---

def hash_password(mdp: str) -> str:
    """Retourne le hash SHA-256 hexadécimal du mot de passe."""
    return hashlib.sha256(mdp.encode("utf-8")).hexdigest()

def load_users():
    """Charge la liste d'utilisateurs depuis users.json; renvoie une liste."""
    if not os.path.exists(FICHIER_UTILISATEURS):
        return []
    try:
        with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_users(users):
    """Sauvegarde la liste d'utilisateurs de manière atomique pour éviter corruption."""
    dir_name = os.path.dirname(os.path.abspath(FICHIER_UTILISATEURS)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmpf:
            json.dump(users, tmpf, indent=4, ensure_ascii=False)
            tmpf.flush()
            os.fsync(tmpf.fileno())
        os.replace(tmp_path, FICHIER_UTILISATEURS)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

# --- Vérification d'identifiants  ---

def verifier_identifiants(username, password):
    users = load_users()
    hashed = hash_password(password)
    for u in users:
        if u.get("username") == username and u.get("password") == hashed:
            return True
    return False

# --- Fenêtre d'inscription  ---

class SignupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Créer un compte")
        self.geometry("320x220")
        self.resizable(False, False)

        tk.Label(self, text="Nom d'utilisateur:").pack(pady=(10, 2))
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=2, fill="x", padx=20)

        tk.Label(self, text="Mot de passe:").pack(pady=(8, 2))
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=2, fill="x", padx=20)

        tk.Label(self, text="Confirmer le mot de passe:").pack(pady=(8, 2))
        self.entry_pass_confirm = tk.Entry(self, show="*")
        self.entry_pass_confirm.pack(pady=2, fill="x", padx=20)

        tk.Button(self, text="Créer le compte", command=self.creer_compte).pack(pady=12)

    def creer_compte(self):
        username = self.entry_user.get().strip()
        pwd = self.entry_pass.get()
        pwd_conf = self.entry_pass_confirm.get()

        # validations 
        if not username or not pwd or not pwd_conf:
            messagebox.showerror("Erreur", "Remplis tous les champs.")
            return
        if pwd != pwd_conf:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        users = load_users()
        if any(u.get("username") == username for u in users):
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
            return

        # Ajout du nouvel utilisateur (mot de passe haché)
        users.append({
            "username": username,
            "password": hash_password(pwd)
        })
        try:
            save_users(users)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
            return

        messagebox.showinfo("Succès", "Compte créé avec succès ! Tu peux maintenant te connecter.")
        self.destroy()

# --- Fenêtre de Login principale ---

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion - Gestion Budget")
        self.geometry("320x200")
        self.resizable(False, False)

        tk.Label(self, text="Nom d'utilisateur:").pack(pady=(12, 2))
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=2, fill="x", padx=20)

        tk.Label(self, text="Mot de passe:").pack(pady=(8, 2))
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=2, fill="x", padx=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Se connecter", width=12, command=self.connexion).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Créer un compte", width=12, command=self.open_signup).grid(row=0, column=1, padx=6)

    def open_signup(self):
        SignupWindow(self)

    def connexion(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get()
        if not user or not pwd:
            messagebox.showerror("Erreur", "Remplis tous les champs.")
            return

        if verifier_identifiants(user, pwd):
            messagebox.showinfo("Succès", "Connexion réussie !")
            self.destroy()
         
            try:
                from main import BudgetApp
                app = BudgetApp()
                app.mainloop()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir l'application principale : {e}")
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# --- Lancement ---
if __name__ == "__main__":
    
    if not os.path.exists(FICHIER_UTILISATEURS):
        with open(FICHIER_UTILISATEURS, "w", encoding="utf-8") as f:
            json.dump([], f)

    login = LoginApp()
    login.mainloop()
