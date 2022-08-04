"""User Interface elements for web application."""

# Core libs
import re
import sys
import uuid
import logging
from pathlib import Path

# Third-party libs
from tornado.web import UIModule

# Source libs
from .helpers import get_path_from_name
from .constants import PATH_INFO, PATH_TEMPLATES


class HandlerUI(UIModule):
    # def render(self, html=None, **kwargs):
    #     if html is None:
    #         html = self.__class__.__name__
    #     return self.render_string("ui/{}.html".format(html),
    #                               id=uuid.uuid4().__int__(), **kwargs)

    def render(self, name_directory: str = "ui", name_file=None):
        self.id = str(uuid.uuid4()).replace("-", "")

        return self.render_string(
            (
                f"{name_directory}/"
                + get_path_from_name(
                    name=(self.__class__.title() if not name_file else name_file),
                    path=PATH_TEMPLATES / name_directory,
                ).name
            ),
            ui=self,
        )

    @classmethod
    def title(cls):
        return "_".join(cls.__name__.split("_")[1:]).lower()


# NOTE: SECTION -> DYNAMICALLY CREATED UIs
for path_template in [
    x
    for x in (PATH_TEMPLATES / "ui").iterdir()
    if (not x.is_dir() and re.search(r"\.html(?:\.j2)?", x.name, re.IGNORECASE))
]:
    # Dont worry about not including some, everything is controlled by the PH anyway
    # if not re.search("(old|new|_?test_?|_$)", f.stem, re.IGNORECASE):
    name_path_template = path_template.name.split(".")[0]

    # TODO: Add __admin for admin-only pages, add __auth for authenticated-only pages

    name = "".join(
        [
            a if a.isupper() else b
            for a, b in zip(name_path_template, name_path_template.title())
        ]
    )

    _class_handler = type(f"UI_{name}", (HandlerUI,), {})
    logging.info(f"Created ui {_class_handler}")
    setattr(sys.modules[__name__], _class_handler.__name__, _class_handler)


class UI_Vue(HandlerUI):
    def render(self, name):
        # self.model = model
        return super().render(name_directory="vue", name_file=name)

    @property
    def splitName(self) -> str:
        matches = re.findall("[A-Z][a-z]+", self.model.__name__)
        return "-".join([str(x).lower() for x in matches])
