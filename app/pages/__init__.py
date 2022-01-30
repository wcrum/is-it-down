import os
import markdown2

pages = {"/": []}

pages_path = os.path.dirname(os.path.realpath(__file__))


class Pages:
    def __init__(self):
        self.registered = {}
        self.unregistered = {}

    def add_page(self, page):

        if page.meta.get("base_url"):
            self.registered[page.meta["base_url"]] = page
        else:
            self.unregistered[page.filename] = page


class Page:
    def __init__(self, path, contents):
        self.path = path
        self.filename = os.path.basename(path)
        self.contents = contents
        self.html = markdown2.markdown(
            contents, extras=["fenced-code-blocks", "metadata", "toc"]
        )
        self.meta = self.html.metadata
        self.toc_html = self.html.toc_html


def create_pages():
    _pages = Pages()
    for path in os.listdir(pages_path):
        f = os.path.join(pages_path, path)
        if os.path.isfile(f) and f.endswith(".md"):
            with open(f, "r") as file:
                contents = file.read()

            page = Page(f, contents)
            _pages.add_page(page)

    return _pages
