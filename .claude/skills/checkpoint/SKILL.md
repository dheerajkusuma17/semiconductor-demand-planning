---
name: checkpoint
description: End-of-phase checkpoint for the Semiconductor Demand Planning project. Verifies the environment, re-runs the phase's notebooks top to bottom, quizzes the owner with the phase's checkpoint questions, records answers in docs/LEARNING_GUIDE.md, updates docs/PROGRESS_LOG.md, then commits and pushes so nothing is ever lost. Use when the user types /checkpoint or says a phase/day is finished.
---

# /checkpoint: close out a project phase safely

Optional argument: the phase name, e.g. `/checkpoint Day 2`. If none is given, read the latest entry in `docs/PROGRESS_LOG.md` to tell which phase is in progress.

## Steps

1. **Environment check.** Run `.\.venv\Scripts\python.exe scripts/check_env.py`. If anything fails, stop and fix it first.

2. **Re-run the phase's notebooks** from a clean state, so results are reproducible:
   ```powershell
   .\.venv\Scripts\jupyter.exe nbconvert --to notebook --execute --inplace notebooks/<NN_name>.ipynb
   ```
   Run every notebook touched in this phase, plus `pytest` if `tests/` has tests. Report any failure and fix it before continuing.

3. **Results summary.** List the key numbers this phase produced (accuracy, bias, p-values, safety stock, etc.), exactly as the notebooks printed them. **Never invent or round numbers in a misleading way.** Log any new assumptions in `docs/DECISIONS_LOG.md`.

4. **Checkpoint quiz.**
   - Take the 3–5 checkpoint questions from the end of the phase's notebook(s).
   - Ask the owner with AskUserQuestion, or in chat for open questions. Ask one batch and wait for the answers.
   - Give short, kind feedback: what is right, and what to revisit, pointing to the notebook section.
   - Append to `docs/LEARNING_GUIDE.md` under `## <Phase>`: each question, the owner's answer, the model answer, and one interview-style follow-up question.

5. **Update `docs/PROGRESS_LOG.md`.** Add a new entry at the top with the date (absolute, YYYY-MM-DD), the phase, Done / Key results / Next / Open questions.

6. **Commit and push.**
   - `git add -A`, then check `git status` for anything that shouldn't be committed: data/raw files, secrets, large binaries over 50 MB.
   - Commit message: `Checkpoint: <phase> - <one-line summary>`, ending with the attribution trailer the session specifies.
   - `git push`. If the remote doesn't exist yet, stop and ask the owner before creating a public repo.

7. **Report.** Give a short recap: what was saved, the commit hash, the GitHub link, and what the next phase is.
