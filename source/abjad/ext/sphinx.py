import copy
import enum
import hashlib
import os
import pathlib
import shutil
import subprocess

import sphinx
from docutils.nodes import (
    Element,
    FixedTextElement,
    General,
    SkipNode,
    image,
    literal_block,
)
from docutils.parsers.rst import Directive, directives
from sphinx.util import logging
from sphinx.util.console import brown  # type: ignore
from sphinx.util.nodes import set_source_info
from sphinx.util.osutil import copyfile, ensuredir
from uqbar.book.extensions import Extension
from uqbar.strings import normalize

from .. import format as _format
from .. import lilypondfile as _lilypondfile
from .. import tag as _tag
from ..configuration import Configuration
from ..contextmanagers import TemporaryDirectoryChange
from ..illustrators import illustrate
from ..io import Illustrator, LilyPondIO, Player

configuration = Configuration()
logger = logging.getLogger(__name__)


class HiddenDoctestDirective(Directive):
    """
    A hidden doctest directive.

    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: dict[str, str] = {}

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive."""
        self.assert_has_content()
        return []


class ShellDirective(Directive):
    """
    A shell directive.

    Represents a shell session.

    Generates a docutils ``literal_block`` node.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: dict[str, str] = {}

    ### PUBLIC METHODS ###

    def run(self):
        self.assert_has_content()
        result = []
        with TemporaryDirectoryChange(configuration.abjad_directory):
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
        """Executes the directive."""
        node = thumbnail_block()
        node["classes"] += self.options.get("class", "")
        node["group"] = self.options.get("group", "")
        node["title"] = self.options.get("title", "")
        node["uri"] = self.arguments[0]
        environment = self.state.document.settings.env
        name, suffix = os.path.splitext(node["uri"])
        environment.images.add_file(environment.docname, node["uri"])
        thumbnail_uri = name + "-thumbnail" + suffix
        environment.thumbnails[thumbnail_uri] = environment.docname
        # this may also work:
        # environment.thumbnails[environment.docname] = thumbnail_uri
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
    app.env.thumbnails = {}  # separate so Sphinx doesn't purge it
    install_lightbox_static_files(app)
    (pathlib.Path(app.builder.outdir) / "_images").mkdir(exist_ok=True)


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
        cls.add_option("lilypond/no-trim", directives.flag)
        cls.add_option("lilypond/pages", directives.unchanged)
        cls.add_option("lilypond/with-columns", int)

    def __init__(
        self,
        illustrable,
        kind,
        no_trim=None,
        pages=None,
        with_columns=None,
        **keywords,
    ):
        self.illustrable = copy.deepcopy(illustrable)
        self.keywords = keywords
        self.kind = kind
        self.no_trim = no_trim
        self.pages = pages
        self.with_columns = with_columns

    def to_docutils(self):
        if isinstance(self.illustrable, _lilypondfile.LilyPondFile):
            illustration = self.illustrable
        else:
            illustration = illustrate(self.illustrable, **self.keywords)
        if self.kind == self.Kind.AUDIO:
            block = _lilypondfile.Block("midi")
            illustration["score"].items.append(block)
        illustration.lilypond_version_token = r'\version "2.19.83"'
        code = illustration._get_lilypond_format()
        code = _format.remove_site_comments(code)
        code = _tag.remove_tags(code)
        node = self.lilypond_block(code, code)
        node["kind"] = self.kind.name.lower()
        node["no-trim"] = self.no_trim
        node["pages"] = self.pages
        node["with-columns"] = self.with_columns
        return [node]

    @staticmethod
    def visit_block_html(self, node):
        output_directory = pathlib.Path(self.builder.outdir) / "_images"
        render_prefix = "lilypond-{}".format(
            hashlib.sha256(node[0].encode()).hexdigest()
        )
        if node["kind"] == "audio":
            flags = []
            glob = f"{render_prefix}.mid*"
        else:
            flags = ["-dcrop", "-dbackend=svg"]
            glob = f"{render_prefix}*.svg"
        lilypond_io = LilyPondIO(
            None,
            flags=flags,
            output_directory=output_directory,
            render_prefix=render_prefix,
            should_copy_stylesheets=True,
            should_open=False,
            should_persist_log=False,
            string=node[0],
        )
        if not list(output_directory.glob(glob)):
            _, _, _, success, log = lilypond_io()
            if not success:
                logger.warning(f"LilyPond render failed\n{log}", location=node)
        source_path = (pathlib.Path(self.builder.imgpath) / render_prefix).with_suffix(
            ".ly"
        )
        if node["kind"] == "audio":
            pass
        else:
            embed_images(self, node, output_directory, render_prefix, source_path)
        raise SkipNode


table_row_open_template = '<div class="table-row">'
table_row_close_template = "</div>"
basic_image_template = normalize(
    """
    <div class="uqbar-book">
        <a href="{source_path}"><img src="{relative_path}"/></a>
    </div>
    """
)
thumbnail_template = normalize(
    """
    <a data-lightbox="{group}" href="{fullsize_path}" title="{title}" data-title="{title}" class="{cls}">
        <img src="{thumbnail_path}" alt="{alt}"/>
    </a>
    """
)


def embed_images(self, node, output_directory, render_prefix, source_path):
    paths_to_embed = []
    if node.get("pages"):
        for page_spec in node["pages"].split(","):
            page_spec = page_spec.strip()
            if "-" in page_spec:
                start_spec, _, stop_spec = page_spec.partition("-")
                start_page, stop_page = int(start_spec), int(stop_spec) + 1
            else:
                start_page, stop_page = int(page_spec), int(page_spec) + 1
            for page_number in range(start_page, stop_page):
                for path in output_directory.glob(f"{render_prefix}-{page_number}.svg"):
                    paths_to_embed.append(path)
    elif node.get("no-trim"):
        for path in output_directory.glob(f"{render_prefix}.svg"):
            paths_to_embed.append(path)
        if not paths_to_embed:
            page_count = len(list(output_directory.glob(f"{render_prefix}-*.svg")))
            for page_number in range(1, page_count + 1):
                for path in output_directory.glob(f"{render_prefix}-{page_number}.svg"):
                    paths_to_embed.append(path)
    else:
        for path in output_directory.glob(f"{render_prefix}.cropped.svg"):
            paths_to_embed.append(path)
    with_columns = node.get("with-columns")
    if with_columns:
        for i in range(0, len(paths_to_embed), with_columns):
            self.body.append(table_row_open_template)
            for path in paths_to_embed[i : i + with_columns]:
                relative_path = pathlib.Path(self.builder.imgpath) / path.name
                self.body.append(
                    thumbnail_template.format(
                        alt="",
                        cls="table-cell thumbnail",
                        group=f"group-{render_prefix}",
                        fullsize_path=relative_path,
                        thumbnail_path=relative_path,
                        title="",
                    )
                )
            self.body.append(table_row_close_template)
    else:
        for path in paths_to_embed:
            relative_path = pathlib.Path(self.builder.imgpath) / path.name
            self.body.append(
                basic_image_template.format(
                    relative_path=relative_path, source_path=source_path
                )
            )


def install_lightbox_static_files(app):
    source_static_path = os.path.join(app.builder.srcdir, "_static")
    target_static_path = os.path.join(app.builder.outdir, "_static")
    source_lightbox_path = os.path.join(source_static_path, "lightbox2")
    target_lightbox_path = os.path.join(target_static_path, "lightbox2")
    relative_file_paths = []
    for root, _, file_names in os.walk(source_lightbox_path):
        for file_name in file_names:
            absolute_file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(absolute_file_path, source_static_path)
            relative_file_paths.append(relative_file_path)
    if os.path.exists(target_lightbox_path):
        shutil.rmtree(target_lightbox_path)
    for relative_file_path in sphinx.util.display.status_iterator(
        relative_file_paths,
        "installing lightbox files... ",
        brown,
        len(relative_file_paths),
    ):
        source_path = os.path.join(source_static_path, relative_file_path)
        target_path = os.path.join(target_static_path, relative_file_path)
        target_directory = os.path.dirname(target_path)
        if not os.path.exists(target_directory):
            ensuredir(target_directory)
        copyfile(source_path, target_path)
        if relative_file_path.endswith(".js"):
            app.add_js_file(relative_file_path, defer="defer")
        elif relative_file_path.endswith(".css"):
            app.add_css_file(relative_file_path)


def on_html_collect_pages(app):
    for path in sphinx.util.display.status_iterator(
        app.env.thumbnails,
        "copying gallery thumbnails...",
        "brown",
        len(app.env.thumbnails),
    ):
        source_path = pathlib.Path(app.srcdir) / path
        target_path = pathlib.Path(app.outdir) / "_images" / source_path.name
        try:
            shutil.copy(source_path, target_path)
        except Exception:
            logger.warning(f"Could not copy {source_path}")
    return []


def setup(app):
    app.connect("builder-inited", on_builder_inited)
    app.connect("html-collect-pages", on_html_collect_pages)
    app.add_css_file("abjad.css")
    app.add_directive("docs", HiddenDoctestDirective)
    app.add_directive("shell", ShellDirective)
    app.add_directive("thumbnail", ThumbnailDirective)
    app.add_js_file("ga.js")
    app.add_node(
        thumbnail_block,
        html=[visit_thumbnail_block_html, None],
        latex=[visit_thumbnail_block_latex, None],
    )
