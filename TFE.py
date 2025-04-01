from tkinter import *
from tkinter import messagebox
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from datetime import datetime
import locale
import webbrowser
import urllib.parse

locale.setlocale(locale.LC_TIME, 'french')  

# Fonctions
def afficher_admin():
    admin_window.geometry("800x500")
    frame_admin.pack(expand=True, fill="both")
    frame_profil.pack_forget()
    frame_creer_profil.pack_forget()
    frame_article.pack_forget()
    frame_article_options.pack_forget()
    frame_vente.pack_forget()
    frame_restock.pack_forget()

def afficher_profil():
    admin_window.geometry("800x500")
    frame_profil.pack(expand=True, fill="both")
    frame_admin.pack_forget()
    frame_creer_profil.pack_forget()
    frame_article.pack_forget()
    frame_article_options.pack_forget()
    get_profil()

def enregistrer_sql():

    get_prenom = creer_entry_prenom.get()
    get_nom = creer_entry_nom.get()
    get_mdp = creer_entry_mdp.get()
    get_mail = creer_entry_mail.get()

    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Utilisateurs WHERE nom = ?", (get_nom,))
    verif = cursor.fetchone()

    if verif:
        messagebox.showwarning("Attention", "Le nom existe déjà dans la base de données.")
    else:
        status = "salarié"

        cursor.execute("INSERT INTO Utilisateurs(nom, prenom, mot_de_passe, status, e_mail) VALUES(?, ?, ?, ?, ?)",
                       (get_nom, get_prenom, get_mdp, status, get_mail))
        conn.commit()
        messagebox.showinfo("Succès", "Compte créé avec succès !")

        get_profil()  # pour actualiser sans quitter l'application

    conn.close()

def enregistrer_sql_article():
    avoir_article = entry_nom_article.get()
    avoir_prix = entry_prix_article.get()
    avoir_quantite = entry_quantite_article.get()
    avoir_code = entry_code_article.get()


    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Article WHERE nom_article = ?", (avoir_article,))
    verifier_article = cursor.fetchone()

    if verifier_article:
        messagebox.showwarning("Erreur", "Cet article existe déjà dans la base de données.")
    else:
        cursor.execute("INSERT INTO Article (nom_article, prix, quantite, code_barre) VALUES (?, ?, ?, ?)",
                       (avoir_article, avoir_prix, avoir_quantite, avoir_code))
        messagebox.showinfo(".", "Article ajouté à votre magasin !")
        conn.commit()
        get_article()  # Actualiser la liste des articles
    conn.close()
     # mettre un avertissement si duplication de code barre est inutile car quand tu scan c'est d'office unique


def creer_profil():
    admin_window.geometry("800x500")
    frame_creer_profil.pack(expand=True, fill="both")
    frame_profil.pack_forget()
    frame_admin.pack_forget()
    frame_article.pack_forget()
    frame_article_options.pack_forget()

def afficher_profil_depuis_creation():
    admin_window.geometry("800x500")
    frame_profil.pack(expand=True, fill="both")
    frame_creer_profil.pack_forget()
    frame_admin.pack_forget()
    frame_article.pack_forget()
    frame_article_options.pack_forget()

def afficher_article():
    admin_window.geometry("800x500")
    frame_article.pack(expand=True, fill="both")
    frame_admin.pack_forget()
    frame_profil.pack_forget()
    frame_creer_profil.pack_forget()
    frame_article_options.pack_forget()

def afficher_admin_article():
    admin_window.geometry("800x500")
    frame_admin.pack(expand=True, fill="both")
    frame_article.pack_forget()
    frame_profil.pack_forget()
    frame_creer_profil.pack_forget()
    frame_article_options.pack_forget()

def afficher_article_options():
    admin_window.geometry("800x530")
    frame_article_options.pack(expand=True, fill="both")
    frame_admin.pack_forget()
    frame_profil.pack_forget()
    frame_creer_profil.pack_forget()
    frame_article.pack_forget()
    frame_modifier_article.pack_forget()

def get_profil():
    employe_treeview.delete(*employe_treeview.get_children())  # Effacer les données existantes
    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()


    cursor.execute("SELECT ID_user, prenom, nom, e_mail FROM Utilisateurs")
    employes = cursor.fetchall()


    for employe in employes:
        employe_treeview.insert("", "end", values=(employe[0], employe[1],employe[2],employe[3]))  # Ajouter les données au Treeview
    conn.close()

