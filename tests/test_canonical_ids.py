"""Stable canonical IDs let résumé variants select content without array positions."""
import copy

import pytest

from scripts.generate_resume_pdf import ID_COLLECTIONS, canonical_index, load_config, validate_config


@pytest.fixture(scope="module")
def config():
    return load_config()


def test_every_selectable_item_has_a_unique_readable_id(config):
    index = canonical_index(config)
    expected = sum(len(config[kind]) for kind in ID_COLLECTIONS)
    expected += sum(len(job["achievements"]) for job in config["experience"])
    expected += len(config.get("positioningStatements", []))
    assert len(index) == expected
    for item_id in index:
        assert item_id == item_id.lower()
        assert not any(ch.isdigit() for ch in item_id), item_id


@pytest.mark.parametrize("kind,prefix", [
    ("skills", "skill-"), ("selectedEngineeringPrograms", "program-"),
    ("pdfEngineeringHighlights", "highlight-"), ("projects", "project-"),
    ("experience", "exp-"), ("additionalExperience", "exp-"), ("education", "edu-"),
])
def test_ids_use_a_human_readable_kind_prefix(config, kind, prefix):
    for item in config[kind]:
        assert item["id"].startswith(prefix), item["id"]


def test_achievement_ids_use_ach_prefix(config):
    for job in config["experience"]:
        for achievement in job["achievements"]:
            assert achievement["id"].startswith("ach-")
            assert achievement["text"]


def test_duplicate_id_fails_validation(config):
    broken = copy.deepcopy(config)
    broken["projects"][1]["id"] = broken["projects"][0]["id"]
    with pytest.raises(ValueError, match="duplicate canonical ID"):
        validate_config(broken)


@pytest.mark.parametrize("bad_id", [None, "", "Project-HowlPlane", "project-one-two-3", "project"])
def test_malformed_or_positional_id_fails_validation(config, bad_id):
    broken = copy.deepcopy(config)
    broken["projects"][0]["id"] = bad_id
    with pytest.raises(ValueError, match=r"projects\[0\]\.id"):
        validate_config(broken)


def test_ids_do_not_depend_on_array_position(config):
    reordered = copy.deepcopy(config)
    reordered["projects"].reverse()
    reordered["skills"].reverse()
    before, after = canonical_index(config), canonical_index(reordered)
    assert before.keys() == after.keys()
    for item_id, (kind, item) in before.items():
        assert after[item_id] == (kind, item)
