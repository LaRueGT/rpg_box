"""Tests for the rules derived from character ability scores."""

import pytest

from rules import ability_rules


@pytest.mark.parametrize(
    ("score", "expected_modifier"),
    [
        (3, -3),
        (4, -2),
        (6, -1),
        (9, 0),
        (13, 1),
        (16, 2),
        (18, 3),
    ],
)
def test_ability_modifier_uses_standard_score_bands(score, expected_modifier):
    """Each representative score produces the modifier for its band."""
    assert ability_rules.ability_modifier(score) == expected_modifier


@pytest.mark.parametrize("invalid_score", [2, 19, 3.5, True, "12"])
def test_ability_score_must_be_an_integer_from_3_through_18(invalid_score):
    with pytest.raises((TypeError, ValueError)):
        ability_rules.ability_modifier(invalid_score)


@pytest.mark.parametrize(
    ("strength", "expected_target"),
    [(3, 1), (8, 1), (9, 2), (12, 2), (13, 3), (15, 3), (16, 4), (17, 4), (18, 5)],
)
def test_strength_open_doors_returns_the_correct_d6_target(strength, expected_target):
    assert ability_rules.strength_open_doors(strength) == expected_target


def test_intelligence_rules_handle_literacy_and_extra_languages():
    assert ability_rules.intelligence_literate(5) is False
    assert ability_rules.intelligence_literate(6) is True
    assert ability_rules.intelligence_native_speech(3) == "broken"
    assert ability_rules.intelligence_native_speech(4) == "native"
    assert ability_rules.intelligence_additional_languages(12) == 0
    assert ability_rules.intelligence_additional_languages(13) == 1
    assert ability_rules.intelligence_additional_languages(18) == 3


def test_dexterity_changes_descending_ac_and_initiative():
    assert ability_rules.armor_class(16) == 7
    assert ability_rules.armor_class(16, base_ac=5) == 3
    assert ability_rules.dexterity_initiative_modifier(3) == -2
    assert ability_rules.dexterity_initiative_modifier(8) == -1
    assert ability_rules.dexterity_initiative_modifier(13) == 1
    assert ability_rules.dexterity_initiative_modifier(18) == 2


@pytest.mark.parametrize(
    ("hit_die_roll", "constitution", "expected_hp"),
    [(1, 3, 1), (2, 3, 1), (4, 9, 4), (1, 18, 4)],
)
def test_constitution_hit_points_never_drops_below_one(
    hit_die_roll, constitution, expected_hp
):
    assert (
        ability_rules.constitution_hit_points(hit_die_roll, constitution)
        == expected_hp
    )


def test_constitution_hit_die_roll_must_not_be_negative():
    with pytest.raises(ValueError):
        ability_rules.constitution_hit_points(-1, 10)


def test_charisma_controls_reactions_retainers_and_loyalty():
    assert ability_rules.charisma_reaction_modifier(3) == -2
    assert ability_rules.charisma_reaction_modifier(18) == 2
    assert ability_rules.charisma_max_retainers(3) == 1
    assert ability_rules.charisma_max_retainers(18) == 7
    assert ability_rules.charisma_retainer_loyalty(3) == 4
    assert ability_rules.charisma_retainer_loyalty(18) == 10
