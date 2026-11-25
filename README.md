# Rental DevOps — checkpoint 02

Ce monorepo est le socle d'une formation DevOps pratique destinée à des
étudiants de master. Le checkpoint 02 sécurise la chaîne de production des
images : références immuables, nomenclatures logicielles, signatures sans clé
et attestations de provenance.

## Architecture actuelle

| Service | Technologie | Port | Responsabilité |
|---|---|---:|---|
| `car-rental-service` | Java 17, Spring Boot, Gradle | 8080 | Gestion en mémoire des voitures et locations |
| `pricing-service` | Python 3.12, FastAPI | 8000 | Calcul autonome des tarifs |

Les deux services partagent un réseau Docker. Ils ne communiquent pas encore
entre eux.

## Prérequis

- Git ;
- JDK 17 ou supérieur ;
- Python 3.12 ou une version compatible ;
- Docker avec Docker Compose.

Vérification rapide :

```bash
python scripts/course.py prerequisites
```

## Installation des dépendances Python

```bash
cd apps/pricing-service
python -m venv .venv
```

Activation sous Linux ou macOS :

```bash
source .venv/bin/activate
```

Activation sous PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Puis :

```bash
python -m pip install -r requirements-dev.txt
cd ../..
```

## Vérification locale

Depuis la racine :

```bash
python scripts/course.py verify
```

Cette commande exécute les tests Gradle et Pytest, Checkstyle, Ruff, puis la
politique locale de chaîne logicielle.
Pour diagnostiquer une étape séparément, utiliser `test`, `lint`,
`test-java`, `test-python`, `lint-java`, `lint-python` ou
`supply-chain-policy`.

## Intégration continue

Chaque pull request vers `main` déclenche huit contrôles lisibles :

- tests, qualité et construction de l'image pour le service Java ;
- tests, qualité et construction de l'image pour le service Python ;
- détection de secrets sur l'historique Git.
- revue des dépendances ajoutées ou mises à jour.

Les rapports de tests et de qualité sont conservés sept jours comme artefacts
GitHub Actions. Sur `main`, chaque image est publiée par digest dans GHCR, signée
avec Cosign, accompagnée d'un SBOM SPDX et de deux attestations GitHub, puis
analysée avec Trivy. Les workflows vérifient leurs propres preuves avant de se
terminer.

## Exécution avec Docker Compose

```bash
python scripts/course.py compose-up
python scripts/course.py smoke
```

Endpoints utiles :

```text
GET  http://localhost:8080/health
GET  http://localhost:8080/cars
GET  http://localhost:8000/health
POST http://localhost:8000/quotes
GET  http://localhost:8000/docs
```

Arrêt :

```bash
python scripts/course.py compose-down
```

## Organisation

```text
apps/                 Services applicatifs
archive/              Notes historiques conservées
course/               Présentation Quarto et travaux pratiques
docs/                 État de référence et checkpoints
infra/                Future infrastructure de test
scripts/              Commandes portables du cours
tests/                Futures suites de tests système
.github/workflows/     Pipelines CI par service et sécurité du dépôt
```

## Limites intentionnelles du checkpoint

- stockage Java uniquement en mémoire ;
- aucune communication entre les services ;
- aucune base PostgreSQL ni migration ;
- aucun test de contrat ou test E2E ;
- aucun manifeste Kubernetes ou cluster Kind ;
- dépendances transitives applicatives non verrouillées par hash ;
- aucune vérification de signature à l'admission Kubernetes.

Voir [la fiche du checkpoint](docs/CHECKPOINT-02.md), le
[support de cours](course/slides/02-supply-chain.qmd) et le
[TP 02](course/labs/tp02.qmd).

Le point de départ étudiant reste disponible sous le tag
`checkpoint/00-starter`. Les deux premières étapes validées sont publiées sous
`checkpoint/01-ci` et `checkpoint/02-supply-chain`.

L'état historique antérieur à la refonte reste disponible sous le tag
`legacy/v1-microservices`.
