# Profile README blurb (draft)

A "featured project" card for your GitHub **profile** README
(`github.com/winxtxrgit/winxtxrgit` → `README.md`). Three lengths — paste the one
that fits. Tweak the voice to yours before publishing.

---

## Short (one-liner for a "Projects" list)

```markdown
- **[glassbox](https://github.com/winxtxrgit/glassbox)** — explainable LLM triage that cites its evidence and checks whether the explanation is actually *faithful*. Local, free, zero-dependency. `pipx install glassbox-audit`
```

---

## Medium (a featured-project card)

```markdown
### 🔍 [glassbox](https://github.com/winxtxrgit/glassbox)

An LLM will hand you a confident reason for its decision — glassbox checks whether
that reason is *real*. It makes a local model quote its evidence verbatim, then
tests whether the quote exists (grounding), whether erasing it changes the verdict
(faithfulness), and whether the decision survives meaning-preserving edits
(consistency). Runs free on Ollama, zero third-party dependencies.

**Finding:** across 40 emails, a few-shot prompt lifted Qwen 7B's grounding 48% → 80%
but left faithfulness flat — grounding is not faithfulness.

`pipx install glassbox-audit` · MIT
```

---

## Long (card with a visual + badges)

```markdown
### 🔍 [glassbox](https://github.com/winxtxrgit/glassbox) — does your LLM's *reason* hold up?

![CI](https://github.com/winxtxrgit/glassbox/actions/workflows/ci.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/glassbox-audit?color=0e75b6)
![MIT](https://img.shields.io/badge/license-MIT-0e75b6)

LLMs give confident explanations that are often decorative — a fluent sentence
written *after* the decision. glassbox measures that instead of trusting it: the
model must quote its evidence verbatim, then four lenses check whether the quote
is real, load-bearing, stable, and well-calibrated. Local + free on Ollama, pure
standard-library core.

<p align="center">
  <img src="https://raw.githubusercontent.com/winxtxrgit/glassbox/main/benchmarks/fewshot-7b.png" width="560" alt="Few-shot recovers the 7B's grounding, not its faithfulness">
</p>

I used it to find something I didn't expect — a few-shot prompt recovered Qwen 7B's
grounding (48% → 80%) without moving its faithfulness at all. **Grounding is not
faithfulness.** Writeup: [benchmarks/RESULTS.md](https://github.com/winxtxrgit/glassbox/blob/main/benchmarks/RESULTS.md).

`pipx install glassbox-audit`
```

> Note: the PyPI badge and `pipx install` line only resolve once 0.8.0 is actually
> published (see `docs/PUBLISHING.md`). Until then they'll show "not found" — post
> the blurb after the first release, or drop the install line for now.