def get_article():
    table_data.delete(*table_data.get_children())
    restock_treeview.delete(*restock_treeview.get_children())

    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()


    cursor.execute("SELECT ID_article, nom_article, prix, quantite FROM Article")
    objet = cursor.fetchall()


    for article in objet:
        table_data.insert("", "end", values=(article[0], article[1], f"{article[2]}€", article[3]))
        restock_treeview.insert("", "end", values=(article[0], article[1], f"{article[2]}€", article[3]))
    conn.close()

    if article[3] < 10:
        pass




def confirmer_vente():
    global total_ventes
    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%d, %B, %H:%M ")


    for child in vente_treeview.get_children():
        [article, quantite, prix_total] = vente_treeview.item(child, "values")

        cursor.execute("UPDATE Article SET quantite = quantite - ? WHERE nom_article  = ? AND quantite >= ?", (quantite, article, quantite)) #quantite parenthese est le stock que je veux vendre

        if cursor.rowcount: # Vérifie si une ligne a été modifiée donc if "modification faite grace au UPDATE"
            cursor.execute("INSERT INTO Vente (nom_article, quantite, prix_total, date_vente) VALUES (?, ?, ?, ?)", (article, quantite, prix_total, date))
    


    conn.commit()
    conn.close()


    vente_treeview.delete(*vente_treeview.get_children()) # refresh la  treeview
    messagebox.showinfo("", "Ventes confirmées.")

    get_article()

def ajouter_article_vente():
    code_barre = entry_vente_article.get()
    quantite = entry_vente_quantite.get()
    quantite = int(quantite)

    if quantite <= 0: # si l'user met moins que 0
            messagebox.showwarning("", "veuillez mettre une quantité valide !")
    else: 
        conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nom_article, prix, quantite FROM Article WHERE code_barre = ?", (code_barre,)) # récupère les infos de l'article grâce au code barre
        retour_val = cursor.fetchone()
        
        if retour_val:
            [article, prix_unitaire, stock_dispo] = retour_val # retour_val c'est une liste *, donc chaque variable prendras l'article avec le bon index

            quantite_deja_ajoutee = 0 # la quantite dans la treeview

            contenu_vente_treeview = vente_treeview.get_children() 

            for item in contenu_vente_treeview:
                valeurs = vente_treeview.item(item, "values")

                if valeurs[0] == article:
                    quantite_deja_ajoutee += int(valeurs[1])



            # Vérifier si la quantité totale donc déjà ajoutée + nouvelle est disponible
            if (quantite_deja_ajoutee + quantite) > stock_dispo:
                messagebox.showwarning("", f"Stock insuffisant ! Il ne reste que {stock_dispo - quantite_deja_ajoutee} de disponible")
                return


            prix_total = (prix_unitaire * quantite)

            
            if quantite > stock_dispo: # si le stock est trop faible
                messagebox.showwarning("", "Stock insuffisant !")
                return


    #POUR VERIFIER LES DUPLICTAIONS DANS LA TREEVIEW
            for item in contenu_vente_treeview:         # c une boucle dans la treeview
                valeur = vente_treeview.item(item, "values")

                if valeur[0] == article:        # si le premier argument donc "nom article" = au code barre correspondant au nom de l'article dans la DB
                    quantite_treeview = int(valeur[1])          # la quantité dans la treeview
                    new_quantite = quantite_treeview + quantite

                    nouveau_prix = prix_unitaire * new_quantite         # recalcule le prix total
                    vente_treeview.item(item, values=(article, new_quantite, f"{nouveau_prix}€")) 

                    entry_vente_article.delete(0, END)
                    entry_vente_quantite.delete(0, END) 
                    return  # va recommencer la fonction a partir d'ici


            vente_treeview.insert("", "end", values=(article, quantite, f"{prix_total}€"))
                
            entry_vente_article.delete(0, END)
            entry_vente_quantite.delete(0, END)
        else:
            messagebox.showwarning("", "Article non trouvé dans la base de données")
        
        conn.commit()
        conn.close()

def supprimer_article(event=None):
    selected_item = table_data.selection()


    if selected_item:
        item_values = table_data.item(selected_item, "values")
        id_article = item_values[0]


        conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
        cursor = conn.cursor()


        cursor.execute("DELETE FROM Article WHERE ID_article = ?", (id_article,))
        conn.commit()
        messagebox.showinfo("Succès", "Article supprimé avec succès !")


        get_article()  # refresh les articles
        conn.close()
    else:
        messagebox.showwarning("Avertissement", "Aucun article sélectionné.")

