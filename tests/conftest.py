"""Shared fixtures: build each targeted résumé variant once per session."""
import pypdf
import pytest

from scripts.generate_resume_pdf import build, load_config, load_variants

VARIANT_NAMES = tuple(load_variants()["variants"])


@pytest.fixture(scope="session")
def variants():
    return load_variants()


@pytest.fixture(scope="session")
def variant_pdfs(tmp_path_factory, variants):
    """{variant name: {"path", "reader", "pages", "text"}} from the canonical sources."""
    config = load_config()
    built = {}
    for name in variants["variants"]:
        path = tmp_path_factory.mktemp(name) / variants["variants"][name]["file"]
        build(config, path, name, variants)
        reader = pypdf.PdfReader(path)
        pages = [page.extract_text() for page in reader.pages]
        built[name] = {
            "path": path,
            "reader": reader,
            "pages": pages,
            "text": " ".join(" ".join(page.split()) for page in pages),
        }
    return built
