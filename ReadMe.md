# ⚡ THE FRIDAY BREACH — Semaine 7 / 2026-06-05

*"Pourquoi monter un cluster Spark à €4000/mois quand un canard peut faire le même boulot en 0,3 secondes ?"* — L'Architecte

---

## 🕹️ MISSION CODENAME : **DUCK HUNT**

### 📡 CATÉGORIE : Data Engineering · Découverte DuckDB

**Difficulté :** ██░░░ 2/5 · **XP :** 300 · **Durée max :** 60 minutes  
**Niveau :** Débutant — aucun prérequis sauf Python et un terminal

---

## 🗺️ LE SCÉNARIO

Le service marketing vient de te balancer 3 fichiers CSV en te disant "fais-en quelque chose". Pas de base de données, pas de serveur, pas de budget. Juste toi, un terminal, et un outil que tu ne connais pas encore. Aujourd'hui tu vas découvrir **DuckDB** : une base de données analytique qui tient dans un seul fichier, s'installe en une commande, et écrase des benchmarks Spark sur ton laptop. En 60 minutes, tu vas passer de zéro à des analyses dignes d'un Data Engineer.

---

## 🛠️ INSTALLATION (5 MIN) (Ou utiliser le docker-compose du dossier infrastructure)

\# Option 1 — pip (recommandé)

pip install duckdb

\# Option 2 — CLI standalone (pas besoin de Python)

\# macOS

brew install duckdb

\# Windows → télécharger l'exe sur https://duckdb.org/docs/installation

**Vérification :**

python \-c "import duckdb; print(duckdb.\_\_version\_\_)"

\# ou

duckdb \--version

---

## 📦 LES DONNÉES DE MISSION

Crée un dossier `duck-hunt/` et télécharge ces 3 fichiers (données fictives fournies ci-dessous, copie-colle dans des fichiers `.csv`) :

### `clients.csv`

client\_id,nom,ville,segment

C001,Alice Martin,Bruxelles,Premium

C002,Bob Dupont,Paris,Standard

C003,Chloé Bernard,Lyon,Premium

C004,David Petit,Bruxelles,Standard

C005,Eva Rousseau,Paris,Premium

C006,Frank Moreau,Liège,Standard

C007,Grace Leroy,Bruxelles,Premium

C008,Hugo Simon,Paris,Standard

### `commandes.csv`

commande\_id,client\_id,date\_commande,montant,statut

O001,C001,2026-01-15,250.00,livré

O002,C002,2026-01-20,89.50,livré

O003,C001,2026-02-03,430.00,livré

O004,C003,2026-02-14,175.00,annulé

O005,C004,2026-03-01,320.00,livré

O006,C001,2026-03-10,95.00,en cours

O007,C005,2026-03-22,610.00,livré

O008,C002,2026-04-05,45.00,livré

O009,C006,2026-04-12,280.00,livré

O010,C003,2026-04-18,190.00,livré

O011,C007,2026-05-02,540.00,livré

O012,C005,2026-05-15,120.00,en cours

O013,C008,2026-05-28,75.00,livré

O014,C007,2026-06-01,380.00,livré

O015,C004,2026-06-03,210.00,en cours

### `produits_par_commande.csv`

commande\_id,produit,quantite,prix\_unitaire

O001,Laptop,1,220.00

O001,Souris,1,30.00

O002,Clavier,1,89.50

O003,Écran,1,399.00

O003,Câble HDMI,1,15.00

O003,Support,1,16.00

O005,Webcam,2,160.00

O007,Laptop,1,590.00

O007,Housse,1,20.00

O009,Clavier,1,89.50

O010,Écran,1,190.00

O011,Laptop,1,510.00

O011,Souris,1,30.00

O013,Câble HDMI,3,25.00

O014,Webcam,1,160.00

O014,Clavier,1,89.50

O015,Souris,2,60.00

---

## 🎯 LES NIVEAUX DE LA MISSION

### 🟢 NIVEAU 1 — Premier contact (15 min)

*Objectif : lire des CSV sans aucune infrastructure*

Lance Python et tape ceci :

import duckdb

\# DuckDB peut lire un CSV directement — sans import, sans CREATE TABLE

result \= duckdb.sql("SELECT \* FROM 'clients.csv'").fetchdf()

print(result)

**Que se passe-t-il ?** DuckDB a lu le CSV, inféré les types automatiquement, et retourné un DataFrame Pandas. Sans configuration. Sans serveur. Sans rien.

**Ta mission :**

- Affiche uniquement les clients du segment `Premium`  
- Compte combien il y a de clients par `ville`  
- Trie le résultat par nombre de clients décroissant

\# Piste de départ — à toi de compléter

duckdb.sql("""

    SELECT ville, COUNT(\*) as nb\_clients

    FROM 'clients.csv'

    WHERE ...

    GROUP BY ...

    ORDER BY ...

""").show()

---

### 🟡 NIVEAU 2 — Jointures et agrégations (20 min)

*Objectif : croiser les données comme un vrai Data Analyst*

DuckDB gère les jointures entre CSV comme s'il s'agissait de vraies tables.

**Mission :** Calcule le **chiffre d'affaires total par client** (uniquement les commandes avec statut `livré`), en affichant le nom du client, sa ville, son segment, et son CA total trié du plus grand au plus petit.

