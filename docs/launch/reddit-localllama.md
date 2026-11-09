# r/LocalLLaMA draft

> Post as a text post to r/LocalLLaMA. This community cares about local models,
> reproducibility and honest caveats — lead with the finding, not the tool.
> A good crosspost target is r/MachineLearning (use the [P] Project flair there).

## Title

```
Qwen 2.5 7B is less auditable than the 3B on 40 emails — and a few-shot prompt fixed its grounding but not its faithfulness.
```

## Body

I built a small open-source tool (glassbox) that checks whether a local LLM's
*explanation* holds up, not just whether its label is right. It makes the model
quote its evidence verbatim, then:

- **grounds** each quote (does it actually exist in the document?),
- tests **faithfulness** by erasing the cited span and re-running (if the label
  doesn't change, the evidence was decorative), and
- tests **consistency** under meaning-preserving edits (lowercasing, whitespace,
  a forwarding wrapper).

Everything runs locally on Ollama — no API, nothing leaves the machine.

Then I compared `qwen2.5:3b` vs `qwen2.5:7b` on 40 phishing/benign/injection
emails (GTX 1650 Ti, 4 GB). Similar accuracy, very different auditability — plain
prompt:

| | 3B | 7B |
|---|---:|---:|
| Accuracy | 82% | 78% |
| Grounded | 98% | 48% |
| Faithful | 45% | 18% |
| Trustworthy (all checks) | 45% | 18% |
| ~s/doc | 43.6 | 90.5 |

**The 7B stops quoting verbatim** — it paraphrases its "evidence", so more than
half its citations can't be located in the source. It's also non-deterministic at
temp 0 (re-running the same email flipped both the label and the citations).

So I tried to fix it with a **few-shot "quote verbatim" prompt**. On the 7B it
lifted grounding **48% → 80%** and accuracy **78% → 90%** — but faithfulness barely
moved (**18% → 20%**), so trustworthiness stayed flat at 18%. The model now quotes
*correctly*, yet erasing the quote still rarely changes the verdict. It bought
back locatability, not faithfulness. (On the small 3B the longer prompt backfired
— malformed output on 13 of 40.)

**Caveats:** 40 emails, one run per cell, 7B varies run to run. Directional, not
conclusive — I'd love for people with more VRAM to try it on bigger models and
more docs and report back.

Repo (MIT, pure-stdlib core): https://github.com/winxtxrgit/glassbox
Full numbers: FINDINGS.md and benchmarks/RESULTS.md in the repo.

```bash
pip install glassbox-audit
ollama pull qwen2.5:3b
glassbox audit email.txt --model qwen2.5:3b
```
