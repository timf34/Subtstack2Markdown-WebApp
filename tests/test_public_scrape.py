from scraper import public_client, transform


def test_parse_and_transform():
    posts, author = public_client.fetch_public_posts("tests/data/sample_feed.xml")
    assert author == "Sample Author"
    assert len(posts) == 2
    md = transform.html_to_md(posts[0].content_html)
    assert "hello" in md.lower()
    html = transform.md_to_html(md)
    assert "<p>" in html
