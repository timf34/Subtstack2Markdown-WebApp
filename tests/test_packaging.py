from pathlib import Path
from zipfile import ZipFile

from scraper import public_client, writer


def test_package(tmp_path, monkeypatch):
    posts, author = public_client.fetch_public_posts("tests/data/sample_feed.xml")
    monkeypatch.setattr(writer, "BASE_MD_DIR", tmp_path / "md")
    monkeypatch.setattr(writer, "BASE_HTML_DIR", tmp_path / "html")
    monkeypatch.setattr(writer, "DIST_DIR", tmp_path / "dist")
    monkeypatch.setattr(writer, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(writer, "ASSETS_DIR", Path("assets"))
    monkeypatch.setattr(writer, "TEMPLATE_FILE", Path("author_template.html"))
    zip_path = writer.package("job1", author, posts)
    assert zip_path.exists()
    with ZipFile(zip_path) as zf:
        names = zf.namelist()
        assert any(name.endswith('.md') for name in names)
        assert any(name.endswith(f"{author}.html") for name in names)
