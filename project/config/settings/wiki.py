# see https://portswigger.net/web-security/cross-site-scripting/cheat-shee
EXTENSIONS = [
    'lock',
    'callout',
    'opinion',
]

WHITELISTED_TAGS = [
    'p',
    'a',
    'abbr',
    'acronym',
    'address',
    'article',
    'aside',
    'base',
    'big',
    'b',
    'br',
    'blockquote',
    'code',
    'cite',
    'caption',
    'col',
    'define',
    'pre',
    'span',
    'svg',
    'table',
    'tbody',
    'td',
    'template',
    'tfoot',
    'th',
    'tr',
    'var',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'div',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'section',
]


WHITELISTED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'rel'],
    'abbr': ['title'],
    'acronym': ['title'],
    'base': ['href']
}

WHITELISTED_PROTOCOLS = [
    'https'
]

WHITELISTED_CSS_PROPERTIES = [
    "azimuth",
    "background-color",
    "border-bottom-color",
    "border-collapse",
    "border-color",
    "border-left-color",
    "border-right-color",
    "border-top-color",
    "clear",
    "color",
    "cursor",
    "direction",
    "display",
    "elevation",
    "float",
    "font",
    "font-family",
    "font-size",
    "font-style",
    "font-variant",
    "font-weight",
    "height",
    "letter-spacing",
    "line-height",
    "overflow",
    "pause",
    "pause-after",
    "pause-before",
    "pitch",
    "pitch-range",
    "richness",
    "speak",
    "speak-header",
    "speak-numeral",
    "speak-punctuation",
    "speech-rate",
    "stress",
    "text-align",
    "text-decoration",
    "text-indent",
    "unicode-bidi",
    "vertical-align",
    "voice-family",
    "volume",
    "white-space",
    "width",
]

WHITELISTED_SVG_PROPERTIES = [
    "fill",
    "fill-opacity",
    "fill-rule",
    "stroke",
    "stroke-width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-opacity",
]

TAG_PREFIX = '#'

TAG_VALUES = {
    'all_grades': '9,10,11,12',
    'all_districts': 'peel',
    'all_subjects': 'english,maths',
}