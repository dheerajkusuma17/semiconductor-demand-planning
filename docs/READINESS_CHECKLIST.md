# Day 0 Readiness Checklist

Nothing in the project starts until every box is ticked. Status as of **2026-11-06**.

## A. Tools
- [x] Python 3.11.4, Git 2.56, GitHub CLI (signed in as `dheerajkusuma17`), VS Code installed
- [x] Git identity set (Dheeraj Kumar Kusuma)
- [x] `.venv` created and `pip install -r requirements.txt` succeeded (versions frozen in `requirements-lock.txt`)
- [x] `python scripts/check_env.py` → **34/34 PASS**
- [x] Jupyter kernel "Semiconductor DP (.venv)" registered
- [x] VS Code extensions: Python, Jupyter, Pylance, Rainbow CSV, GitLens, Data Wrangler
- [x] GitHub repo created and first commit pushed: https://github.com/dheerajkusuma17/semiconductor-demand-planning
- [ ] **You:** Power BI Desktop installed and opens `data/sample/powerbi_test.csv`
- [ ] **You:** Streamlit Community Cloud account linked to GitHub

## B. Data
- [x] `python scripts/download_data.py` → Intel dataset (26,114 rows, 86 SKUs, 5 DCs, 187 weeks) + 3 FRED series downloaded and validated

## C. Skills
- [x] `notebooks/00_prerequisites_bootcamp.ipynb` runs top to bottom
- [ ] **You:** completed the 5 bootcamp exercises

## D. Concepts
- [ ] **You:** read `docs/CONCEPTS_PRIMER.md` and `docs/INDUSTRY_PRIMER.md`
- [ ] **You:** concept quiz score ≥ 12/15 (or gaps reviewed)

## E. Never-lose-anything setup
- [x] `CLAUDE.md`, `docs/PROGRESS_LOG.md`, `docs/DECISIONS_LOG.md`
- [x] `/checkpoint` command (`.claude/skills/checkpoint/SKILL.md`)
- [ ] `/checkpoint` run once to commit Day 0 (after your items above)