duckdb.sql("""

    SELECT

        c.nom,

        c.ville,

        c.segment,

        \-- TODO : somme des montants des commandes livrées

    FROM 'clients.csv' c

    \-- TODO : joindre avec commandes.csv

    WHERE ...

    GROUP BY ...

    ORDER BY ...

""").show()

**Bonus :** Ajoute une colonne `rang` qui classe chaque client par CA au sein de son segment. Cherche dans la doc DuckDB : `RANK() OVER (PARTITION BY ... ORDER BY ...)`.

---

### 🔵 NIVEAU 3 — Persistance et performance (15 min)

*Objectif : passer du mode "lecture CSV" à une vraie base de données locale*

Jusqu'ici DuckDB lisait les CSV à la volée. Maintenant tu vas créer une **base persistante** — un seul fichier `.duckdb` qui remplace ton serveur PostgreSQL pour ce type d'usage analytique.

\# Crée une base persistante (un fichier duck-hunt/analytics.duckdb)

con \= duckdb.connect("analytics.duckdb")

\# Crée les tables à partir des CSV (une seule fois)

con.execute("CREATE TABLE clients AS SELECT \* FROM 'clients.csv'")

con.execute("CREATE TABLE commandes AS SELECT \* FROM 'commandes.csv'")

con.execute("CREATE TABLE produits AS SELECT \* FROM 'produits\_par\_commande.csv'")

\# Vérifie

con.sql("SHOW TABLES").show()

con.sql("DESCRIBE commandes").show()

**Mission :** Écris une requête qui répond à cette question business :

*"Quel est le produit le plus vendu (en quantité totale) par segment client ?"*

Tu dois croiser les 3 tables. Cherche du côté des CTEs (`WITH ma_table AS (...)`) pour garder la requête lisible.

---

### 🔴 BOSS LEVEL — Export et automatisation (10 min)

*Pour ceux qui ont fini en avance*

DuckDB peut exporter directement en **Parquet**, le format de référence en Data Engineering (compression, typage fort, compatible avec tout l'écosystème data).

\# Exporte le résultat de ta meilleure requête en Parquet

con.execute("""

    COPY (

        SELECT ... \-- ta requête du niveau 3

    ) TO 'rapport\_final.parquet' (FORMAT PARQUET)

""")

\# Relis le Parquet pour vérifier

duckdb.sql("SELECT \* FROM 'rapport\_final.parquet'").show()

**Mission Boss :** Automatise tout dans un script `pipeline.py` qui :

1. Lit les 3 CSV  
2. Crée les tables dans `analytics.duckdb`  
3. Génère le rapport "produit par segment"  
4. L'exporte en Parquet  
5. Affiche un résumé dans le terminal

Lance-le avec `python pipeline.py`. Ça doit tourner de A à Z sans intervention manuelle.

---

## 💡 AIDE-MÉMOIRE DUCKDB

| Ce que tu veux faire | La commande |
| :---- | :---- |
| Lire un CSV à la volée | `SELECT * FROM 'fichier.csv'` |
| Voir les types des colonnes | `DESCRIBE ma_table` |
| Voir toutes les tables | `SHOW TABLES` |
| Compter les lignes | `SELECT COUNT(*) FROM ...` |
| Grouper et agréger | `GROUP BY col HAVING COUNT(*) > 5` |
| Trier | `ORDER BY col DESC` |
| Limiter les résultats | `LIMIT 10` |
| Rang dans un groupe | `RANK() OVER (PARTITION BY x ORDER BY y)` |
| Exporter en Parquet | `COPY (...) TO 'fichier.parquet' (FORMAT PARQUET)` |
| Afficher dans le terminal | `.show()` sur le résultat |

---

## 🏅 RÉCOMPENSES

| Niveau complété | XP | Badge |
| :---- | :---- | :---- |
| Recrue | **100 XP** | 🐣 *Le Canard Éveillé* |
| Opérative | **225 PX** | 🦆 *L'Analyste du Marais* |
|  |  | 💾 *Le Maître de la Base* |
| Boss | **300 XP** | 🏆 *Le Chasseur de Canards* |

---

## 📤 PROOF OF WORK

Dépose dans le thread :

1. **📋 Le résultat** de ta requête du Niveau 2 (screenshot ou copie du terminal).  
2. **📋 La requête SQL** du Niveau 3 — "produit le plus vendu par segment".  
3. **🎮 Difficulté ressentie :**  
   - `🟢` — Trop facile, donne-moi le vrai challenge.  
   - `🟡` — SQL me revient. DuckDB m'a surpris.  
   - `🔴` — Les jointures et moi, on a encore du chemin.  
4. **💡 Une chose** : qu'est-ce que DuckDB peut remplacer dans ton flux de travail actuel ?

---

## 🧠 LE MOT DE L'ARCHITECTE

DuckDB n'est pas un jouet. C'est ce que PostgreSQL aurait été s'il avait été conçu pour l'analytique dès le départ. Il tourne sur ton laptop, il lit du CSV, du Parquet, du JSON, il parle à Pandas, il exporte en tout. Et il est **rapide** — pas "rapide pour un truc local", rapide tout court.

Dans 6 mois, quand quelqu'un te sortira un fichier Excel de 2 millions de lignes en te demandant "tu peux analyser ça ?", tu ouvriras un terminal. Et tu souriras.

---

*— L'Architecte · The Friday Breach · Semaine 7 · 2026-06-05* *Vendredi prochain : Debrief Duck Hunt \+ on monte d'un cran avec dbt.*  
