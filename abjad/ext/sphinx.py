import copy
import enum
import hashlib
import os
import pathlib
import subprocess

from docutils.nodes import (
    Element,
    FixedTextElement,
    General,
    SkipNode,
    image,
    literal_block,
)
from docutils.parsers.rst import Directive, directives
from sphinx.util import FilenameUniqDict
from sphinx.util.nodes import set_source_info
from uqbar.book.extensions import Extension
from uqbar.strings import normalize

from abjad import abjad_configuration
from abjad.io import Illustrator, LilyPondIO, Player
from abjad.lilypondfile import Block
from abjad.system import TemporaryDirectoryChange


class HiddenDoctestDirective(Directive):
    """
    An hidden doctest directive.

    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive.
        """
        self.assert_has_content()
        return []


class ShellDirective(Directive):
    """
    An shell directive.

    Represents a shell session.

    Generates a docutils ``literal_block`` node.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    ### PUBLIC METHODS ###

    def run(self):
        self.assert_has_content()
        result = []
        with TemporaryDirectoryChange(abjad_configuration.abjad_directory):
            cwd = pathlib.Path.cwd()
            for line in self.content:
                result.append(f"{cwd.name}$ {line}")
                completed_process = subprocess.run(
                    line,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                result.append(completed_process.stdout)
        code = "\n".join(result)
        literal = literal_block(code, code)
        literal["language"] = "console"
        set_source_info(self, literal)
        return [literal]


class ThumbnailDirective(Directive):
    """
    A thumbnail directive.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    final_argument_whitespace = True
    has_content = False
    option_spec = {
        "class": directives.class_option,
        "group": directives.unchanged,
        "title": directives.unchanged,
    }
    optional_arguments = 0
    required_arguments = 1

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive.
        """
        node = thumbnail_block()
        node["classes"] += self.options.get("class", "")
        node["group"] = self.options.get("group", "")
        node["title"] = self.options.get("title", "")
        node["uri"] = self.arguments[0]
        environment = self.state.document.settings.env
        environment.images.add_file("", node["uri"])
        return [node]


class thumbnail_block(image, General, Element):
    __documentation_ignore_inherited__ = True


def visit_thumbnail_block_html(self, node):
    template = normalize(
        """
        <a data-lightbox="{group}" href="{target_path}" title="{title}" data-title="{title}" class="{cls}">
            <img src="{thumbnail_path}" alt="{alt}"/>
        </a>
        """
    )
    self.builder.thumbnails.add_file("", node["uri"])
    title = node["title"]
    classes = " ".join(node["classes"])
    group = "group-{}".format(node["group"] if node["group"] else node["uri"])
    if node["uri"] in self.builder.images:
        node["uri"] = os.path.join(
            self.builder.imgpath, self.builder.images[node["uri"]]
        )
    target_path = node["uri"]
    prefix, suffix = os.path.splitext(target_path)
    if suffix == ".svg":
        thumbnail_path = target_path
    else:
        thumbnail_path = "{}-thumbnail{}".format(prefix, suffix)
    output = template.format(
        alt=title,
        group=group,
        target_path=target_path,
        cls=classes,
        thumbnail_path=thumbnail_path,
        title=title,
    )
    self.body.append(output)
    raise SkipNode


def visit_thumbnail_block_latex(self, node):
    raise SkipNode


def on_builder_inited(app):
    app.builder.thumbnails = FilenameUniqDict()


class LilyPondExtension(Extension):
    class Kind(enum.Enum):
        IMAGE = 1
        AUDIO = 2

    class lilypond_block(General, FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            Illustrator,
            "__call__",
            lambda self: console.push_proxy(
                cls(
                    self.illustrable,
                    cls.Kind.IMAGE,
                    **{
                        key.replace("lilypond/", "").replace("-", "_"): value
                        for key, value in console.proxy_options.items()
                        if key.startswith("lilypond/")
                    },
                ),
            ),
        )
        monkeypatch.setattr(
            Player,
            "__call__",
            lambda self: console.push_proxy(
                cls(
                    self.illustrable,
                    cls.Kind.AUDIO,
                    **{
                        key.replace("lilypond/", "").replace("-", "_"): value
                        for key, value in console.proxy_options.items()
                        if key.startswith("lilypond/")
                    },
                ),
            ),
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.lilypond_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )
        cls.add_option("lilypond/no-trim", directives.unchanged)
        cls.add_option("lilypond/pages", directives.unchanged)
        cls.add_option("lilypond/stylesheet", directives.unchanged)

    def __init__(self, illustrable, kind, pages=None, stylesheet=None, **keywords):
        self.illustrable = copy.deepcopy(illustrable)
        self.keywords = keywords
        self.kind = kind

    def to_docutils(self):
        illustration = self.illustrable.__illustrate__(**self.keywords)
        if self.kind == self.Kind.AUDIO:
            block = Block(name="midi")
            illustration.score_block.items.append(block)
        code = format(illustration, "lilypond")
        node = self.lilypond_block(code, code)
        node["kind"] = self.kind.name.lower()
        return [node]

    @staticmethod
    def visit_block_html(self, node):
        img_template = '<a class="uqbar-book" href="{source_path}"><img src="{relative_path}"/></a>'
        output_directory = pathlib.Path(self.builder.outdir) / "_images"
        render_prefix = "lilypond-{}".format(
            hashlib.sha256(node[0].encode()).hexdigest()
        )
        if node["kind"] == "audio":
            flags = []
            glob = f"{render_prefix}.mid*"
        else:
            flags = ["-dcrop", "-dbackend=svg"]
            glob = f"{render_prefix}.cropped.svg"
        lilypond_io = LilyPondIO(
            None,
            flags=flags,
            output_directory=output_directory,
            render_prefix=render_prefix,
            should_open=False,
            should_persist_log=False,
            string=node[0],
        )
        if not list(output_directory.glob(glob)):
            lilypond_io()
        source_path = (pathlib.Path(self.builder.imgpath) / render_prefix).with_suffix(".ly")
        for path in output_directory.glob(glob):
            relative_path = pathlib.Path(self.builder.imgpath) / path.name
            if path.suffix in (".mid", ".midi"):
                pass
            else:
                self.body.append(img_template.format(relative_path=relative_path, source_path=source_path))
        raise SkipNode


def setup(app):
    app.connect("builder-inited", on_builder_inited)
    app.add_directive("docs", HiddenDoctestDirective)
    app.add_directive("shell", ShellDirective)
    app.add_directive("thumbnail", ThumbnailDirective)
    app.add_node(
        thumbnail_block,
        html=[visit_thumbnail_block_html, None],
        latex=[visit_thumbnail_block_latex, None],
    )