def afficher_modifier_article():
    frame_modifier_article.pack(expand=True, fill="both")
    frame_article_options.pack_forget()

def supprimer_employe(event=None):
    selected_emp = employe_treeview.selection()


    if selected_emp:
        emp_values = employe_treeview.item(selected_emp, "values") # POur récupérer la valeur de la ligne
        id_emp = emp_values[0] #le premier argument


        conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
        cursor = conn.cursor()


        cursor.execute("DELETE FROM Utilisateurs WHERE ID_user = ?", (id_emp,))
        conn.commit()
        messagebox.showinfo("Succès", "employé supprimé avec succès !")


        get_profil()  # refresh les articles
        conn.close()
    else:
        messagebox.showwarning("Avertissement", "Aucun article sélectionné.")    

def modifier_article(event=None):
    global selected_article
    selected_article = table_data.selection()  # Récupère la sélection

    if selected_article:
        art_values = table_data.item(selected_article, "values")  #get les valeurs


        entry_modifier_nom_article.delete(0, tk.END) #pour effacer l'entry si je selectionne un autre article
        entry_modifier_nom_article.insert(0, art_values[1])


        entry_modifier_prix_article.delete(0, tk.END)
        entry_modifier_prix_article.insert(0, art_values[2])




        afficher_modifier_article()

def modifier_db_article():
    global entry_modifier_nom_article
    global entry_modifier_prix_article
    global selected_article

    nouveau_nom = entry_modifier_nom_article.get()
    nouveau_prix = entry_modifier_prix_article.get()


    conn = sqlite3.connect("C:\\Users\\yassi\\OneDrive\\Documents\\TFE.db")
    cursor = conn.cursor()
 
    art_values = table_data.item(selected_article, "values")
    id_art = art_values[0]

    cursor.execute("UPDATE Article SET nom_article = ?, prix = ? WHERE ID_article = ? ",(nouveau_nom, nouveau_prix, id_art))
    conn.commit()
    conn.close()

    get_article()

 
def afficher_vente():

    admin_window.geometry("850x500")
    frame_vente.pack(expand=True, fill = "both")
    frame_admin.pack_forget()
    frame_article_options.pack_forget()

def afficher_restock(): # à faire avant le scanner

    admin_window.geometry("850x520")
    frame_restock.pack(expand=True, fill="both")
    frame_admin.pack_forget()

def lien_restock(event=None):
    selected_item = restock_treeview.selection()


    if selected_item:
        item_values = restock_treeview.item(selected_item, "values")

        art = item_values[1]    

        url = f"https://www.amazon.fr/s?k={urllib.parse.quote(art)}" # amazon + mon article
        webbrowser.open(url)
    else:
        messagebox.showwarning("Avertissement", "Aucun article sélectionné.")    

# Fenêtre principale
admin_window = Tk()
admin_window.geometry("800x500")
admin_window.title("Fenêtre Administrateur")


                                                    #FRAME PRINCIPALE
frame_admin = Frame(admin_window, bg="lavender")
frame_admin.place(x=0, y=0, width=800, height=500)


bouton_employe = Button(frame_admin, text="Employé", width=20, height=2, relief='ridge',
                        background='blanched almond', activebackground='pale green',
                        activeforeground='black', font=("arial", 12), command=afficher_profil)
bouton_employe.place(x=10, y=50)

bouton_article = Button(frame_admin, text="Article", width=20, height=2, relief='ridge',
                        background='blanched almond', activebackground='pale green',
                        activeforeground='black', font=("arial", 12), command=afficher_article_options)
bouton_article.place(x=10, y=120)

bouton_vente = Button(frame_admin, text="Vente", width=20, height=2, relief='ridge',
                      background='blanched almond', activebackground='pale green',
                      activeforeground='black', font=("arial", 12), command=afficher_vente)
bouton_vente.place(x=10, y=190)

bouton_restock = Button(frame_admin, text="Renouveler stock", width=20, height=2, relief='ridge',
                        background='blanched almond', activebackground='pale green',
                        activeforeground='black', font=("arial", 12), command=afficher_restock)
bouton_restock.place(x=10, y=260)

bouton_quitter = Button(frame_admin, text="Quitter", width=15, height=1, relief='ridge',
                        background='Tomato', activebackground='pale green',
                        activeforeground='black', font=("arial", 10), command=admin_window.quit)
bouton_quitter.place(x=10, y=450)






                                                        # Frame Profil
frame_profil = Frame(admin_window, bg="lightblue")

