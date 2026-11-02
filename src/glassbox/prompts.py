"""The instruction that turns a chat model into an auditable classifier.

The prompt pins the model to a fixed JSON shape and — crucially — demands that
every evidence string be copied **verbatim** from the document. That demand is
what makes the output checkable: :mod:`glassbox.grounding` can then confirm each
quote exists, and a model that paraphrases instead of quoting convicts itself.
"""

from __future__ import annotations

from .schema import Policy

# The instruction styles build_prompts understands. "plain" states the rules;
# "few-shot" also shows worked verbatim-quoting examples.
PROMPT_STYLES = ("plain", "few-shot")

# A security-triage default that fits a log/email/document pipeline. Swap it for
# any Policy with your own question and labels.
DEFAULT_POLICY = Policy(
    name="security-triage",
    question=(
        "Does this document show signs of a security threat — phishing, malware, "
        "credential theft, intrusion, or data exfiltration?"
    ),
    labels=("suspicious", "benign"),
)

SYSTEM_TEMPLATE = """\
You are a careful triage classifier. You will be given a DOCUMENT and a QUESTION.

Decide the single best label from this exact set: {labels}.

Reply with ONLY a JSON object, no prose around it, in this shape:
{{
  "label": one of {labels},
  "confidence": a number from 0 to 1,
  "rationale": a short plain-language explanation of your decision,
  "evidence": a list of short strings, each copied CHARACTER-FOR-CHARACTER from
              the DOCUMENT, that justify the label
}}

Rules:
- Every string in "evidence" MUST appear verbatim in the DOCUMENT. Do not
  paraphrase, summarize, translate, or fix typos in a quote.
- If nothing in the document supports a label, return an empty "evidence" list
  and lower your confidence accordingly.
- Quote the shortest spans that carry the signal, not whole paragraphs."""

# Shown only under prompt_style="few-shot". Larger, more fluent models tend to
# reword their "evidence" into a nicer sentence instead of copying it, which
# breaks grounding (the quote can no longer be found in the source). Two worked
# examples that copy evidence character-for-character pull them back toward
# literal quoting. The examples assume the default suspicious/benign framing.
FEWSHOT_BLOCK = """\
Here are two examples of the exact output format. Note that every "evidence"
string is copied word-for-word from its DOCUMENT -- it is not reworded.

EXAMPLE 1
DOCUMENT:
Your account is locked. Confirm your password at http://login.example to restore access.
OUTPUT:
{"label": "suspicious", "confidence": 0.9, "rationale": "Asks the user to confirm a password at an external link -- classic credential phishing.", "evidence": ["Confirm your password at http://login.example"]}

EXAMPLE 2
DOCUMENT:
Hi team, the budget review is moved to 2pm on Friday. Agenda attached.
OUTPUT:
{"label": "benign", "confidence": 0.85, "rationale": "A routine internal scheduling note with no threat signals.", "evidence": ["the budget review is moved to 2pm on Friday"]}

Now do the same for the real DOCUMENT below."""


def build_prompts(document: str, policy: Policy = DEFAULT_POLICY) -> tuple[str, str]:
    """Return the ``(system, user)`` prompt pair for triaging *document* under *policy*.

    When ``policy.prompt_style == "few-shot"`` the system prompt also carries two
    worked examples demonstrating verbatim evidence quoting.
    """
    labels = ", ".join(policy.labels)
    system = SYSTEM_TEMPLATE.format(labels=labels)
    if policy.prompt_style == "few-shot":
        system = f"{system}\n\n{FEWSHOT_BLOCK}"
    user = f"QUESTION: {policy.question}\n\nDOCUMENT:\n{document}"
    return system, user
