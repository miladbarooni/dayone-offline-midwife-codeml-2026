# Audit croisé : qwen2.5vl:7b (extraction v3) jugé par un annotateur indépendant

**Protocole.** 20 images (dossiers complets des patientes 1 et 2 = 16 pages spécimen couvrant
les 6 types, + 4 photos réelles). Extraction par le pipeline du bot (classification + checklist).
Juge : Claude (vision indépendante), avec la couche texte du PDF comme arbitre pour les valeurs
manuscrites des spécimens. Barème par champ : OK / FAUX (valeur erronée) / HALLU (déclaré rempli
alors que vide) / OMIS (rempli mais non extrait). Détail par page : `bot/results/batch20/_audit_notes.md` ;
JSON bruts : `bot/results/batch20/`. (p.15 et p.14/16 : JSON audités, image non re-vérifiée.)

## Résultat global

| Segment | Champs extraits corrects | FAUX | HALLU | OMIS notables |
|---|---|---|---|---|
| 12 pages spécimen hors bébé | ≈ 203/211 (**96 %** des champs extraits) | 8 | 1 | collapse des grilles (~140 cellules), multi-sélection |
| 4 pages spécimen NOUVEAU-NÉ | valeurs lues justes, **schéma faux** | 2 | 6 | ~38 (âge, allaitement, vaccins, décisions…) |
| 4 photos réelles | ≈ 11 champs sûrs | 4 | 6 | ~35 |

## Les 6 constats, par gravité

1. **Taxonomie incomplète (le plus grave, le plus corrigeable).** Les consultations post-partum
   existent en deux variantes : MÈRE et **NOUVEAU-NÉ** (4 pages sur 20 ; 8 types réels, pas 6).
   La checklist mère plaquée sur une page bébé produit des faux dangereux (Taille 48 cm → TA,
   périmètre crânien 34 cm → Pouls) et des hallucinations de schéma (« pilule » sur une page qui
   n'a pas de planification familiale). Correctif : 2 checklists bébé (~20 lignes).
2. **Grilles de visites : colonnes écrasées + les seuls faux chiffres du lot.** Une valeur par
   ligne (la 1re remplie), ~70 cellules perdues par grille — dont la **trajectoire hypertensive**
   de la patiente 2 (TA 151/97 → 150/88, œdèmes au 7-8e mois). Les 2 corruptions de chiffres du
   spécimen sont dans ce contexte : **« TA = 15/97 » pour 151/97** et **« BCF = 12.9 » pour 129**.
3. **Classification erronée → cascade (photos réelles).** 1-3.jpg (suite du carnet
   d'identification) classée « accouchement » : Forceps, Césarienne programmée, « Vivant »
   inventés. Une mauvaise classification est pire qu'une extraction prudente.
4. **Multi-sélection : seule la 1re case cochée survit** (4 occurrences : lochies « sanglantes »
   ×2, « Vitamine A » ×2 — cliniquement significatives).
5. **Variance de rappel entre exécutions.** Même type de page : p.02 = 24 champs, 6 omis ;
   p.10 = 13 champs, ~22 omis (table des accouchements entière, vaccinations cochées + dates,
   et « oncle » résumé en « RAS »).
6. **Photos réelles : la précision s'effondre sur l'écriture réelle** (« Dakar » inventé pour une
   adresse griffonnée, DDR 13/05 vs 19/05) — mais la discipline ILLISIBLE tient en partie
   (nom masqué par un papier → ILLISIBLE ✓, conf. 10 %).

## Ce qui est solide

Pages spécimen hors grille : en-têtes 7/7 et 9/9 (une seule hallucination de case sur 2 pages),
accouchement 11/11 deux fois (« Souffrance fœtale » comprise), consultations mère ~17/19 ;
cases à risque non cochées correctement laissées vides ; refus de deviner sur champ masqué.

## Recommandations (dans l'ordre coût/bénéfice)

1. Ajouter les 2 types NOUVEAU-NÉ (+2 checklists) — corrige 20 % des pages du registre réel.
2. Grilles : extraire **colonne par colonne** (un appel par colonne de visite, ou recadrage) ;
   c'est aussi là que naissent les corruptions de chiffres.
3. Multi-sélection : demander explicitement « liste TOUTES les cases cochées du groupe ».
4. Photos réelles : étape de classification séparée avec option « page non reconnue → mode
   prudent » (lister uniquement ce qui est lisible, aucun schéma imposé).
5. Afficher la confiance de classification ; en dessous d'un seuil, tout passe « à confirmer ».