label_profil = Label(frame_profil, text="Profil Utilisateur", font=("Arial", 20), bg="lightblue")
label_profil.place(x=10, y=10)

# Treeview pour les employés
style = ttk.Style()
style.configure("Custom.Treeview", font=("Arial", 14))
style.configure("Custom.Treeview.Heading", font=("Arial", 13, "bold"))

employe_treeview = ttk.Treeview(frame_profil, columns=("c1", "c2","c3","c4"), show='headings', height=10, style="Custom.Treeview")
employe_treeview.place(x=10, y=60)

employe_treeview.column("c1", width=150, anchor="center")
employe_treeview.column("c2", width=150, anchor="center")
employe_treeview.column("c3", width=150, anchor="center")
employe_treeview.column("c4", width=150, anchor="center")

employe_treeview.heading("c1", text="ID")
employe_treeview.heading("c2", text="nom")
employe_treeview.heading("c3", text="prénom")
employe_treeview.heading("c4", text="adresse e-mail")



bouton_retour = Button(frame_profil, text="retour", width=15, height=1, relief='ridge',
                       background='red', activebackground='pale green',
                       activeforeground='black', font=("arial", 10), command=afficher_admin)
bouton_retour.place(x=10, y=450)

bouton_ajouter_profil = Button(frame_profil, text="Ajouter un employé", width=15, height=1, relief='ridge',
                               background='blanched almond', activebackground='pale green', command=creer_profil,
                               activeforeground='black', font=("arial", 10))
bouton_ajouter_profil.place(x=640, y=30)

bouton_supprimer_emp = Button(frame_profil, text="supprimer l'employé", width=15, height=1, relief='ridge',
                       background='Tomato', activebackground='pale green',
                       activeforeground='black', font=("arial", 10),command=lambda:supprimer_employe())
bouton_supprimer_emp.place(x=640, y=80)


                                                        
                                                        # Frame Créer Profil

frame_creer_profil = Frame(admin_window, bg="lavender")

creer_entry_nom = Entry(frame_creer_profil, width=20, font=("arial", 12), relief="solid")
creer_entry_nom.place(x=80, y=40)

creer_entry_mdp = Entry(frame_creer_profil, width=20, font=("arial", 12), relief="solid", show="*")
creer_entry_mdp.place(x=80, y=100)

creer_entry_prenom = Entry(frame_creer_profil, width=20, font=("arial", 12), relief="solid")
creer_entry_prenom.place(x=370, y=40)

creer_entry_mail = Entry(frame_creer_profil, width=20, font=("arial", 12), relief="solid")
creer_entry_mail.place(x=370, y=100)

btn_enregistrer = Button(frame_creer_profil, text="Enregistrer", width=10, height=1,
                         relief='ridge', background='blanched almond', activebackground='pale green',
                         activeforeground='black', font=("arial", 10), command=enregistrer_sql)
btn_enregistrer.place(x=200, y=200)

btn_retour = Button(frame_creer_profil, text="Retour", width=10, height=1,
                    relief='ridge', background='grey', activebackground='pale green',
                    activeforeground='black', font=("arial", 10), command=afficher_profil_depuis_creation)
btn_retour.place(x=600, y=10)

label_nom = Label(frame_creer_profil, text="Prénom", font=("Arial", 10), background='lavender')
label_nom.place(x=315, y=40)

label_mdp = Label(frame_creer_profil, text="Mot de passe", background='lavender')
label_mdp.place(x=2, y=100)

label_prenom = Label(frame_creer_profil, text="Nom", font=("Arial", 10), background='lavender')
label_prenom.place(x=40, y=40)

label_mail = Label(frame_creer_profil, text="E-mail", font=("Arial", 10), background='lavender')
label_mail.place(x=315, y=100)



                                                    # Frame ajouter Article

frame_article = Frame(admin_window, bg="PaleGreen2")

label_article = Label(frame_article, text="Ajouter un article", font=("Arial", 25), bg="PaleGreen2")
label_article.place(x=10, y=10)

bouton_retour_admin = Button(frame_article, text="Retour", width=15, height=1, relief='ridge',
                             background='Bisque3', activebackground='white', activeforeground='black',
                             font=("arial", 10), command=afficher_article_options)
bouton_retour_admin.place(x=10, y=450)

bouton_confirmer_article = Button(frame_article, text="Ajouter un article", width=15, height=1, relief='ridge',
                                  activebackground='white', activeforeground='black', font=("arial", 10),
                                  command=enregistrer_sql_article)
