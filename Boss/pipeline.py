import duckdb

def run_pipeline():
    print("Démarrage du pipeline de données DuckDB...")

    # 1. Connexion à la base persistante
    print("Connexion à la base 'analytics.duckdb'...")
    con = duckdb.connect("analytics.duckdb")

    # 2. Création des tables à partir des CSV (avec OR REPLACE pour pouvoir relancer le script)
    print("Chargement des fichiers CSV dans les tables...")
    con.execute("CREATE OR REPLACE TABLE clients AS SELECT * FROM '../data/clients.csv'")
    con.execute("CREATE OR REPLACE TABLE commandes AS SELECT * FROM '../data/commandes.csv'")
    con.execute("CREATE OR REPLACE TABLE produits AS SELECT * FROM '../data/produits_par_commande.csv'")

    # 3. Génération du rapport et export en Parquet
    print("Calcul du produit le plus vendu par segment et export vers 'rapport_final.parquet'...")
    
    requete_export = """
    COPY (
        WITH total_par_produit AS (
            -- Étape 1 : On joint les 3 tables et on somme les quantités pour les commandes livrées
            SELECT 
                c.segment,
                p.produit, 
                SUM(p.quantite) as quantite_totale
            FROM clients c
            JOIN commandes co ON c.client_id = co.client_id
            JOIN produits p ON co.commande_id = p.commande_id
            WHERE co.statut = 'livré'
            GROUP BY c.segment, p.produit
        ),
        produits_rankes AS (
            -- Étape 2 : On attribue un rang par segment basé sur la quantité totale
            SELECT 
                segment,
                produit,
                quantite_totale,
                RANK() OVER(PARTITION BY segment ORDER BY quantite_totale DESC) as rang
            FROM total_par_produit
        )
        -- Étape 3 : On ne garde que le premier de chaque segment
        SELECT 
            segment,
            produit,
            quantite_totale
        FROM produits_rankes
        WHERE rang = 1
        ORDER BY segment
    ) TO 'rapport_final.parquet' (FORMAT PARQUET)
    """
    
    # Exécution de la copie vers Parquet
    con.execute(requete_export)

    # 4. Affichage du résumé dans le terminal
    print("\nPipeline terminé avec succès ! Voici un aperçu du fichier Parquet généré :")
    con.sql("SELECT * FROM 'rapport_final.parquet'").show()

    # Fermeture propre de la connexion
    con.close()

if __name__ == "__main__":
    run_pipeline()