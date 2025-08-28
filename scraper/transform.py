import html2text
import markdown


html_to_md_converter = html2text.HTML2Text()
html_to_md_converter.ignore_images = True
html_to_md_converter.body_width = 0


def html_to_md(html: str) -> str:
    return html_to_md_converter.handle(html)


def md_to_html(md: str) -> str:
    return markdown.markdown(md)
