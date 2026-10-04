# Probe d'extraction locale — 3 oct, ~23 h

**Question posée** : un VLM local peut-il lire le registre? (condition d'entrée du défi, jamais validée avant)
**Modèle** : qwen2.5vl:7b via Ollama, Mac (CPU/MPS), `num_ctx=8192` requis, `format=json`, température 0.

| Image | Résultat | Temps |
|---|---|---|
| Spécimen p.1 (124/129 images de ce type) | **9/9 champs exacts** | 56 s |
| Photo réelle 1-1.jpg (manuscrite, nom couvert) | Région «Casa-Settat»→Casablanca-Settat ✓, province ✓, établissement ✓, **nom masqué → ILLISIBLE ✓ (ne devine pas)**; n° fiche garbled ~; type + risques cochés **hallucinés ✗** | 28 s |

**Architecture retenue (stage 1)** : extraction en deux passes — texte sous schéma JSON forcé (confiances
fiables), cases à cocher en prompt strict séparé. Sur le spécimen : texte 6/6 auto-validé + cases correctement
proposées. Sur la photo réelle : le texte reste bon, les cases restent peu fiables → règle produit : les cases
ne sont jamais auto-acceptées. Piste stage 2 : recadrage de la zone des cases avant la passe dédiée.

**Conclusions** : texte = fiable, y compris manuscrit; cases à cocher = non fiables → défaut produit : les cases
passent toujours par la confirmation de la sage-femme (c'est la « revue conversationnelle » de la grille).
Vitesse → réponse à la question d'échelle du sponsor : une box GPU ~2 000 $ ≈ 100+ pages/h, une par clinique.
