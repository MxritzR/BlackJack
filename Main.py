import tkinter as tk
from PIL import Image, ImageTk
import random
import os

#Kartenfarben und werte definieren
farben = ['H', 'D', 'S', 'C']
werte = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
karten_bilder = {}
hand_bets = []
aktuelle_hand = 0
splitting = False
info_fenster = None
guthaben = 1000  # Startguthaben
einsatz = 100  # Standard-Einsatz für jede Runde





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

#Guthaben berechnen
def update_guthaben_label():
    guthaben_label.config(text=f"Guthaben: {guthaben} €")


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

#Guthaben anzeigen
guthaben_label = tk.Label(root, text=f"Guthaben: {guthaben} €", bg="#2d2d2d", fg="white", font=("Arial", 12, "bold"))
guthaben_label.pack()

einsatz_frame = tk.Frame(root, bg="#2d2d2d")
einsatz_frame.pack(pady=5)

tk.Label(einsatz_frame, text="Einsatz:", bg="#2d2d2d", fg="white", font=("Arial", 12)).pack(side="left")
einsatz_entry = tk.Entry(einsatz_frame, font=("Arial", 12), width=8)
einsatz_entry.insert(0, "100")
einsatz_entry.pack(side="left", padx=5)


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
    if len(spieler_karten) == 0 or aktuelle_hand >= len(spieler_karten):
        return  # Schutz vor Zugriff außerhalb der Liste

    #Dealer-Karten anzeigen
    for widget in frame_dealer.winfo_children():
        widget.destroy()
    for i, karte in enumerate(dealer_karten):
        img = karten_bilder[karte] if dealer_offen or i == 0 else karten_bilder["BACK"]
        tk.Label(frame_dealer, image=img, bg="#2d2d2d").pack(side="left", padx=5)

    # Spieler-Karten anzeigen
    for widget in frame_spieler.winfo_children():
        widget.destroy()

    for i, hand in enumerate(spieler_karten):
        hand_frame = tk.Frame(frame_spieler, bg="#2d2d2d")
        hand_frame.pack(side="left", padx=20)

        for karte in hand:
            img = karten_bilder[karte]
            tk.Label(hand_frame, image=img, bg="#2d2d2d").pack(side="left", padx=2)

        # Aktive Hand visuell hervorheben
        if i == aktuelle_hand:
            tk.Label(hand_frame, text=f"Hand {i + 1} (aktiv)", fg="white", bg="#2d2d2d", font=("Arial", 10)).pack()
        else:
            tk.Label(hand_frame, text=f"Hand {i + 1}", fg="gray", bg="#2d2d2d", font=("Arial", 10)).pack()


    #Punktestände aktualisieren
    punkte_spieler = berechne_punkte(spieler_karten[aktuelle_hand])
    punkte_dealer = berechne_punkte(dealer_karten if dealer_offen else dealer_karten[1:])
    spieler_label.config(text=f"Spieler: {punkte_spieler}")
    dealer_label.config(text=f"Dealer: {punkte_dealer}")


def zeige_info():
    global info_fenster

    if info_fenster is not None and tk.Toplevel.winfo_exists(info_fenster):
        info_fenster.lift()  # Fenster in den Vordergrund holen
        return

    info_text = (
        "Anleitung – Blackjack \n\n"
        "Ziel des Spiels:\n"
        "Mit den eigenen Karten möglichst nahe an 21 Punkte kommen ohne darüber zu gehen.\n\n"
        "Spielablauf:\n"
        "- Der Spieler und der Dealer erhalten jeweils zwei Karten\n"
        "- Eine Dealer-Karte bleibt verdeckt\n"
        "- Der Spieler entscheidet sich für Aktionen\n\n"
        "Aktionen:\n"
        "  Hit: Eine weitere Karte ziehen\n"
        "  Stand: Bei den aktuellen Karten bleiben\n"
        "  Double: Einsatz symbolisch verdoppeln, genau eine Karte ziehen, dann stehen\n"
        "  Split: Zwei gleiche Karten aufteilen und zwei Hände spielen\n\n"
        "Dealer-Regeln:\n"
        "- Der Dealer zieht bis mindestens 17 Punkte\n"
        "- Ass zählt 11 oder 1, je nach Situation\n\n"
        "Spielende:\n"
        "- Über 21 = verloren\n"
        "- Mehr Punkte als Dealer = gewonnen\n"
        "- Gleichstand = unentschieden\n"
        "- Weniger Punkte als Dealer = verloren"
    )

    info_fenster = tk.Toplevel(root)
    info_fenster.title("Spielanleitung")
    info_fenster.geometry("600x500")
    info_fenster.configure(bg="#f0f0f0")

    text_widget = tk.Text(info_fenster, wrap="word", font=("Arial", 11), bg="#f0f0f0", borderwidth=0)
    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Beim Schließen: Variable zurücksetzen
    def on_close():
        global info_fenster
        info_fenster.destroy()
        info_fenster = None

    info_fenster.protocol("WM_DELETE_WINDOW", on_close)

