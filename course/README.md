# Support de cours Quarto

Ce projet Quarto rassemble les supports qui accompagnent les checkpoints
techniques. Les deux premiers modules portent sur l'intégration continue et la
sécurisation de la chaîne de production logicielle.

## Prévisualiser

```bash
quarto preview course
```

## Construire

```bash
quarto render course
```

La sortie HTML est créée dans `course/_site/` et n'est pas versionnée.

## Contenu

- `slides/01-ci.qmd` : présentation du module 01 ;
- `labs/tp01.qmd` : TP guidé du module 01 ;
- `slides/02-supply-chain.qmd` : présentation du module 02 ;
- `labs/tp02.qmd` : TP guidé, critères d'acceptation et prolongements du module 02.
