# Synthetic Git Activity Generator

This creates **clearly labeled synthetic backdated commits**, not a genuine work history.
It covers June 1 through October 19, 2026, with 1 to 8 commits per day and a varied distribution (deterministic seed).

## Prerequisites

- macOS Terminal, Python 3, and Git
- Configure your GitHub-associated commit email (check https://github.com/settings/emails), then run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-verified-github-email@example.com"
```

## Generate locally

From the directory containing `generate.py`:

```bash
python3 generate.py
cd synthetic-activity-repo
git log -1 --format=fuller
```

## Publish to GitHub (optional)

1. Create an **empty PRIVATE** repository on GitHub. Do not initialize it with a README or .gitignore.
2. In the generated repository directory, run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_PRIVATE_REPO.git
git push -u origin main
```

3. To show private contribution counts, visit your GitHub profile > Contribution settings > Private contributions.

**Note:** A private repository hides commit details from unauthorized visitors, but your contribution graph may still show contribution counts. GitHub attribution depends on a verified/associated commit email and other contribution eligibility rules. This is not an actual historical work diary.
