from jinja2 import Template, Environment, BaseLoader
from typing import Dict, Any


def render_html(html_str: str, data_dict: Dict[str, Any]) -> str:
    env = Environment(loader=BaseLoader())
    template = env.from_string(html_str)
    return template.render(**data_dict)
