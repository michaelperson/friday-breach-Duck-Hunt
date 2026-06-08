# Utilisation d'une image Python officielle allégée
FROM python:3.11-slim

# Empêche Python d'écrire des fichiers .pyc et force l'affichage des logs dans le terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définition du répertoire de travail
WORKDIR /workspace

# Installation des dépendances système de base (au cas où tu as besoin de télécharger des datasets)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie du fichier des dépendances et installation
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exposition du port pour Jupyter Lab
EXPOSE 8888

# Commande par défaut : lancement de Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token='duckdb'"]