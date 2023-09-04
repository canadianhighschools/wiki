from markdown_it import MarkdownIt
from .extensions.callout import callout_plugin
from .extensions.lock import lock_plugin

import bleach


def create_md():
    md = (MarkdownIt('commonmark', {'breaks': True, 'html': True})
            .use(callout_plugin)
            .use(lock_plugin)
        )
    return md


md = create_md()


def create_whitelisted_tags():
    return ["p",
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "code",
        "em",
        "i",
        "li",
        "ol",
        "strong",
        "ul",
        "div",
    ]


def create_whitelisted_attributes(tags):
    base_whitelisted_attributes = {
        "a": ["href", "title"],
        "abbr": ["title"],
        "acronym": ["title"],
    }

    for t in tags:
        if (t in base_whitelisted_attributes):
            base_whitelisted_attributes[t].append('class')
        else:
            base_whitelisted_attributes[t] = ["class"]

    return base_whitelisted_attributes
        

ALLOWED_TAGS = create_whitelisted_tags()
ALLOWED_ATTRIBUTES = create_whitelisted_attributes(ALLOWED_TAGS)

def render_to_html(text):
    bleach.sanitizer.ALLOWED_ATTRIBUTES
    html_text = md.render(text)
    print ("unrendered", html_text)
    return bleach.clean(html_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
