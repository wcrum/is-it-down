import jinja2
from flask import render_template
from flask import current_app
from flask import request


def render_markdown(template_name, file=None, **context):
    if file:
        page = current_app.pages.unregistered[file]
    else:
        page = current_app.pages.registered[request.path]

    env = jinja2.Environment(loader=jinja2.BaseLoader(), auto_reload=True)
    template = env.from_string(str(page.html))
    page.html = template.render(**context)

    rendered = render_template(template_name, page=page, **context)

    return rendered
