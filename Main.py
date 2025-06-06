<<<<<<< HEAD
import tkinter as tk
from PIL import Image, ImageTk
import random
import os

#Kartenfarben und werte definieren
farben = ['H', 'D', 'S', 'C']
werte = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
karten_bilder = {}

#Kartenwert berechnen für eine einzelne Karte
def kartenwert(karte):
    wert = karte[:-1]
    if wert in ['J', 'Q', 'K']:
        return 10
    elif wert == 'A':
        return 11
    else:
        return int(wert)

#Punkte einer Hand berechnen (inkl Ass-Logik)
def berechne_punkte(karten):
    punkte = sum(kartenwert(k) for k in karten)
    as_count = sum(1 for k in karten if k[:-1] == 'A')
    while punkte > 21 and as_count:
        punkte -= 10
        as_count -= 1
    return punkte

#Eine neue zufällige Karte ziehen
def ziehe_karte():
    return random.choice(werte) + random.choice(farben)

#GUI-Grundstruktur
root = tk.Tk()
root.title("Blackjack")
root.config(bg="#2d2d2d")
root.geometry("800x600")

#Statusanzeige
status_label = tk.Label(root, text="Willkommen bei Blackjack!", bg="#2d2d2d", fg="white", font=("Arial", 16))
status_label.pack(pady=20)

#Bereiche für Kartenanzeige
frame_dealer = tk.Frame(root, bg="#2d2d2d")
frame_dealer.pack(pady=10)

frame_spieler = tk.Frame(root, bg="#2d2d2d")
frame_spieler.pack(pady=10)

#Punktestände anzeigen
dealer_label = tk.Label(root, text="Dealer: 0", bg="#2d2d2d", fg="white", font=("Arial", 12, "bold"))
dealer_label.pack()
spieler_label = tk.Label(root, text="Spieler: 0", bg="#2d2d2d", fg="white", font=("Arial", 12, "bold"))
spieler_label.pack()

#Kartengrafiken laden
def lade_bilder():
    pfad = "cards"
    for wert in werte:
        for farbe in farben:
            name = f"{wert}{farbe}"
            datei = f"{pfad}/{name}.png"
            if os.path.exists(datei):
                img = Image.open(datei).resize((80, 120))
                karten_bilder[name] = ImageTk.PhotoImage(img)
    back = Image.open(f"{pfad}/back.png").resize((80, 120))
    karten_bilder["BACK"] = ImageTk.PhotoImage(back)

lade_bilder()

#Spielstatusvariablen
spieler_karten = []
dealer_karten = []
spiel_beendet = False

#GUI aktualisieren (Karten und Punkte anzeigen)
def update_gui(dealer_offen=False):
    #Dealer-Karten anzeigen
    for widget in frame_dealer.winfo_children():
        widget.destroy()
    for i, karte in enumerate(dealer_karten):
        img = karten_bilder[karte] if dealer_offen or i == 0 else karten_bilder["BACK"]
        tk.Label(frame_dealer, image=img, bg="#2d2d2d").pack(side="left", padx=5)

    #Spieler-Karten anzeigen
    for widget in frame_spieler.winfo_children():
        widget.destroy()
    for karte in spieler_karten:
        img = karten_bilder[karte]
        tk.Label(frame_spieler, image=img, bg="#2d2d2d").pack(side="left", padx=5)

    #Punktestände aktualisieren
    punkte_spieler = berechne_punkte(spieler_karten)
    punkte_dealer = berechne_punkte(dealer_karten if dealer_offen else dealer_karten[1:])
    spieler_label.config(text=f"Spieler: {punkte_spieler}")
    dealer_label.config(text=f"Dealer: {punkte_dealer}")

#Neue Runde starten (2 Karten für Spieler & Dealer)
def neue_runde():
    global spieler_karten, dealer_karten, spiel_beendet
    spiel_beendet = False
    spieler_karten = [ziehe_karte(), ziehe_karte()]
    dealer_karten = [ziehe_karte(), ziehe_karte()]
    status_label.config(text="Neue Runde gestartet. Deine Entscheidung…")
    update_gui()

#Spieler zieht Karte
def hit():
    global spiel_beendet
    if spiel_beendet:
        return
    spieler_karten.append(ziehe_karte())
    update_gui()
    if berechne_punkte(spieler_karten) > 21:
        status_label.config(text="Überkauft! Dealer gewinnt.")
        spiel_beendet = True
        update_gui(dealer_offen=True)

#Spieler bleibt stehen, Dealer zieht und Ergebnis wird ausgewertet
def stand():
    global spiel_beendet
    if spiel_beendet:
        return
    while berechne_punkte(dealer_karten) < 17:
        dealer_karten.append(ziehe_karte())
    punkte_spieler = berechne_punkte(spieler_karten)
    punkte_dealer = berechne_punkte(dealer_karten)
    if punkte_dealer > 21 or punkte_spieler > punkte_dealer:
        status_label.config(text="Du gewinnst!")
    elif punkte_spieler == punkte_dealer:
        status_label.config(text="Unentschieden.")
    else:
        status_label.config(text="Dealer gewinnt.")
    spiel_beendet = True
    update_gui(dealer_offen=True)

#Button unten
btn_frame = tk.Frame(root, bg="#2d2d2d")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text="Neue Runde", command=neue_runde, bg="#4caf50", fg="white", font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Hit", command=hit, bg="#2196f3", fg="white", font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Stand", command=stand, bg="#f44336", fg="white", font=("Arial", 12), width=12).grid(row=0, column=2, padx=10)

#Spiel starten
neue_runde()
=======
import tkinter as tk
from PIL import Image, ImageTk
import random
import os

