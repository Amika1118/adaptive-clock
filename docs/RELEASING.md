# Releasing a new version (for maintainers)

A GitHub **Release** is the page people download from. This repository builds it for you when you push a version tag.

1. Make sure the version is right: `Version=` in `tools/gen_ini.py` (then run `python gen_ini.py && python gen_skins.py && python check_ini.py` in `tools`)
   and add a `## <version>` section at the top of `CHANGELOG.md`. The tag below must match the version (tag `v5.0` = `Version=5.0`).
2. Commit and push:
   ```
   git add -A
   git commit -m "Release 5.0"
   git push
   ```
3. Tag it and push the tag:
   ```
   git tag v5.0
   git push origin v5.0
   ```
4. Open the **Actions** tab: the *Release* workflow checks the files, builds `AdaptiveClock-5.0.rmskin` and publishes the release with the text of your
   `CHANGELOG.md` section. A minute later it appears under **Releases**, where people download the `.rmskin`.

Without the workflow: build the package with `python tools/build_rmskin.py`, then on GitHub choose **Releases > Draft a new release**, create the tag
`v5.0`, paste the changelog section, drag in `dist/AdaptiveClock-5.0.rmskin` and press **Publish release**.

Bug reports and ideas arrive as **Issues** (the templates are in `.github/ISSUE_TEMPLATE`).
