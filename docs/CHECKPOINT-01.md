# Checkpoint 01 — boucle d'intégration continue

## Intention pédagogique

Ce checkpoint transforme la CI minimale du socle en boucle de retour exploitable.
Un étudiant doit pouvoir relier chaque job à un risque, reproduire les contrôles
en local et diagnostiquer un échec sans relancer la pipeline à l'aveugle.

## Contenu

- jobs distincts pour tests, qualité et image Docker de chaque service ;
- Checkstyle pour Java et Ruff pour Python ;
- rapports de tests et de qualité publiés comme artefacts ;
- caches Gradle, pip et Docker Buildx ;
- détection de secrets sur l'historique Git avec Gitleaks ;
- publication dans GHCR et analyse Trivy uniquement après intégration sur `main` ;
- annulation des exécutions obsolètes d'une même branche ;
- commandes locales regroupées dans `scripts/course.py`.

Les workflows applicatifs ne filtrent pas les chemins sur `pull_request`. Ainsi,
les contrôles requis existent toujours sur une PR, même lorsqu'un seul service
change. Le filtrage reste actif sur les pushes vers `main` afin d'éviter les
reconstructions inutiles.

## Critères d'acceptation

Depuis un environnement où les dépendances de développement sont installées :

```bash
python scripts/course.py verify
```

Une pull request vers `main` doit présenter les contrôles suivants :

- `Java tests` ;
- `Java quality` ;
- `Java Docker image` ;
- `Python tests` ;
- `Python quality` ;
- `Python Docker image` ;
- `Secret detection`.

Les jobs Docker ne commencent qu'après succès des tests et de la qualité. Les
rapports doivent rester téléchargeables, y compris lorsqu'un contrôle échoue.

## Dette volontaire pour les checkpoints suivants

- les actions ne sont pas encore épinglées par SHA ;
- Trivy utilise encore une référence de branche ;
- aucune SBOM, signature ou attestation de provenance ;
- aucune communication inter-services ni test de contrat ;
- aucune persistance, aucun volume et aucun déploiement Kind ;
- aucun test E2E dans un environnement éphémère.

Cette frontière permet au checkpoint 02 de traiter la supply chain sans mélanger
les objectifs avec les fondamentaux de la CI.
