from __future__ import annotations

from dataclasses import replace

from glassbox.prompts import DEFAULT_POLICY, FEWSHOT_BLOCK, PROMPT_STYLES, build_prompts


def test_plain_is_the_default_and_omits_examples():
    assert DEFAULT_POLICY.prompt_style == "plain"
    system, user = build_prompts("hello", DEFAULT_POLICY)
    assert FEWSHOT_BLOCK not in system
    assert "verbatim" in system  # the core contract is still stated
    assert "DOCUMENT:\nhello" in user


def test_few_shot_appends_worked_examples():
    policy = replace(DEFAULT_POLICY, prompt_style="few-shot")
    system, _ = build_prompts("hello", policy)
    assert FEWSHOT_BLOCK in system
    assert "EXAMPLE 1" in system and "EXAMPLE 2" in system


def test_few_shot_examples_are_themselves_verbatim():
    # Each example must quote a span that actually appears in its own example
    # document -- otherwise the demonstration contradicts the rule it teaches.
    assert "Confirm your password at http://login.example" in FEWSHOT_BLOCK
    assert "the budget review is moved to 2pm on Friday" in FEWSHOT_BLOCK


def test_labels_render_in_both_styles():
    for style in PROMPT_STYLES:
        system, _ = build_prompts("x", replace(DEFAULT_POLICY, prompt_style=style))
        assert "suspicious, benign" in system
