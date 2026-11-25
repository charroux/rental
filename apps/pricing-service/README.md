# Pricing Service

Service Python/FastAPI autonome fournissant un calcul de tarif déterministe.
Le service Java ne l'appelle pas encore : cette intégration sera réalisée dans
un checkpoint ultérieur.

## Installation locale

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Qualité

```bash
python -m ruff check app tests
python -m ruff format --check app tests
```

## Lancement

```bash
uvicorn app.main:app --reload --port 8000
```

Endpoints disponibles :

- `GET /health`
- `POST /quotes`
- `GET /docs` pour l'interface OpenAPI

Exemple :

```bash
curl -X POST http://localhost:8000/quotes \
  -H "Content-Type: application/json" \
  -d '{"category":"standard","days":3}'
```