bouton_confirmer_article.place(x=300, y=380)

entry_nom_article = Entry(frame_article, width=20, font=("arial", 12), relief="solid")
entry_nom_article.place(x=300, y=100)

label_nom_article = Label(frame_article, text="Nom de l'article", font=("Arial", 10), bg="PaleGreen2")
label_nom_article.place(x=200, y=100)

entry_prix_article = Entry(frame_article, width=20, font=("arial", 12), relief="solid")
entry_prix_article.place(x=300, y=180)

label_prix_article = Label(frame_article, text="Prix de l'article", font=("Arial", 10), bg="PaleGreen2")
label_prix_article.place(x=200, y=180)

entry_quantite_article = Entry(frame_article, width=20, font=("arial", 12), relief="solid")
entry_quantite_article.place(x=300, y=260)

label_quantite_article = Label(frame_article, text="Quantité", font=("Arial", 10), bg="PaleGreen2")
label_quantite_article.place(x=200, y=260)

entry_code_article = Entry(frame_article, width=20, font=("arial", 12), relief="solid")
entry_code_article.place(x=300, y=340)

label_quantite_article = Label(frame_article, text="code barre", font=("Arial", 10), bg="PaleGreen2")
label_quantite_article.place(x=200, y=340)    
    


    
                                                                                # Frame Article Options
frame_article_options = Frame(admin_window, bg="lightgreen")

label_article_options = Label(frame_article_options, text="Options Articles", font=("Arial", 25), bg="lightgreen")
label_article_options.place(x=10, y=10)

bouton_ajouter_article_option = Button(frame_article_options, text="Ajouter un article", width=15, height=1, relief='ridge',
                                       background='pale green', activebackground='white', activeforeground='black',
                                       font=("arial", 10), command=afficher_article)
bouton_ajouter_article_option.place(x=640, y=30)

bouton_supprimer_article_option = Button(frame_article_options, text="Supprimer un article", width=15, height=1, relief='ridge',
                                         background='Coral', activebackground='white', activeforeground='black',
                                         font=("arial", 10), command=lambda: supprimer_article())
bouton_supprimer_article_option.place(x=640, y=80)

bouton_retour_admin_article_options = Button(frame_article_options, text="retour", width=15, height=1, relief='ridge',
                                             background='grey', activebackground='white', activeforeground='black',
                                             font=("arial", 10), command=afficher_admin)
bouton_retour_admin_article_options.place(x=10, y=450)

bouton_modifier_article = Button(frame_article_options, text="Modifier un article", width=15, height=1, relief='ridge',
                                             background='orange', activebackground='white', activeforeground='black',
                                             font=("arial", 10),command=lambda:modifier_article())
bouton_modifier_article.place(x=640, y=130)

                                        # Treeview pour les articles
style = ttk.Style()
style.configure("Custom.Treeview", font=("Arial", 14))
style.configure("Custom.Treeview.Heading", font=("Arial", 13, "bold"))

table_data = ttk.Treeview(frame_article_options, columns=("c1", "c2", "c3", "c4"), show='headings', height=18, style="Custom.Treeview")
table_data.place(x=10, y=60)

table_data.column("c1", width=150, anchor="center")
table_data.column("c2", width=150, anchor="center")
table_data.column("c3", width=150, anchor="center")
table_data.column("c4", width=150, anchor="center")

table_data.heading("c1", text="ID")
table_data.heading("c2", text="Article")
table_data.heading("c3", text="Prix")
table_data.heading("c4", text="Quantité")

                                                            #FRAME MODIFIER ARTICLE

frame_modifier_article = Frame(admin_window, bg="navajo white")


label_modifier_article = Label(frame_modifier_article, text="Modifier un article", font=("Arial", 20), bg="navajo white")
label_modifier_article.place(x=10, y=10)

label_modifier_nom_article = Label(frame_modifier_article, text="Nom de l'article", font=("Arial", 10), bg="navajo white")
label_modifier_nom_article.place(x=200, y=100)


entry_modifier_nom_article = Entry(frame_modifier_article, width=20, font=("arial", 12), relief="solid")
entry_modifier_nom_article.place(x=300, y=100)

entry_modifier_nom_article.insert("0","coucou")
label_modifier_prix_article = Label(frame_modifier_article, text="Prix de l'article", font=("Arial", 10), bg="navajo white")
label_modifier_prix_article.place(x=200, y=180)


entry_modifier_prix_article = Entry(frame_modifier_article, width=20, font=("arial", 12), relief="solid")
entry_modifier_prix_article.place(x=300, y=180)



