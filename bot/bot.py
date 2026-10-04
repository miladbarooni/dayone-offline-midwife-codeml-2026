"""DayOne — Offline Midwife : bot Telegram, extraction 100 % locale (v3, checklists par type de page).

Passe A : identifier le type de page (6 types du registre).
Passe B : interroger la page avec la CHECKLIST des champs imprimés de ce type —
          chaque champ doit recevoir une valeur, "VIDE" ou "ILLISIBLE" (aucun oubli possible).

Run :  TELEGRAM_TOKEN=123:abc [DAYONE_MODEL=gemma4:12b] python3 -u bot.py
"""
import base64, json, os, sys, time, urllib.request, urllib.parse

TOKEN = os.environ.get("TELEGRAM_TOKEN") or sys.exit("Set TELEGRAM_TOKEN (get one from @BotFather)")
API = f"https://api.telegram.org/bot{TOKEN}"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("DAYONE_MODEL", "qwen2.5vl:7b")
CONF_SEUIL = 0.75

T_FICHE, T_IDENT, T_GROSS, T_ACCOU, T_PRECO, T_TARDIF, T_AUTRE = PAGE_TYPES = [
    "FICHE DE SURVEILLANCE (en-tête)", "IDENTIFICATION ET ANTÉCÉDENTS", "GROSSESSE ACTUELLE",
    "DÉROULEMENT DE L'ACCOUCHEMENT", "CONSULTATION DU POST-PARTUM PRÉCOCE",
    "CONSULTATION DU POST-PARTUM TARDIF", "AUTRE"]

