# X / Twitter thread draft

> 7 tweets. Keep each under 280 chars. Attach the audit screenshot/asciinema to
> tweet 1 and the results-table image to tweet 4 if you have them.

**1/**
Does a bigger LLM explain itself better?

I built a tool to check whether a model's cited evidence is actually real and
load-bearing — then ran it on Qwen 2.5 3B vs 7B.

The bigger model is worse. 🧵

**2/**
The tool is glassbox. It makes a local LLM quote its evidence verbatim, then asks
3 questions:

• grounding: does the quote exist in the doc?
• faithfulness: erase it — does the verdict change?
• consistency: reword the doc — does the label hold?

All local, no API.

**3/**
A label can be right for a decorative reason — a fluent sentence the model wrote
*after* deciding.

glassbox measures that instead of trusting it. A verdict is "trustworthy" only
when the explanation survives all three checks.

**4/**
3B vs 7B on 40 emails, similar accuracy:

Grounded: 98% → 48%
Faithful: 45% → 18%
Trustworthy: 45% → 18%

The small model is auditable ~2.5x as often. And ~2x faster.

**5/**
Why? The 7B stops quoting verbatim — it paraphrases its "evidence", so a third of
its citations can't be found in the source.

It's also non-deterministic at temp 0: re-running the same email flipped both the
label and the citations.

**6/**
So I tried fixing the 7B with a few-shot "quote verbatim" prompt.

Grounding: 48% → 80%. Accuracy: 78% → 90%. 

But faithfulness? 18% → 20%. Trustworthiness didn't move.

It bought back locatable quotes — not load-bearing ones. Grounding ≠ faithfulness.

**7/**
MIT, pure-stdlib core, runs free on Ollama. There's a `--json` mode and a GitHub
Action that fails CI on an untrustworthy verdict.

Caveats: small corpora, few runs. Try it on bigger models and tell me if it
reproduces 👇

https://github.com/winxtxrgit/glassbox
