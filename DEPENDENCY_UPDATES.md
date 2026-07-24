# Dependency Updates

Renovate öffnet **einen PR** (`renovate/all`) für alle Deps. Wir arbeiten auf diesem Branch, nicht direkt auf `main`.

## Workflow

Die **Version** wird immer im **letzten, eigenen Commit** gebumpt.
Davor: erst die Deps, dann ggf. spaCy.

**1. Commit: alle Deps außer spaCy + Fixes**
- Alle anstehenden Dep-Updates außer spaCy anwenden.
- spaCy auf der **alten** Version belassen (den spaCy-Bump aus dem PR zurücknehmen).
- `uv sync`, dann das Sprachmodell ziehen: `uv run python -m spacy download de_core_news_sm`.
- `uv run ruff check . && uv run mypy . && uv run pytest` müssen grün sein; nötige Fixes gehören in diesen Commit.

**2. Ist spaCy dabei?**
Falls ja, `./evaluate.sh .data` ausführen. Es zieht automatisch die neueste spaCy-Version und vergleicht sie mit der aktuell gesetzten (noch alten).
- gut genug → **Commit: spaCy updaten** (spaCy-Abhängigkeit auf die neue Version)
- nicht gut genug / nicht dabei → spaCy weglassen, **kein Commit**

*Getestet wird sm/md/lg. Auf ein größeres Modell nur wechseln, wenn neue spaCy-Version + größeres Modell ≥10% besser sind; sonst diskutieren (größere Modelle sind deutlich langsamer). Läuft im uv-Venv (Skript nutzt `uv run`/`uv pip`, nichts global).*

**3. Commit: Version setzen** (`pyproject.toml`: `version`)
- Format: `0.<minor>.<spaCy-ohne-Punkte>.<Datum>`, z. B. spaCy `3.8.14` am 24.07.2026 → `0.4.3814.20260724`.
- `<minor>` anheben statt nur Datum: bei signifikanten Änderungen oder bei einem zweiten Release am selben Tag.