#Neue Runde starten (2 Karten für Spieler & Dealer)
def neue_runde():
    # Alle veränderten globalen Variablen deklarieren
    global spieler_karten, dealer_karten, spiel_beendet, hand_bets, aktuelle_hand, splitting, guthaben, einsatz


    spiel_beendet = False

    # Einsatz prüfen und abziehen
    try:
        neuer_einsatz = int(einsatz_entry.get())
        if neuer_einsatz <= 0:
            raise ValueError
    except ValueError:
        status_label.config(text="Ungültiger Einsatz!")
        return

    if guthaben < neuer_einsatz:
        status_label.config(text="Nicht genug Guthaben für diesen Einsatz!")
        return

    einsatz = neuer_einsatz
    guthaben -= einsatz


    spieler_karten = [[ziehe_karte(), ziehe_karte()]]
    hand_bets = [einsatz] #Einsatz merken
    aktuelle_hand = 0
    splitting = False
    dealer_karten = [ziehe_karte(), ziehe_karte()]


    update_gui()
    update_guthaben_label()

    # Direkt prüfen, ob Blackjack
    if berechne_punkte(spieler_karten[0]) == 21:
        status_label.config(text="Blackjack! Du gewinnst direkt.")
        guthaben += int(einsatz * 2.5)
        spiel_beendet = True
        update_gui(dealer_offen=True)
        update_guthaben_label()
        return

    status_label.config(text="Neue Runde gestartet. Deine Entscheidung…")


#Spieler zieht Karte
def hit():
    global spiel_beendet
    if spiel_beendet:
        return
    spieler_karten[aktuelle_hand].append(ziehe_karte())
    update_gui()
    if berechne_punkte(spieler_karten[aktuelle_hand]) > 21:
        status_label.config(text="Überkauft! Dealer gewinnt.")
        spiel_beendet = True
        update_gui(dealer_offen=True)

#Spieler bleibt stehen, Dealer zieht und Ergebnis wird ausgewertet
def stand():
    global aktuelle_hand, spiel_beendet

    if splitting and aktuelle_hand == 0:
        aktuelle_hand = 1
        status_label.config(text="Zweite Hand spielen…")
        update_gui()
        return

    while berechne_punkte(dealer_karten) < 17:
        dealer_karten.append(ziehe_karte())

    update_gui(dealer_offen=True)
    auswertung()
    spiel_beendet = True

# Vergleicht jede Spielerhand mit dem Dealer und zeigt das Ergebnis an
def auswertung():
    global guthaben, einsatz, spiel_beendet  # Zugriff auf die globalen Variablen

    if spiel_beendet:
        return  # Verhindert doppeltes Ausführen

    dp = berechne_punkte(dealer_karten)
    for i, hand in enumerate(spieler_karten):
        sp = berechne_punkte(hand)

        # Ergebnislogik
        if sp > 21:
            result = "verloren"
        elif dp > 21 or sp > dp:
            result = "gewonnen"
        elif sp == dp:
            result = "unentschieden"
        else:
            result = "verloren"

        # Guthaben anpassen
        einsatz_hand = hand_bets[i]
        if result == "gewonnen":
            guthaben += einsatz_hand * 2
        elif result == "unentschieden":
            guthaben += einsatz_hand

        update_guthaben_label()

        # Status anzeigen
        status_label.config(text=f"Hand {i+1}: Du hast {result}.")

        spiel_beendet = True  # Spieler kann danach nichts mehr drücken

# Teilt eine Spielerhand auf, wenn zwei gleiche Karten vorhanden sind
def split_hand():
    global splitting, spieler_karten, hand_bets, aktuelle_hand
    hand = spieler_karten[0]
    if len(hand) != 2 or kartenwert(hand[0]) != kartenwert(hand[1]):
        return
    splitting = True
    spieler_karten = [[hand[0], ziehe_karte()], [hand[1], ziehe_karte()]]
    hand_bets = [1, 1]
    aktuelle_hand = 0
    update_gui()
    status_label.config(text="Split – Hand 1 spielen")

# Verdoppelt den Einsatz (symbolisch), zieht eine Karte und beendet die Runde
def double_down():
    global guthaben, hand_bets

    if spiel_beendet:
        return  # Kein Double nach Spielende

    hand = spieler_karten[aktuelle_hand]
    if len(hand) != 2:
        return
    if guthaben < hand_bets[aktuelle_hand]:
        status_label.config(text="Nicht genug Guthaben für Double.")
        return

    # Einsatz verdoppeln
    guthaben -= hand_bets[aktuelle_hand]
    hand_bets[aktuelle_hand] *= 2
    update_guthaben_label()

    # Eine Karte ziehen und stehen
    hand.append(ziehe_karte())
    update_gui()
    stand()



#Button unten
btn_frame = tk.Frame(root, bg="#2d2d2d")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text="Neue Runde", command=neue_runde, bg="#4caf50", fg="white", font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Hit", command=hit, bg="#2196f3", fg="white", font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Stand", command=stand, bg="#f44336", fg="white", font=("Arial", 12), width=12).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Double", command=double_down, bg="#ff9800", fg="white", font=("Arial", 12), width=12).grid(row=0, column=3, padx=10)
tk.Button(btn_frame, text="Split", command=split_hand, bg="#9c27b0", fg="white", font=("Arial", 12), width=12).grid(row=0, column=4, padx=10)
tk.Button(btn_frame, text="Info", command=zeige_info, bg="#607d8b", fg="white", font=("Arial", 12), width=12).grid(row=0, column=5, padx=10)



#Spiel starten
neue_runde()
root.mainloop()