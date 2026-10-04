# DayOne — bot Telegram, extraction 100 % locale (stage 1)

Photo d'une page du registre → champs structurés avec confiance par champ. L'IA (qwen2.5vl:7b)
tourne **entièrement sur la machine** via Ollama — aucune IA cloud, contrairement à la démo du stand.

## Lancer (2 minutes)

1. Sur Telegram : parler à **@BotFather** → `/newbot` → choisir un nom → copier le token.
2. ```bash
   ollama pull qwen2.5vl:7b        # déjà fait sur ce Mac
   TELEGRAM_TOKEN=123:abc python3 bot.py
   ```
3. Envoyer une photo du registre au bot (tester avec `Datasets/dayone-participants/data/Paper Registry/`).

## Comportement clé (aligné sur la grille d'évaluation)

- **Extraction** : champs texte lus avec confiance mesurée (~56 s/page sur ce Mac, bien plus vite sur GPU).
- **Incertitude** : champ masqué ou illisible → `ILLISIBLE`, jamais deviné (testé sur la photo réelle au nom couvert).
- **Deux passes** : passe 1 = champs texte sous schéma JSON forcé (confiances incluses); passe 2 = cases à
  cocher avec prompt anti-hallucination. ~20 s/page une fois le modèle chaud.
- **Cases à cocher** : point faible connu des VLM (encore halluciné sur la photo réelle difficile) →
  **jamais auto-acceptées, toujours « à confirmer »** par la sage-femme. Stage 2 : recadrer la zone des cases
  avant la passe 2, et boutons ✅/✏️ de revue conversationnelle.
- **Hors-ligne** : le client Telegram met les photos en file d'attente sans signal (démo : mode avion).
- **Limite assumée (à dire en présentation)** : Telegram est le transport de la **démo**. L'API WhatsApp Business
  ne peut pas pointer vers un modèle local — c'est la limitation que DayOne demande d'expliquer. En production :
  PWA type WhatsApp auto-hébergée sur le réseau local de la clinique (~2 000 $ de matériel), rien ne sort du bâtiment.

## Mesuré (probe du 3 oct, voir ../PROBE.md)

Spécimen : 9/9 champs exacts. Photo réelle : région/province/établissement corrects (écriture manuscrite),
nom masqué correctement refusé; cases à cocher hallucinées → d'où la règle « toujours confirmer ».
