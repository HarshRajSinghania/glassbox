# Good first issues

**Filed on 2026-11-09** as GitHub issues
[#2–#7](https://github.com/winxtxrgit/glassbox/issues?q=is%3Aissue+label%3A%22good+first+issue%22%2C%22help+wanted%22%2C%22research%22).
(The original draft's "`--runs N`" item was already implemented this session, so
it was not filed.) The drafts are kept below as a record; new ideas can be filed
with:

```bash
gh issue create --title "<title>" --label "good first issue,enhancement" --body "<body>"
```

---

## 1. Add a synonym-swap consistency perturbation

**Labels:** `good first issue`, `enhancement`

The consistency lens edits a document in meaning-preserving ways and checks the
verdict doesn't flip. We have lowercase, whitespace, boilerplate, punctuation,
and two Thai edits. Add one that swaps a small set of safe synonyms
(e.g. "urgent" ↔ "time-sensitive") — a verdict that flips on wording, not
meaning, is fragile.

Add the function + a `Perturbation` entry in `src/glassbox/consistency.py`
(follow `_normalize_punctuation`) and a test in `tests/test_consistency.py`.
Keep the mapping tiny and genuinely meaning-preserving, and make it a no-op when
no term is present.

---

## 2. Add a labelled corpus in another language

**Labels:** `good first issue`, `help wanted`

We ship `examples/phishing.jsonl` (English) and `examples/thai.jsonl`. Add a
third language as a JSONL of `{"id","document","label","category"}` rows,
balanced between phishing/benign. No GPU or model needed — this is just data.
Bonus: add the matching numeral/particle perturbation for that language if it
has one (see the Thai edits in `consistency.py` as a template).

---

## 3. Text reliability diagram in `calibrate` output

**Labels:** `good first issue`, `enhancement`

`glassbox calibrate` prints ECE/Brier and a per-bin table. Add a small ASCII
reliability diagram (confidence bin vs. observed accuracy) under the table so
over/under-confidence is visible at a glance. Keep it ASCII-only (the CLI runs on
consoles that choke on fancy glyphs). Render logic in `cli.py`, with a unit test
on the string it produces.

---

## 4. Export benchmark/calibration results to CSV

**Labels:** `good first issue`, `enhancement`

`benchmarks/run_benchmark.py` prints a Markdown table. Add a `--csv PATH` option
that also writes the rows as CSV, so results are easy to chart or diff across
runs. Pure stdlib (`csv` module). Add a test that the file is written with the
expected header.

---

## 5. Allow a custom base URL for the OpenAI-compatible backend

**Labels:** `enhancement`, `help wanted`

`OpenAICompatBackend` targets OpenRouter/Groq. Let users point it at a local
OpenAI-compatible server (llama.cpp `server`, LM Studio, vLLM) by accepting a
`--base-url` on the CLI and threading it through `_make_backend` in `cli.py`.
Document it in the README backends section. Keep API-key handling env-only.

---

## 6. ~~`--runs N` for the benchmark to measure non-determinism~~ (done)

Implemented in this session — `benchmarks/run_benchmark.py` has `--runs N` with a
mean + min-max spread table. Not filed.

---

## 7. Pin down *why* `--prompt few-shot` doesn't improve faithfulness

**Labels:** `help wanted`, `research`

The plain-vs-few-shot comparison is already in `benchmarks/RESULTS.md`: on the 7B,
few-shot lifts grounding 48% → 80% but leaves faithfulness flat (18% → 20%) and
trustworthiness unchanged. The open question is *why* the now-verbatim citations
still aren't load-bearing. Pick a handful of 7B few-shot verdicts that are grounded
but unfaithful, run `glassbox probe <file> --model qwen2.5:7b --prompt few-shot`,
and characterise what the model quotes versus what actually carries the signal.
A short writeup (or a prompt tweak that moves faithfulness) is the payoff.
