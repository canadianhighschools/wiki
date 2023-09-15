from apps.core.utils.lazy import lazy_import

from markdown_it import MarkdownIt
from markdown_it.main import MarkdownIt
import bleach

from .extensions.callout.index import execute

try:
    from settings.base import RENDERER_WHITELISTED_TAGS, RENDERER_WHITELISTED_ATTRIBUTES, RENDERER_WHITELISTED_PROTOCOLS, RENDERER_EXTENSIONS
except ImportError:
    RENDERER_WHITELISTED_TAGS = bleach.ALLOWED_TAGS
    RENDERER_WHITELISTED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES
    RENDERER_WHITELISTED_PROTOCOLS = bleach.ALLOWED_PROTOCOLS
    RENDERER_EXTENSIONS = []


def markdown_builder():
    md = MarkdownIt('commonmark', {'breaks': True, 'html': True}).use(execute)

    # for ext_id in RENDERER_EXTENSIONS:
    #     print ("Using renderer extension", ext_id)
    #     ext = lazy_import(f'apps.core.data.renderer.extensions.{ext_id}')
    #     md.use(ext.execute, ext_id)
    return md


def render_to_html(md: MarkdownIt, content: str):
    print (f"rendering:\n{content}")
    html_text = md.render(content)
    return bleach.clean(
            html_text,
            tags=RENDERER_WHITELISTED_TAGS,
            attributes=RENDERER_WHITELISTED_ATTRIBUTES,
            protocols=RENDERER_WHITELISTED_PROTOCOLS,
            strip=True,
        )