CHECKLISTS = {
 T_FICHE: """N° de la fiche · Région · Province · Nom de l'établissement sanitaire ·
Type de l'établissement [case: DR/CSC/CSU/CSCA/CSUA] · Couverture [case: Fixe/Mobile] ·
Nom/Prénom de la parturiente · Grossesse classée à risque [case] ·
Type de risque [cases: Anémie/H.T.A/Diabète/Cardiopathie/Métrorragie/Infection/Pré-éclampsie/Eclampsie/Autres]""",
 T_IDENT: """Age · CIN · Niveau d'instruction · Profession · Adresse · Téléphone · Nom du mari · Profession du mari ·
Consanguinité [case] · Grossesse désirée [case] ·
Antécédents familiaux, séparer « famille de la femme » et « mari/famille » [cases: HTA/Diabète/Maladies héréditaires/Malformations/Allergies] ·
Antécédents de la femme : Médicaux · Chirurgicaux · Gynécologiques ·
Anomalies des grossesses antérieures, une entrée par ligne remplie (Avortement/Accouchement prématuré/Mort fœtale in utéro/Autres) avec Nature, Nombre, Date, Lieu, Âge gestationnel ·
Déroulement des accouchements antérieurs, une entrée par cellule remplie « <ligne> — Accouch. N » (Date/Modalité d'extraction/Indication césarienne/Complication/Poids nouveau-né/Compl. nouveau-né) ·
Gestation · Parité · Nombre d'enfants vivants · VAT · Vaccinée contre la rubéole [case] · Vaccinée contre l'hépatite B [case] · Frottis cervical / IVA""",
 T_GROSS: """DDR · Taille · Groupage [case: A/B/O/AB] · Rhésus [case: Rh+/Rh-] · Date prévue d'accouchement · Date de dépassement de terme ·
puis le TABLEAU des visites — colonnes : 1er trim. V1/V2/V3, 2ème trim. V1/V2/V3, 7ème/8ème/9ème mois —
UNE entrée par CELLULE remplie, nom = « <ligne> — <colonne> », pour les lignes :
Rendez-vous · Venue le · Visites de relance · Age probable · Poids (kg) · TA · Anomalies squelette ·
État des conjonctives · Examen des seins · Œdèmes · Mouvements actifs · HU (cm) · BCF · Examen au spéculum ·
TV état du col · TV présentation · TV bassin · Glucosurie · Albuminurie · Rubéole · Toxoplasmose ·
Syphilis (TPHA/VDRL) · Ag HBs · Sérologie VIH · Hémoglobine · Plaquettes · Bilan glycémique · RAI ·
Traitement Fer · Examen fait par""",
 T_ACCOU: """Patiente · Lieu [cases: Maison d'accouchement/Maternité/Clinique privée/A domicile/Autres] ·
Assisté par un personnel qualifié [case] · Date de l'accouchement ·
Mode de l'accouchement [cases: Voie basse non instrumentale/Voie basse instrumentale/Forceps/Ventouse/Avec épisiotomie] ·
Césarienne [case: Programmée/Urgence] · Indication de la césarienne ·
Présence de complications [case: Au moment de l'accouchement/Suites de couches] ·
Type de complications [cases: Pré-éclampsie/Eclampsie/Hémorragie/Infection/Autres] · Si autres, préciser ·
État du nouveau-né [case: Vivant/Mort-né/Décès < 24 heures] · Sexe · Poids à la naissance ·
Périmètre crânien à la naissance · Anomalie à préciser · Âge gestationnel""",
 T_PRECO: """Date de la consultation · Moment [case: entre 7ème et 8ème jour / après le 8ème jour] ·
T° · TA · Pouls · Poids · État des conjonctives [case: Normales/Décolorées] · Présence du globe utérin [case] ·
État des lochies [cases: Fade/fétide/claires/sanglantes/Jaunâtres] ·
État du périnée [cases: Normal/Épisiotomie/Déchirure/Réparée] · État des sphincters [case: Normal/Anormal] ·
Césarienne [case] · État de la cicatrice · État des seins [case: Normal/lymphangite/mastite et abcès] ·
État des mollets [cases: Normal/Rouges/Chauds/Douloureux à la dorsiflexion] ·
Présence de complication [case] · Type [cases: Hémorragie/Infection/Eclampsie/Phlébite/Complications mammaires/Anémie/Autres] ·
Notion de prise de médicaments [case] + détail manuscrit · Traitement prescrit [cases: Fer/Vitamine A] · Autres à préciser ·
Prochain rendez-vous · Planification familiale : Désire utiliser une méthode [case] · Si oui laquelle [case: pilule/DIU/Autre] ·
Prescription faite [case] · Référée [case] · Si pas de méthode, pourquoi (texte)""",
 T_AUTRE: """Tous les champs renseignés visibles (valeur manuscrite ou case cochée), nom = libellé imprimé.""",
}
CHECKLISTS[T_TARDIF] = CHECKLISTS[T_PRECO].replace(
    "Moment [case: entre 7ème et 8ème jour / après le 8ème jour]",
    "Moment [case: entre 40ème et 50ème jour / après le 50ème jour]")

PROMPT_A = """Page d'un registre marocain de suivi de grossesse. Identifie :
1) type_page : le titre imprimé en haut de la page ;
2) nom_patiente : le nom manuscrit ou imprimé de la patiente s'il apparaît, sinon ""."""
SCHEMA_A = {"type": "object",
            "properties": {"type_page": {"type": "string", "enum": PAGE_TYPES},
                           "nom_patiente": {"type": "string"}},
            "required": ["type_page", "nom_patiente"]}

SCHEMA_B = {"type": "object",
            "properties": {"champs": {"type": "array", "items": {
                "type": "object",
                "properties": {"nom": {"type": "string"}, "valeur": {"type": "string"},
                               "case_cochee": {"type": "boolean"}, "confiance": {"type": "number"}},
                "required": ["nom", "valeur", "case_cochee", "confiance"]}}},
            "required": ["champs"]}

def prompt_b(page_type):
    return f"""Tu lis une page « {page_type} » d'un registre marocain de suivi de grossesse.
Voici les champs imprimés de cette page :
{CHECKLISTS[page_type]}

Pour CHAQUE champ de la liste, donne une entrée :
- valeur = ce qui est écrit à la main, ou le libellé de la case cochée d'une croix ;
- valeur = "VIDE" si le champ est laissé en blanc et qu'aucune case n'est cochée ;
- valeur = "ILLISIBLE" (confiance <= 0.3) si c'est rempli mais illisible ou masqué. Ne devine JAMAIS ;
- case_cochee = true si l'information vient d'une case à cocher ;
- confiance = ton estimation réelle entre 0 et 1 ;
- ne recopie JAMAIS une liste imprimée comme si elle était cochée : seulement les croix réellement visibles."""


