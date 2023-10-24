from markdown_it.utils import PresetType
from utils.imports import lazy_import

from markdown_it import MarkdownIt
from markdown_it.main import MarkdownIt
import bleach
from bleach.css_sanitizer import CSSSanitizer, ALLOWED_CSS_PROPERTIES, ALLOWED_SVG_PROPERTIES

try:
    from project.config.settings.wiki import WHITELISTED_TAGS, WHITELISTED_ATTRIBUTES, WHITELISTED_PROTOCOLS, EXTENSIONS, WHITELISTED_CSS_PROPERTIES, WHITELISTED_SVG_PROPERTIES
except ImportError:
    WHITELISTED_TAGS = bleach.ALLOWED_TAGS
    WHITELISTED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES
    WHITELISTED_PROTOCOLS = bleach.ALLOWED_PROTOCOLS
    EXTENSIONS = []
    WHITELISTED_CSS_PROPERTIES = ALLOWED_CSS_PROPERTIES
    WHITELISTED_SVG_PROPERTIES = ALLOWED_SVG_PROPERTIES

DEFAULT_EXTENSIONS = ['section']
EXTENSIONS += DEFAULT_EXTENSIONS

CSS_SANITIZER = CSSSanitizer(allowed_css_properties=WHITELISTED_CSS_PROPERTIES,
                             allowed_svg_properties=WHITELISTED_SVG_PROPERTIES)


def preset() -> PresetType:
    return {
        "options": {
            "maxNesting": 20,  # Internal protection, recursion limit
            "html": True,  # Enable HTML tags in source,
            # this is just a shorthand for .enable(["html_inline", "html_block"])
            # used by the linkify rule:
            "linkify": False,  # autoconvert URL-like texts to links
            # used by the replacements and smartquotes rules
            # Enable some language-neutral replacements + quotes beautification
            "typographer": False,
            # used by the smartquotes rule:
            # Double + single quotes replacement pairs, when typographer enabled,
            # and smartquotes on. Could be either a String or an Array.
            #
            # For example, you can use '«»„“' for Russian, '„“‚‘' for German,
            # and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
            "quotes": "\u201c\u201d\u2018\u2019",  # /* “”‘’ */
            # Renderer specific; these options are used directly in the HTML renderer
            "xhtmlOut": True,  # Use '/' to close single tags (<br />)
            "breaks": True,  # Convert '\n' in paragraphs into <br>
            "langPrefix": "language-",  # CSS language prefix for fenced blocks
            # Highlighter function. Should return escaped HTML,
            # or '' if the source string is not changed and should be escaped externally.
            # If result starts with <pre... internal wrapper is skipped.
            #
            # function (/*str, lang, attrs*/) { return ''; }
            #
            "highlight": None,
        },
        "components": {
            "core": {"rules": ["normalize", "block", "inline", "text_join"]},
            "block": {
                "rules": [
                    "blockquote",
                    "code",
                    "fence",
                    "hr",
                    "html_block",
                    "lheading",
                    "list",
                    "reference",
                    "paragraph",
                ]
            },
            "inline": {
                "rules": [
                    "autolink",
                    "backticks",
                    "emphasis",
                    "entity",
                    "escape",
                    "html_inline",
                    "image",
                    "link",
                    "newline",
                    "text",
                ],
                "rules2": ["balance_pairs", "emphasis", "fragments_join"],
            },
        },
    }


def markdown_builder():
    md = MarkdownIt(config=preset())

    for ext_id in EXTENSIONS:
        ext = lazy_import(f'.extensions.{ext_id}', package=__package__)
        ext.wrapper().plugin(md)

    return md


class RenderedPageText:
    def __init__(self, sections, content) -> None:
        self.sections = sections
        self.content = content


def render_to_html(md: MarkdownIt, content: str) -> RenderedPageText:
    tokens = md.parse(content)

    # [('get-started', 'Getting Started', 0)]
    sections = []

    for t in tokens:
        if (t.type == 'section_open' and t.info != 'hidden'):
            sections.append(
                {'id': t.attrGet('id'), 'title': t.content, 'level': t.level-1})

    html_text = md.renderer.render(tokens, md.options, {})

    return RenderedPageText(
        sections=sections,
        content=bleach.clean(
            text=html_text,
            tags=WHITELISTED_TAGS,
            attributes=WHITELISTED_ATTRIBUTES,
            protocols=WHITELISTED_PROTOCOLS,
            strip=False,
            strip_comments=True,
            css_sanitizer=bleach.css_sanitizer.ALLOWED_CSS_PROPERTIES
        ))
