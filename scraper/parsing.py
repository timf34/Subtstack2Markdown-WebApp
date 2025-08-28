from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import xml.etree.ElementTree as ET


@dataclass
class Post:
    title: str
    subtitle: str
    date: str
    content_html: str


def parse_feed(xml_text: str) -> Tuple[str, List[Post]]:
    root = ET.fromstring(xml_text)
    channel = root.find('channel')
    author = channel.findtext('title', default='substack') if channel is not None else 'substack'
    posts: List[Post] = []
    if channel is not None:
        for item in channel.findall('item'):
            title = item.findtext('title', default='')
            subtitle = item.findtext('description', default='')
            pub_date = item.findtext('pubDate', default='')
            content = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded', default='')
            posts.append(Post(title=title, subtitle=subtitle, date=pub_date, content_html=content))
    return author, posts
