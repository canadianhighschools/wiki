import re
from core.models import Category, Page, Revision, TextContent

from typing import Optional


def page_from_path(path: str) -> Optional[Page]:
    """
    get-started/fundamentals/changing-a-course

    moves to get-started (category)
        moves to fundamentals (category)
            returns changing-a-course (page)
    """
    if (path == ""): return 
    
    slugs = re.split(r'/', path.strip('/'))

    # iterate to the direct parent of the page, we dont grab the page directly because
    # iterating categories is pretty minimal in terms of cost and this way we can have
    # local slugs (two "basic" page slugs in different categories)
    parent = None
    for i in range(len(slugs)-1):
        try: 
            parent = Category.objects.get(parent=parent, slug=slugs[i])
        except Category.DoesNotExist:
            return

    try:
        return Page.objects.get(parent=parent, slug=slugs[-1]) # use last slug
    except Page.DoesNotExist:
        return 



def revision_from_page(page: Page) -> Optional[Revision]:
    if (not page or page.order == -1): return 

    try:
        return page.revisions.get(order=page.order) # fetch revision by current order
    except Revision.DoesNotExist:
        return 



def content_from_revision(revision: Revision) -> Optional[TextContent]:
    if (not revision): return 

    try:
        content = revision.content
        return content
        
    except TextContent.DoesNotExist:
        return
    

def text_from_content(content: TextContent) -> Optional[str]:
    if (content.flags == 0): 
        return content.text
    


def text_from_path(path) -> Optional[str]:
    # the ultimate stack
    page = page_from_path(path)
    if (not page): return 

    revision = revision_from_page(page)
    if (not revision): return 

    content = content_from_revision(revision)
    if (not content): return 

    return text_from_content(content)