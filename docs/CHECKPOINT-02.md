# Checkpoint 02 — chaîne de production logicielle

## Intention pédagogique

Une image qui porte le bon nom peut avoir été remplacée, construite ailleurs ou
modifiée après la CI. Ce checkpoint associe le livrable à un digest immuable et
produit des preuves vérifiables sur son contenu et son origine.

## Contenu

- toutes les actions GitHub tierces sont épinglées à un commit complet ;
- les images de base Docker combinent un tag lisible et un digest immuable ;
- Dependabot suit les commits d'actions et les digests Docker ;
- le graphe de dépendances et les alertes de vulnérabilités GitHub sont activés ;
- une revue des dépendances bloque les nouvelles vulnérabilités élevées ;
- Syft produit un SBOM SPDX JSON pour chaque image publiée ;
- Cosign signe chaque digest avec l'identité OIDC du workflow ;
- GitHub atteste la provenance du build et le SBOM ;
- Trivy analyse le même digest que celui qui est signé et attesté ;
- le workflow vérifie signature et attestations avant de réussir ;
- une politique locale détecte les références mutables.

## Chaîne de confiance

```text
sources Git + workflow identifié
              |
              v
       image@sha256:digest
          /       |       \
   signature   provenance   SBOM SPDX
          \       |       /
              vérification
```

Le tag `latest` reste pratique pour l'humain, mais aucune preuve ne le prend
comme sujet. Signature, SBOM, attestation et scan portent tous sur le digest
produit par Buildx.

## Critères d'acceptation

En local :

```bash
python scripts/course.py verify
python scripts/course.py supply-chain-policy
```

Sur une pull request :

- `Dependency review` est présent ;
- aucune action ne référence un tag ou une branche ;
- les deux images se construisent avec leurs bases épinglées.

Après intégration sur `main` :

- `Java supply chain` et `Python supply chain` réussissent ;
- les SBOM sont téléchargeables comme artefacts ;
- GHCR contient les signatures et attestations OCI ;
- la commande `gh attestation verify` accepte chaque image par digest ;
- Trivy téléverse un rapport SARIF pour chaque digest.

## Dette volontaire

- les dépendances transitives Python et Gradle ne sont pas encore verrouillées
  par hash ;
- aucune politique d'admission Kubernetes ne vérifie encore les signatures ;
- aucun déploiement ne promeut une image par digest entre environnements ;
- la communication inter-services, la persistance, Kind et l'E2E restent à
  traiter.

Le checkpoint suivant peut donc se concentrer sur l'intégration des services,
avant d'utiliser ces preuves lors des déploiements Kubernetes.
