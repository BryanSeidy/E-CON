# Roadmap d'exécution produit — E-CON

## Synthèse d'audit

Le backend Django REST expose déjà les domaines centraux : authentification JWT, dashboard par rôle, institutions/départements, entreprises/membres, offres, candidatures, stages, documents, journaux hebdomadaires, évaluations et notifications. Le frontend Vue consommait partiellement ces APIs : dashboard, offres, candidatures et stages étaient branchés, tandis que documents, journaux, évaluations et notifications existaient côté backend mais restaient non exploités côté UI. Les pages `profile` et `university-students` restent non connectables sans endpoint backend dédié.

## Modules incomplets détectés

- `accounts`, `ai_matching`, `analytics` et `audit` contiennent des packages API vides : pas de serializers/views/routes métier exposés.
- `profile` et `university-students` sont des vues frontend sans endpoint REST disponible.
- Les parcours documents, weekly logs, évaluations et notifications étaient des endpoints disponibles mais sans écran exploitable complet.

## Placeholders et mocks détectés

- Page générique `PlaceholderPage.vue` utilisée par la majorité des routes produit.
- Aucune donnée mockée structurante détectée dans le frontend ; les limitations sont affichées quand l'API n'existe pas.
- Les mentions de `unittest.mock` sont limitées aux tests backend.

## Pages non connectées ou partiellement connectées

- Non connectées faute d'API : profil utilisateur, liste des étudiants université.
- Partiellement connectées avant ce sprint : documents, journaux hebdomadaires, évaluations, notifications.
- Connectées : dashboard, offres, candidatures, stages.

## Endpoints non exploités côté frontend avant ce sprint

- `GET /api/v1/documents/`, actions `approve`, `reject`.
- `GET/POST /api/v1/weekly-logs/`.
- `GET/POST /api/v1/evaluations/`.
- `GET /api/v1/notifications/`, action `read`.
- Endpoints institutions, départements et company-memberships restent surtout administratifs et à intégrer selon besoins P2/P5.

## Backlog priorisé

| Priorité | Tâche | Impact utilisateur | Dépendances | Estimation |
| --- | --- | --- | --- | --- |
| P0 | Corriger la compatibilité TypeScript 6 du frontend | Débloque typecheck/build et livraison CI | `tsconfig.json` | 0.25 j |
| P0 | Connecter les pages documents, journaux, évaluations, notifications aux APIs existantes | Supprime les écrans inutilisables sur des fonctionnalités production | Clients API existants | 1 j |
| P0 | Maintenir l'affichage explicite des limites profil/étudiants | Évite formulaires fictifs et incohérences de données | Création future endpoints accounts/students | 0.25 j |
| P1 | Ajouter création de journal hebdomadaire | Permet au stagiaire de suivre son activité sans back-office | Stage existant | 0.5 j |
| P1 | Ajouter création d'évaluation | Permet superviseurs/entreprises de saisir les évaluations | Stage existant + permissions backend | 0.5 j |
| P1 | Ajouter actions métier document et notification | Permet validation documents et suivi notification | Endpoints action DRF | 0.5 j |
| P2 | Décomposer `PlaceholderPage.vue` en pages dédiées | Maintenance et UX plus propres | P0/P1 stabilisés | 2 j |
| P2 | Ajouter détails lisibles des relations au lieu d'UUID | Compréhension métier améliorée | Serializers enrichis ou appels complémentaires | 1 j |
| P3 | Module matching IA offres/stagiaires | Recommandations et scoring | Modèles `ai_matching`, données CV/offres | 5 j |
| P4 | Landing page SEO publique | Acquisition universités/entreprises | Design marketing, contenu | 2 j |
| P5 | Tenant isolation stricte multi-universités | Scalabilité et sécurité SaaS | Modèles institutions/accounts enrichis | 5 j |
| P5 | Observabilité/audit API | Exploitation production | Module audit, logs structurés | 3 j |

## Tâches implémentées dans ce sprint

- P0 : typecheck frontend débloqué via option de compatibilité TypeScript.
- P0/P1 : endpoints backend existants consommés côté frontend pour documents, journaux hebdomadaires, évaluations et notifications.
- P1 : formulaires de création pour journaux hebdomadaires et évaluations, actions de revue documents et lecture notifications.
