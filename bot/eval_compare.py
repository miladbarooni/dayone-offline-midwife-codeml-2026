"""Compare les modèles VLM locaux sur 3 pages types du registre (v3, checklists).

Usage:  python3 eval_compare.py qwen2.5vl:7b [gemma4:12b ...]
Écrit results/<modele>__<page>.json et affiche un tableau récapitulatif.
"""
import glob, json, os, sys, time

os.environ.setdefault("TELEGRAM_TOKEN", "dummy")
import bot

REG = "/Users/milad/Programming/Hackathon CodeML 7/Datasets/dayone-participants/data/Paper Registry"
PAGES = {  # patient 1 : en-tête, post-partum tardif ; patient 4 : tableau de visites
    "entete": f"{REG}/dossiers_specimen_10_patientes-01.png",
    "tardif": sorted(glob.glob(f"{REG}/dossiers_specimen_10_patientes-07*"))[0],
    "grille": sorted(glob.glob(f"{REG}/dossiers_specimen_10_patientes-27*"))[0],
}
os.makedirs("results", exist_ok=True)
rows = []
for model in sys.argv[1:] or ["qwen2.5vl:7b"]:
    bot.MODEL = model
    for page, path in PAGES.items():
        try:
            f, dt = bot.extract(open(path, "rb").read())
            champs = f.get("champs", [])
            remplis = [c for c in champs if str(c.get("valeur")) not in ("VIDE", "")]
            illis = [c for c in remplis if c.get("valeur") == "ILLISIBLE"]
            json.dump(f, open(f"results/{model.replace(':','_').replace('/','_')}__{page}.json", "w"),
                      ensure_ascii=False, indent=1)
            rows.append((model, page, f.get("type_page", "?"), len(champs), len(remplis), len(illis), round(dt)))
            print(f"[ok] {model} {page}: type={f.get('type_page')!r} champs={len(champs)} "
                  f"remplis={len(remplis)} illisibles={len(illis)} {dt:.0f}s")
        except Exception as e:
            rows.append((model, page, f"ERREUR {e}", 0, 0, 0, 0))
            print(f"[ERREUR] {model} {page}: {e!r}")

print("\nmodèle | page | type détecté | champs | remplis | illisibles | s")
for r in rows:
    print(" | ".join(str(x) for x in r))
