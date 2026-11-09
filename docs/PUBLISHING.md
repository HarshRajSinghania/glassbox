# Publishing glassbox to PyPI

glassbox publishes to PyPI with **Trusted Publishing** (OIDC) — GitHub Actions
proves the repo's identity to PyPI, so there is **no API token** stored anywhere.
The [`publish.yml`](../.github/workflows/publish.yml) workflow builds the package
and uploads it whenever a GitHub **release** is published.

The distribution is named **`glassbox-audit`** (`glassbox` is taken on PyPI by an
unrelated project); the import package and the `glassbox` command are unchanged.

## One-time setup (before the very first publish)

These two steps only need to be done once, by the repo owner.

### 1. Create the PyPI *pending* publisher

Because `glassbox-audit` does not exist on PyPI yet, you register a **pending
publisher** — it both authorises the workflow *and* reserves the name, and the
first successful run creates the project.

1. Sign in at [pypi.org](https://pypi.org) (an account with **2FA enabled** — PyPI
   requires it for uploads). Create the account first if you don't have one.
2. Go to **Account settings → Publishing**, or directly:
   <https://pypi.org/manage/account/publishing/>.
3. Under **"Add a new pending publisher"**, choose **GitHub** and fill in exactly:

   | Field | Value |
   |---|---|
   | PyPI Project Name | `glassbox-audit` |
   | Owner | `winxtxrgit` |
   | Repository name | `glassbox` |
   | Workflow name | `publish.yml` |
   | Environment name | `pypi` |

   These must match the workflow character-for-character — a mismatch makes the
   upload fail with "not a trusted publisher".
4. Click **Add**. You now have a pending publisher; no token, nothing to copy.

> Optional dry run: register the same pending publisher on
> [TestPyPI](https://test.pypi.org/manage/account/publishing/) and add a
> `repository-url: https://test.pypi.org/legacy/` step to a copy of the workflow if
> you want to rehearse against TestPyPI first. Not required.

### 2. Create the GitHub `pypi` environment

The workflow runs in a GitHub environment called `pypi`. Create it so you can
(optionally) gate releases behind a manual approval:

1. Repo → **Settings → Environments → New environment** → name it exactly `pypi`.
2. Leave it with no secrets (Trusted Publishing needs none). Optionally add
   **Required reviewers** (yourself) — then every publish pauses for your one-click
   approval in the Actions run. Leave it unprotected for fully automatic publishes.

## Publishing a release (every time)

1. Make sure `main` is green and the version is right. The version comes from
   `__version__` in [`src/glassbox/__init__.py`](../src/glassbox/__init__.py)
   (currently **0.8.0**) — the git tag you create must match it.
2. Move the `## Unreleased` notes in [`CHANGELOG.md`](../CHANGELOG.md) under a new
   `## 0.8.0 — YYYY-MM-DD` heading, and commit.
3. Cut the release — this is what triggers `publish.yml`:

   ```bash
   gh release create v0.8.0 \
     --title "v0.8.0" \
     --notes-file RELEASE_NOTES.md   # or --notes "..." / --generate-notes
   ```

   (Or GitHub UI → **Releases → Draft a new release** → tag `v0.8.0` → Publish.)
   The tag is created on whatever `main` points at, so push your commits first.
4. Watch it upload:

   ```bash
   gh run watch "$(gh run list --workflow=publish.yml --limit 1 --json databaseId -q '.[0].databaseId')"
   ```

   If you gave the `pypi` environment required reviewers, approve the run when it
   pauses.
5. Verify it landed:

   ```bash
   pipx run glassbox-audit demo     # or: pip install glassbox-audit
   ```

   and check <https://pypi.org/project/glassbox-audit/>.

## Notes & gotchas

- **Versions are immutable on PyPI.** You cannot re-upload `0.8.0`; a fix needs a
  new version (bump `__version__`, new tag). The build already pins
  `hatchling>=1.27,<1.28` so the metadata stays twine-compatible.
- **The artifact has been verified locally.** `python -m build` + `twine check
  --strict` pass, the wheel installs to `glassbox 0.8.0`, and it ships `py.typed`.
  So the first publish should be mechanical once the pending publisher exists.
- **No token ever.** If anything asks you for a PyPI API token, something is
  misconfigured — Trusted Publishing is token-free by design.
