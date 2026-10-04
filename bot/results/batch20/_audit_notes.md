# Audit en cours — notes par page (juge : Claude, vision indépendante + couche texte PDF)

Barème par champ : OK / FAUX (valeur erronée) / HALLU (vide déclaré rempli) / OMIS (rempli non extrait) / V→I (vide classé ILLISIBLE, direction sûre)

## p.01 en-tête (patiente 1) — 7 OK, 0 FAUX, 0 HALLU, 0 OMIS
Cases CSCA + Fixe ✓, section risques correctement VIDE.
## p.02 identification — 24 OK, 0 FAUX, 0 HALLU, 6 OMIS
OMIS : colonne mari des antécédents familiaux (5× RAS), Compl. nouveau-né (RAS).
Cases : Grossesse désirée cochée ✓, Consanguinité non cochée ✓, VAT=1 ✓, rubéole ✓ + date, hép. B non cochée ✓.
## p.03 grossesse (grille, 6 colonnes remplies) — ~30 OK (valeurs), 2 FAUX, ~70 cellules OMIS (colonnes)
FAUX (bavure de ligne) : « Examen au spéculum = Fermé » (ligne vide ; vient de TV état du col),
« TV bassin = Céphalique » (ligne vide ; vient de TV présentation).
Groupage B ✓ (vérifié image), Rh+ ✓. « Examen fait par » : les 6 colonnes listées ✓.
Mélange de colonnes sans étiquette (Mouvements/HU/BCF viennent du 2e trim).
## p.04 accouchement — 11 OK, 0 FAUX, 0 HALLU, 1 OMIS, 3 V→I
OMIS : case « En milieu surveillé ». V→I : indication césarienne, type complications, si autres (tous vides).
Complications NON cochées et non revendiquées ✓.
## p.05 précoce MÈRE — 17 OK, 0 FAUX, 0 HALLU, 2 OMIS
Globe utérin coché ✓ revendiqué à raison. OMIS : 2e case des groupes multi-sélection
(lochies « sanglantes », traitement « Vitamine A ») — motif systématique : qwen garde la 1re case cochée.
## p.06 précoce NOUVEAU-NÉ — découverte structurelle : page bébé hors taxonomie
Valeurs LUES correctement (37.1°C, 3485 g, 48 cm, 34 cm, Néant, 12/03/2026) mais forcées dans
le schéma mère : Taille→TA, périmètre crânien→Pouls = 2 FAUX de schéma ; « Moment » et
« pilule » = 2 HALLU de schéma ; ~10 OMIS (âge 7 j, allaitement exclusif, BCG/HB/VitD cochés,
Vu par, Décision, Traitement Néant).
## p.07 tardif MÈRE — 15 OK, 0 FAUX, 0 HALLU, ~1 OMIS (déjà validé contre PDF p.7)
Les deux cases lochies « Fade claires » capturées cette fois.
## p.08 tardif NOUVEAU-NÉ — même cascade de schéma que p.06
OK : date, T° 36.8, poids 5218 g, Néant, revenir 17/05/2026. HALLU schéma : « Moment », « pilule ».
OMIS : âge 43 j, taille 58, PC 37, **allaitement mixte** (changement réel vs exclusif), Vu par, Décision.

**Constat intermédiaire** : la taxonomie doit passer de 6 à 8 types (variantes NOUVEAU-NÉ
des deux consultations post-partum). Les « erreurs » des pages bébé sont des erreurs de
schéma, pas de vision.