def tg(method, **params):
    data = urllib.parse.urlencode(params).encode()
    return json.load(urllib.request.urlopen(f"{API}/{method}", data, timeout=90))


def _generate(prompt, img_b64, fmt, n_predict):
    body = json.dumps({"model": MODEL, "stream": False, "format": fmt, "think": False,
                       "messages": [{"role": "user", "content": prompt, "images": [img_b64]}],
                       "options": {"temperature": 0, "num_predict": n_predict, "num_ctx": 8192}}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", body, {"Content-Type": "application/json"})
    return json.loads(json.load(urllib.request.urlopen(req, timeout=900))["message"]["content"])


def extract(image_bytes):
    img = base64.b64encode(image_bytes).decode()
    t0 = time.time()
    a = _generate(PROMPT_A, img, SCHEMA_A, 150)
    page_type = a.get("type_page", T_AUTRE)
    b = _generate(prompt_b(page_type), img, SCHEMA_B, 4000)
    return {"type_page": page_type, "nom_patiente": a.get("nom_patiente", ""),
            "champs": b.get("champs", [])}, time.time() - t0


def render(d, dt):
    sur, a_confirmer, vides = [], [], 0
    for c in d.get("champs", []):
        nom, val = c.get("nom", "?"), str(c.get("valeur", ""))
        conf = float(c.get("confiance", 0) or 0)
        if val == "VIDE" or val == "":
            vides += 1; continue
        if c.get("case_cochee"):
            a_confirmer.append(f"❓ ☒ {nom} : {val}  ({conf:.0%})")
        elif conf < CONF_SEUIL or val == "ILLISIBLE":
            a_confirmer.append(f"❓ {nom} : {val}  ({conf:.0%})")
        else:
            sur.append(f"✅ {nom} : {val}")
    out = f"📄 {d.get('type_page', '?')}"
    pat = d.get("nom_patiente", "")
    if pat and pat not in ("ILLISIBLE", "VIDE"): out += f" — {pat}"
    out += f"\n🤖 {MODEL}, 100 % local · {dt:.0f} s · {vides} champs vides\n"
    if sur: out += "\n" + "\n".join(sur)
    if a_confirmer: out += "\n\n⚠️ À confirmer par la sage-femme :\n" + "\n".join(a_confirmer)
    out += "\n\n_Le registre papier reste la référence._"
    return out


def main():
    print("Bot démarré. Modèle:", MODEL)
    offset = 0
    while True:
        try:
            ups = tg("getUpdates", timeout=50, offset=offset)["result"]
        except Exception as e:
            print("poll:", e); time.sleep(3); continue
        for u in ups:
            offset = u["update_id"] + 1
            msg = u.get("message") or {}
            chat = msg.get("chat", {}).get("id")
            if not chat: continue
            if msg.get("text", "").startswith("/start"):
                tg("sendMessage", chat_id=chat, text="Envoyez la photo d'une page du registre "
                   "(une des 6 pages du dossier). Extraction 100 % locale, champ par champ.")
            elif "photo" in msg:
                tg("sendMessage", chat_id=chat, text="📷 Reçu. Extraction locale en cours…")
                try:
                    file_id = msg["photo"][-1]["file_id"]
                    path = tg("getFile", file_id=file_id)["result"]["file_path"]
                    img = urllib.request.urlopen(f"https://api.telegram.org/file/bot{TOKEN}/{path}", timeout=90).read()
                    fields, dt = extract(img)
                    texte = render(fields, dt)
                    for i in range(0, len(texte), 3500):
                        tg("sendMessage", chat_id=chat, text=texte[i:i+3500], parse_mode="Markdown")
                except Exception as e:
                    print("extraction:", repr(e))
                    tg("sendMessage", chat_id=chat, text=f"Erreur d'extraction : {e}")

if __name__ == "__main__":
    main()
