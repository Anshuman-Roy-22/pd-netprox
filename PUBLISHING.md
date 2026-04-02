# Publishing Checklist

## Tasks already automated in this repository

- Canonical pipeline order is documented and scripted in `scripts/run_pipeline.py`.
- Repository validation is scripted in `scripts/verify_repository.py`.
- SHA256 checksums are scripted in `scripts/update_checksums.py`.
- Large local-only raw files and non-canonical outputs are excluded by `.gitignore`.
- A GitHub Actions sanity check is configured in `.github/workflows/repo-check.yml`.

## Tasks you should do manually

1. Review the included `LICENSE` file and replace it only if you want a different license.
2. Review redistribution terms for every tracked external-data file before making the repository public.
3. Create the GitHub repository in the web UI.
4. Add the remote and push:

```powershell
git remote add origin https://github.com/<your-user>/pd-netprox.git
git push -u origin main
```

5. If you want citation metadata on GitHub, add a real `CITATION.cff` with authors, title, version, and DOI once you have them.
6. If this repository supports a paper or public release, create a GitHub Release and archive it on Zenodo.

## Recommended manual review before push

- Open `README.md` and confirm the project description matches the paper or analysis you want to show publicly.
- Decide whether the tracked GTEx and STRING files are acceptable to redistribute in GitHub.
- Review `scripts/legacy/` once before publication and delete anything you do not want to expose publicly as historical work.
