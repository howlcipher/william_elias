"""Build from source without reading or overwriting checked-in outputs."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = (
    "config.js", "index.html", "robots.txt", "sitemap.xml", "preview.jpg",
    "William_Elias_Resume.pdf",
)
GENERATORS = ("build_config.py", "build_html.py", "generate_resume_pdf.py")


@pytest.fixture(scope="module")
def isolated_builds(tmp_path_factory):
    builds = []
    for name in ("first", "repeat"):
        directory = tmp_path_factory.mktemp(name)
        shutil.copy2(ROOT / "resume.json", directory)
        shutil.copytree(ROOT / "assets", directory / "assets")
        (directory / "scripts").mkdir()
        for source in (*GENERATORS, "site_template.html"):
            shutil.copy2(ROOT / "scripts" / source, directory / "scripts")
        for generator in GENERATORS:
            subprocess.run(
                [sys.executable, "-W", "error", f"scripts/{generator}"],
                cwd=directory, check=True, capture_output=True, timeout=30,
            )
        builds.append(directory)
    return builds


@pytest.mark.parametrize("artifact", ARTIFACTS)
def test_checked_in_artifact_is_fresh(artifact, isolated_builds):
    assert (ROOT / artifact).read_bytes() == (
        isolated_builds[0] / artifact
    ).read_bytes(), f"Regenerate {artifact} with the pinned dependencies"


@pytest.mark.parametrize("artifact", ARTIFACTS)
def test_independent_generation_is_identical(artifact, isolated_builds):
    assert (isolated_builds[0] / artifact).read_bytes() == (
        isolated_builds[1] / artifact
    ).read_bytes(), f"{artifact} differs across independent builds"