#Kartenfarben und werte definieren
farben = ['H', 'D', 'S', 'C']
werte = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
karten_bilder = {}

#Kartenwert berechnen für eine einzelne Karte
def kartenwert(karte):
    wert = karte[:-1]
    if wert in ['J', 'Q', 'K']:
        return 10
    elif wert == 'A':
        return 11
    else:
        return int(wert)

#Punkte einer Hand berechnen (inkl Ass-Logik)
def berechne_punkte(karten):
    punkte = sum(kartenwert(k) for k in karten)
    as_count = sum(1 for k in karten if k[:-1] == 'A')
    while punkte > 21 and as_count:
        punkte -= 10
        as_count -= 1
    return punkte

#Eine neue zufällige Karte ziehen
def ziehe_karte():
    return random.choice(werte) + random.choice(farben)

#GUI-Grundstruktur
root = tk.Tk()
root.title("Blackjack")
root.config(bg="#2d2d2d")
root.geometry("800x600")

#Statusanzeige
status_label = tk.Label(root, text="Willkommen bei Blackjack!", bg="#2d2d2d", fg="white", font=("Arial", 16))
status_label.pack(pady=20)

#Bereiche für Kartenanzeige
frame_dealer = tk.Frame(root, bg="#2d2d2d")
frame_dealer.pack(pady=10)

frame_spieler = tk.Frame(root, bg="#2d2d2d")
frame_spieler.pack(pady=10)

#Punktestände anzeigen
dealer_label = tk.Label(root, text="Dealer: 0", bg="#2d2d2d", fg="white", font=("Arial", 12, "bold"))
dealer_label.pack()
spieler_label = tk.Label(root, text="Spieler: 0", bg="#2d2d2d", fg="white", font=("Arial", 12, "bold"))
spieler_label.pack()

#Kartengrafiken laden
def lade_bilder():
    pfad = "cards"
    for wert in werte:
        for farbe in farben:
            name = f"{wert}{farbe}"
            datei = f"{pfad}/{name}.png"
            if os.path.exists(datei):
                img = Image.open(datei).resize((80, 120))
                karten_bilder[name] = ImageTk.PhotoImage(img)
    back = Image.open(f"{pfad}/back.png").resize((80, 120))
    karten_bilder["BACK"] = ImageTk.PhotoImage(back)

lade_bilder()

#Spielstatusvariablen
spieler_karten = []
dealer_karten = []
spiel_beendet = False

#GUI aktualisieren (Karten und Punkte anzeigen)
def update_gui(dealer_offen=False):
    #Dealer-Karten anzeigen
    for widget in frame_dealer.winfo_children():
        widget.destroy()
    for i, karte in enumerate(dealer_karten):
        img = karten_bilder[karte] if dealer_offen or i == 0 else karten_bilder["BACK"]
        tk.Label(frame_dealer, image=img, bg="#2d2d2d").pack(side="left", padx=5)

    #Spieler-Karten anzeigen
    for widget in frame_spieler.winfo_children():
        widget.destroy()
    for karte in spieler_karten:
        img = karten_bilder[karte]
        tk.Label(frame_spieler, image=img, bg="#2d2d2d").pack(side="left", padx=5)

    #Punktestände aktualisieren
    punkte_spieler = berechne_punkte(spieler_karten)
    punkte_dealer = berechne_punkte(dealer_karten if dealer_offen else dealer_karten[1:])
    spieler_label.config(text=f"Spieler: {punkte_spieler}")
    dealer_label.config(text=f"Dealer: {punkte_dealer}")

#Neue Runde starten (2 Karten für Spieler & Dealer)
def neue_runde():
    global spieler_karten, dealer_karten, spiel_beendet
    spiel_beendet = False
    spieler_karten = [ziehe_karte(), ziehe_karte()]
    dealer_karten = [ziehe_karte(), ziehe_karte()]
    status_label.config(text="Neue Runde gestartet. Deine Entscheidung…")
    update_gui()

#Spieler zieht Karte
def hit():
    global spiel_beendet
    if spiel_beendet:
        return
    spieler_karten.append(ziehe_karte())
    update_gui()
    if berechne_punkte(spieler_karten) > 21:
        status_label.config(text="Überkauft! Dealer gewinnt.")
        spiel_beendet = True
        update_gui(dealer_offen=True)

#Spieler bleibt stehen, Dealer zieht und Ergebnis wird ausgewertet
def stand():
    global spiel_beendet
    if spiel_beendet:
        return
    while berechne_punkte(dealer_karten) < 17:
        dealer_karten.append(ziehe_karte())
    punkte_spieler = berechne_punkte(spieler_karten)
    punkte_dealer = berechne_punkte(dealer_karten)
    if punkte_dealer > 21 or punkte_spieler > punkte_dealer:
        status_label.config(text="Du gewinnst!")
    elif punkte_spieler == punkte_dealer:
        status_label.config(text="Unentschieden.")
    else:
        status_label.config(text="Dealer gewinnt.")
    spiel_beendet = True
    update_gui(dealer_offen=True)

#Button unten
btn_frame = tk.Frame(root, bg="#2d2d2d")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text="Neue Runde", command=neue_runde, bg="#4caf50", fg="white", font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Hit", command=hit, bg="#2196f3", fg="white", font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Stand", command=stand, bg="#f44336", fg="white", font=("Arial", 12), width=12).grid(row=0, column=2, padx=10)

#Spiel starten
neue_runde()
>>>>>>> 68c48b515ba1b6a0b67d1ae2c3bcdd6267271dd9
root.mainloop()