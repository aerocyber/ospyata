# Welcome, contributors

## Pull Request Rule

Rule: `All PRs must be against the ``dev`` branch.`

Monitoring: `Strict`

Refusal: `Denial of merge even if the code is too urgent.`

Exceptions: `Security updates can be done directly against the appropriate branch(es).`

## Recommended start

Type: `Guideline`

Monitoring: `N/A`

Guideline:

Clone the repository:

```bash
git clone https://github.com/aerocyber/ospyata
```

Checkout a new branch, say, feature-x:

```bash
git checkout -b feature-x
```

Do all dev works and commit, push:

```bash
git commit -m 
git push -u origin <branch to push to>
```

### Formatting

The preferred formatter is `autopep8`.
