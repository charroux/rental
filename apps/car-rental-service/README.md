# Car Rental Service

API Spring Boot de gestion de voitures de location. À ce checkpoint, les
données restent en mémoire et le service ne communique pas avec le service de
tarification.

## Prérequis

- JDK 17 ou supérieur ; le bytecode produit cible Java 17
- le wrapper Gradle fourni avec le projet

## Tests

Sous Linux ou macOS :

```bash
./gradlew clean test
```

Sous Windows :

```powershell
.\gradlew.bat clean test
```

## Qualité

```bash
./gradlew checkstyleMain checkstyleTest
```

Les rapports HTML sont écrits dans `build/reports/checkstyle/`.

## Lancement

```bash
./gradlew bootRun
```

Endpoints principaux :

- `GET /health`
- `GET /cars`
- `GET /cars/{plateNumber}`
- `PUT /cars/{plateNumber}?rent=true|false`

## Limites intentionnelles

- état non persistant ;
- aucune base de données ;
- aucun appel vers `pricing-service` ;
- aucune authentification.
