"""Batch qwen sur 20 images pour l'audit croisé (juge indépendant : Claude)."""
import glob, json, os, time
os.environ.setdefault("TELEGRAM_TOKEN", "dummy")
import bot

REG = "/Users/milad/Programming/Hackathon CodeML 7/Datasets/dayone-participants/data/Paper Registry"
names = []
for i in range(1, 17):                      # patients 1-2 : 16 pages spécimen
    names.append(sorted(glob.glob(f"{REG}/dossiers_specimen_10_patientes-{i:02d}*"))[0])
names += [f"{REG}/1-{j}.jpg" for j in (1, 2, 3, 4)]   # 4 photos réelles

os.makedirs("results/batch20", exist_ok=True)
for n, path in enumerate(names, 1):
    base = os.path.basename(path).split("__")[0].replace(".png","").replace(".jpg","_photo")
    out = f"results/batch20/{base}.json"
    if os.path.exists(out):
        print(f"[{n:2d}/20] {base}: déjà fait"); continue
    try:
        f, dt = bot.extract(open(path, "rb").read())
        f["_image"] = os.path.basename(path); f["_secondes"] = round(dt)
        json.dump(f, open(out, "w"), ensure_ascii=False, indent=1)
        remplis = sum(1 for c in f["champs"] if str(c.get("valeur")) not in ("VIDE",""))
        print(f"[{n:2d}/20] {base}: {f['type_page']} | {remplis} remplis | {dt:.0f}s")
    except Exception as e:
        print(f"[{n:2d}/20] {base}: ERREUR {e!r}")
print("BATCH TERMINÉ")