btn_modifier_article = Button(frame_modifier_article, text="ajouter une vente", width=13,
                              relief='ridge', background='blanched almond', activebackground='pale green',
                              activeforeground='black', font=("arial", 10),command=modifier_db_article)
btn_modifier_article.place(x=350, y=350)

btn_annuler_modification = Button(frame_modifier_article, text="Annuler", width=10, height=1,
                                  relief='ridge', background='grey', activebackground='pale green',
                                  activeforeground='black', font=("arial", 10), command=afficher_article_options)
btn_annuler_modification.place(x=200, y=350)



                                            #FRAME VENTE

frame_vente = Frame(admin_window, bg="lightyellow")

label_vente = Label(frame_vente, text="Enregistrer une vente", font=("Arial", 20), bg="lightyellow")
label_vente.place(x=10, y=10)

# Liste des ventes avec un Treeview
vente_treeview = ttk.Treeview(frame_vente, columns=("c1", "c2", "c3"), show='headings', height=10,style="Custom.Treeview")
vente_treeview.place(x=10, y=60)

vente_treeview.column("c1", width=200, anchor="center")
vente_treeview.column("c2", width=150, anchor="center")
vente_treeview.column("c3", width=150, anchor="center")

vente_treeview.heading("c1", text="Nom Article")
vente_treeview.heading("c2", text="Quantité")
vente_treeview.heading("c3", text="Prix total")

label_nom_article = Label(frame_vente, text="Article", font=("Arial", 10), bg="lightyellow")
label_nom_article.place(x=530, y=70)

entry_vente_article = Entry(frame_vente, width=20, font=("arial", 12), relief="solid")
entry_vente_article.place(x=590, y=70)

label_quantite = Label(frame_vente, text="Quantité", font=("Arial", 10), bg="lightyellow")
label_quantite.place(x=530, y=120)

entry_vente_quantite = Entry(frame_vente, width=20, font=("arial", 12), relief="solid")
entry_vente_quantite.place(x=590, y=120)

# Bouton pour enregistrer la vente
btn_enregistrer_vente = Button(frame_vente, text="Valider", width=15, height=1, relief='ridge',
                               background='lightgreen', activebackground='white', activeforeground='black',
                               font=("arial", 10),command=ajouter_article_vente)
btn_enregistrer_vente.place(x=590, y=200)

# Bouton Retour
btn_retour_vente = Button(frame_vente, text="Retour", width=15, height=1, relief='ridge',
                          background='orange', activebackground='white', activeforeground='black',
                          font=("arial", 10), command=afficher_admin)
btn_retour_vente.place(x=10, y=450)


btn_finaliser_vente = Button(frame_vente, text="Confirmer la vente", width=25, height=7, relief='ridge', background='DarkSeaGreen2',
                            activebackground='white', activeforeground='black',command=confirmer_vente,
                            font=("arial", 15))
btn_finaliser_vente.place(x=555, y=320)



                                                        #FRAME RESTOCK
frame_restock = Frame(admin_window, bg="thistle")

label_restock = Label(frame_restock, text="renouveler un stock", font=("Arial", 20), bg="thistle")
label_restock.place(x=10, y=10)


restock_treeview = ttk.Treeview(frame_restock, columns=("c1", "c2", "c3","c4"), show='headings', height=18, style="Custom.Treeview")
restock_treeview.place(x=10, y=60)

restock_treeview.column("c1", width=150, anchor="center")
restock_treeview.column("c2", width=150, anchor="center")
restock_treeview.column("c3", width=150, anchor="center")
restock_treeview.column("c4", width=150, anchor="center")


restock_treeview.heading("c1", text="ID")
restock_treeview.heading("c2", text="Nom Article")
restock_treeview.heading("c3", text="Prix Total")
restock_treeview.heading("c4", text="Quantité")


bouton_restock_retour = Button(frame_restock, text="retour", width=15, height=1, relief='ridge',
                       background='indian red', activebackground='pale green',
                       activeforeground='black', font=("arial", 10), command=afficher_admin)
bouton_restock_retour.place(x=10, y=450)

bouton_restock_lien = Button(frame_restock, text="vérifier la disponibilité", width=18, height=3, relief='ridge',
                                             background='MediumPurple1', activebackground='white', activeforeground='black',
                                             font=("arial", 13),command=lambda:lien_restock())
bouton_restock_lien.place(x=640, y=130)



get_profil()
get_article()

afficher_admin()
admin_window.mainloop()

