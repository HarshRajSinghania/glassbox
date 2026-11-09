# Show HN draft

> Post at https://news.ycombinator.com/submit. Keep the title under 80 chars.
> URL field → the GitHub repo. First comment is yours, posted immediately after.

## Title

```
Show HN: Glassbox – check whether a local LLM's cited evidence is real
```

## URL

```
https://github.com/winxtxrgit/glassbox
```

## First comment (post right after submitting)

I kept seeing LLMs give the right label with a reason that turned out to be
decorative — a fluent sentence written after the fact that didn't actually drive
the decision. glassbox is my attempt to measure that instead of trusting it.

It makes a local model (Ollama, no API key, nothing leaves the machine) quote its
evidence verbatim, then runs three checks:

- grounding: does each quote actually exist in the document, or did the model
  fabricate it?
- faithfulness: erase the cited span and re-run — if the label doesn't change,
  the "reason" was decorative (ERASER comprehensiveness, one citation at a time).
- consistency: re-decide after meaning-preserving edits (lowercasing, whitespace,
  a forwarding wrapper) — if the label flips, it was keying on surface form.

The thing I didn't expect: on 40 emails, Qwen 2.5 7B is noticeably *less*
auditable than the 3B at similar accuracy — it paraphrases its evidence instead
of quoting it, so grounding falls to 48% (the 3B holds 98%) and it's trustworthy
on 18% of docs vs the 3B's 45%.

Then I tried to fix it with a few-shot "quote verbatim" prompt. It lifted the 7B's
grounding 48% → 80% and sharpened accuracy and calibration — but faithfulness
stayed flat (18% → 20%), so trustworthiness didn't move at all. The model now
quotes correctly, yet erasing the quote still doesn't change the verdict. It
bought back *locatability, not faithfulness*. (Writeup and numbers in
benchmarks/RESULTS.md.)

Core is pure stdlib Python, MIT. There's also a `--json` mode, a GitHub Action
that fails CI on an untrustworthy verdict, and optional white-box lenses (logit
lens + occlusion) via transformers.

Caveats are real: small corpora, few runs, 7B is non-deterministic. Happy to hear
where the methodology is weak — and whether the 3B-beats-7B-on-auditability result
reproduces for anyone else.
