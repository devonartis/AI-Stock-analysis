# Branching Strategy

## Main Branches
- `main` - Production-ready code
- `develop` - Integration branch for features

## Feature Branches
Format: `feature/[area]-[description]`
Examples:
- `feature/ui-core-components`
- `feature/layout-setup`
- `feature/charts-integration`
- `feature/ai-chat`

## Bug Fix Branches
Format: `fix/[issue-number]-[description]`
Example: `fix/123-chart-rendering`

## Release Branches
Format: `release/[version]`
Example: `release/1.0.0`

## Branch Workflow
1. Create feature branch from `develop`
2. Develop and test feature
3. Create PR to merge into `develop`
4. After review and approval, merge to `develop`
5. Periodically merge `develop` into `main` for releases

## Commit Message Format
```
type(scope): subject

[optional body]
[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: Code change that neither fixes a bug nor adds a feature
- test: Adding missing tests
- chore: Changes to the build process or auxiliary tools

Example:
```
feat(ui): add stock chart component

- Implement TradingView lightweight charts
- Add basic price and volume display
- Include zoom controls
```
