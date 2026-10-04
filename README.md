# DayOne — The Offline Midwife · CodeML 2026

**Un bot de messagerie + une IA 100 % locale** qui transforment la photo d'une page du registre
papier marocain de suivi de grossesse en données structurées — champ par champ, avec confiance,
et confirmation par la sage-femme. Le registre papier reste la référence ; rien ne part vers une
IA cloud.

## Démo

Bot Telegram : envoyez la photo d'une page du carnet → le type de page est identifié
(en-tête, identification, grossesse, accouchement, post-partum précoce/tardif), puis chaque champ
de CE type de page est extrait : valeur ✅ si confiance haute, **« à confirmer » ❓** pour toute
case à cocher et toute lecture incertaine, `ILLISIBLE` plutôt qu'une invention (testé sur un nom
masqué par un papier). Lancement : [`bot/README.md`](bot/README.md) — 2 minutes, aucune dépendance
Python externe.

## Pourquoi local, pourquoi Telegram

- **Vie privée + coût** (priorités DayOne) : l'extraction tourne sur la machine via Ollama
  (`qwen2.5vl:7b`, 6 Go). Un boîtier GPU ~2 000 $ par clinique ≈ **100+ pages/h**, données sur place.
- **Telegram = transport de la démo.** L'API WhatsApp Business ne peut pas pointer vers un modèle
  local — c'est la limitation que DayOne demande d'expliquer. En production : PWA type WhatsApp
  auto-hébergée sur le réseau de la clinique. Le client Telegram met nativement les photos en file
  d'attente hors-ligne (démo : mode avion).

## Ce qui est mesuré, pas affirmé

- [`PROBE.md`](PROBE.md) — validation initiale + **comparaison qwen2.5vl:7b vs Gemma 4 12B**
  (le 7B spécialiste documents bat le 12B généraliste : fidélité des chiffres manuscrits,
  pas d'écho d'étiquettes, 2-5× plus rapide ; thinking de Gemma 4 désactivé obligatoire).
- [`AUDIT_20_PAGES.md`](AUDIT_20_PAGES.md) — **audit croisé de 20 pages** (annotateur indépendant +
  couche texte du PDF comme arbitre) : **≈ 96 % des champs extraits corrects** sur les pages
  standard, et six modes d'échec nommés (taxonomie mère/nouveau-né, colonnes de grilles,
  multi-sélection, classification des photos réelles…) avec correctifs chiffrés.
  Détail par page : `bot/results/batch20/`.

## Architecture

```
photo Telegram ─► classification du type de page (passe A, locale)
             ─► extraction sous CHECKLIST du type (passe B, schéma JSON forcé, confiance/champ)
             ─► rendu : ✅ sûrs · ❓ cases + incertitudes « à confirmer » · ILLISIBLE jamais deviné
```

`bot/bot.py` (stdlib uniquement) · `bot/eval_compare.py` (banc multi-modèles) ·
`bot/batch20.py` (batch de l'audit).

## Limites connues (voir l'audit)

Pages NOUVEAU-NÉ hors taxonomie v3 (correctif : 2 checklists), colonnes des tableaux de visites
écrasées, seules les cases cochées en premier d'un groupe multi-sélection sont retenues,
précision réduite sur l'écriture manuscrite réelle. Étapes suivantes : stockage chiffré SQLite,
boutons ✅/✏️ de correction, liaison des visites par n° de fiche.

## Outils

Python (stdlib), Ollama, qwen2.5vl:7b / gemma4:12b. Dataset : package participant DayOne
(spécimens fictifs). Assistance IA : Claude (Anthropic) pour le développement et l'audit croisé.
