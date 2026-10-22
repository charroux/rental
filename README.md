

# Rental API

Cette application est une petite API REST en Java avec Spring Boot pour gérer une flotte de voitures en location.

## Prérequis

- Java 17
- Gradle
- Docker

## Construire l'application

Pour compiler le projet localement :

```bash
./gradlew build
```

## Créer une image Docker

Depuis la racine du projet, exécutez :

```bash
docker build -t rental .
```

Cette commande lit le `Dockerfile`, construit l'image de production et prépare le jar généré par Gradle.

## Lancer le conteneur

```bash
docker run --rm -p 8080:8080 rental
```

- `--rm` : supprime automatiquement le conteneur quand il s'arrête
- `-p 8080:8080` : expose le port 8080 du conteneur sur le port 8080 de votre machine
- `rental` : nom de l'image créée précédemment

## Vérifier que l'application fonctionne

Une fois le conteneur démarré, vous pouvez vérifier qu'il répond :

```bash
curl http://localhost:8080/cars
```

Vous devriez obtenir une liste de voitures au format JSON.

## Exemple d'appels API

### Lister toutes les voitures

```bash
curl http://localhost:8080/cars
```

### Obtenir une voiture par plaque

```bash
curl http://localhost:8080/cars/ABC123
```

### Louer une voiture

```bash
curl -X PUT "http://localhost:8080/cars/ABC123?rent=true"
```

### Rendre une voiture

```bash
curl -X PUT "http://localhost:8080/cars/ABC123?rent=false"
```

## Remarques pédagogiques

- L'application garde son état en mémoire pendant la durée de vie du conteneur.
- Elle est volontairement simple pour illustrer les bases d'une API REST avec Spring Boot.
- Le but n'est pas d'avoir une base de données ou une logique complexe, mais de montrer le fonctionnement d'un service web minimal.
