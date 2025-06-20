import copy
import enum
import hashlib
import os
import pathlib
import shutil
import subprocess

import docutils
import sphinx
import uqbar
from uqbar.book.extensions import Extension

from .. import configuration as _configuration
from .. import contextmanagers as _contextmanagers
from .. import format as _format
from .. import illustrators as _illustrators
from .. import io as _io
from .. import lilypondfile as _lilypondfile
from .. import tag as _tag

configuration = _configuration.Configuration()
logger = sphinx.util.logging.getLogger(__name__)


class AbjadClassDocumenter(uqbar.apis.summarizers.SummarizingClassDocumenter):
    """
    Abjad class documenter.

    https://github.com/supriya-project/uqbar/blob/main/uqbar/apis/summarizers.py
    """

    def __str__(self) -> str:
        """
        https://github.com/supriya-project/uqbar/blob/main/uqbar/apis/summarizers.py
        """
        name = getattr(self.client, "__name__")
        if issubclass(self.client, Exception):  # type: ignore
            return ".. autoexception:: {}".format(name)
        attributes = self._classify_class_attributes()
        (
            class_methods,
            data,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
        ) = attributes
        result = [".. autoclass:: {}".format(name)]
        if issubclass(self.client, enum.Enum):  # type: ignore
            result.extend(["   :members:", "   :undoc-members:"])
        else:
            result.extend(self._build_member_autosummary(attributes))
        result.extend(
            self._build_attribute_section(
                special_methods, "automethod", "Special methods"
            )
        )
        result.extend(self._build_attribute_section(methods, "automethod", "Methods"))
        result.extend(
            self._build_attribute_section(
                sorted(class_methods + static_methods, key=lambda x: x.name),
                "automethod",
                "Class & static methods",
            )
        )
        result.extend(
            self._build_attribute_section(
                readwrite_properties, "autoattribute", "Read/write properties"
            )
        )
        result.extend(
            self._build_attribute_section(
                readonly_properties, "autoattribute", "Read-only properties"
            )
        )
        return "\n".join(result)

    def _build_attribute_section(
        self, attributes, directive: str, title: str
    ) -> list[str]:
        """
        https://github.com/supriya-project/uqbar/blob/main/uqbar/apis/summarizers.py
        """
        # if getattr(self.client, "__name__") == "Tuplet" and "Special" in title:
        #     breakpoint()
        result: list[str] = []
        if not attributes:
            return result
        preamble = [
            "",
            "   .. raw:: html",
            "",
            "      <hr/>",
            "",
            "   .. rubric:: {}".format(title),
            "      :class: class-header",
        ]
        for attribute in attributes:
            # do not document __repr__, even if custom-defined on class
            if attribute.name == "__repr__":
                continue
            # document only noninherited attributes
            if attribute.defining_class is self.client:
                autodoc_directive = "   .. {}:: {}.{}".format(
                    directive, getattr(self.client, "__name__"), attribute.name
                )
                result.append("")
                result.append(autodoc_directive)
        if result:
            result = preamble + result
        return result

    def _build_member_autosummary(self, attributes) -> list[str]:
        """
        https://github.com/supriya-project/uqbar/blob/main/uqbar/apis/summarizers.py
        """
        result: list[str] = []
        all_attributes: list = []
        for attribute_section in attributes:
            """
            all_attributes.extend(
                attribute
                for attribute in attribute_section
                if attribute.defining_class is self.client
            )
            """
            for attribute in attribute_section:
                # do not summarize __repr__, even if custom-defined on class
                if attribute.name == "__repr__":
                    continue
                if attribute.defining_class is not self.client:
                    continue
                all_attributes.append(attribute)
        all_attributes.sort(key=lambda x: x.name)
        if not all_attributes:
            return result
        result.extend(
            [
                "",
                "   .. raw:: html",
                "",
                "      <hr/>",
                "",
                "   .. rubric:: {}".format("Attribute summary"),
                "      :class: class-header",
                "",
                "   .. autosummary::",
                # "      :nosignatures:",
                "",
            ]
        )
        for attribute in all_attributes:
            result.append("      {}".format(attribute.name))
        return result


class AbjadModuleDocumenter(uqbar.apis.summarizers.SummarizingModuleDocumenter):
    """
    Abjad module documenter.

    https://github.com/supriya-project/uqbar/blob/main/uqbar/apis/summarizers.py
    """

    def __str__(self) -> str:
        result = self._build_preamble()
        if self.is_nominative:
            result.extend(["", str(self.member_documenters[0])])
        else:
            # true only for abjad, abjad.ext, abjad.parsers
            if self.is_package:
                subpackage_documenters = [
                    _
                    for _ in self.module_documenters or []
                    if _.is_package or not _.is_nominative
                ]
                if subpackage_documenters:
                    result.extend(
                        self._build_toc(subpackage_documenters, show_full_paths=True)
                    )
            all_documenters = []
            for section, documenters in self.member_documenters_by_section:
                all_documenters.extend(documenters)
            all_documenters.sort(key=lambda _: getattr(_.client, "__name__", ""))
            local_documenters = [
                documenter
                for documenter in all_documenters
                if documenter.client.__module__ == self.package_path
            ]
            result.extend(self._build_toc(all_documenters))
            for local_documenter in local_documenters:
                result.extend(["", str(local_documenter)])
        return "\n".join(result)


class AbjadRootDocumenter(uqbar.apis.documenters.RootDocumenter):
    """
    Abjad root documenter.

    Writes abjad/docs/source/api/index.rst.
    """

    do_not_document = (
        "abjad.ext",
        "abjad.ext.sphinx",
        "abjad.parsers.base",
        "abjad.parsers.parser",
        "abjad.parsers.scheme",
    )

    def __str__(self):
        result = [
            self.title,
            "=" * len(self.title),
            "",
            ".. toctree::",
            "   :hidden:",
            "",
        ]
        assert len(self.module_documenters) == 1
        for documenter in self.module_documenters:
            path = documenter.package_path.replace(".", "/")
            if documenter.is_package:
                path += "/index"
            result.append("   {}".format(path))
        for module_documenter, documenters_by_section in self._recurse(self):
            if module_documenter.package_name == "abjad":
                continue
            if module_documenter.package_path in self.do_not_document:
                continue
            package_path = module_documenter.package_path
            reference_name = module_documenter.reference_name
            result.extend(
                [
                    "",
                    f".. rubric:: :ref:`{package_path} <{reference_name}>`",
                    "   :class: section-header",
                ]
            )
            flattened_documenters = []
            for section_name, documenters in documenters_by_section:
                flattened_documenters.extend(documenters)
            function_documenters, class_documenters = [], []
            for documenter in flattened_documenters:
                if documenter.client.__name__[0].islower():
                    function_documenters.append(documenter)
                else:
                    class_documenters.append(documenter)
            function_documenters.sort(key=lambda _: _.client.__name__)
            class_documenters.sort(key=lambda _: _.client.__name__)
            flattened_documenters = function_documenters + class_documenters
            result.extend(
                [
                    "",
                    ".. autosummary::",
                    "",
                ]
            )
            for documenter in flattened_documenters:
                result.append("   ~{}".format(documenter.package_path))
        return "\n".join(result)

    def _recurse(self, documenter):
        result = []
        if (
            isinstance(documenter, uqbar.apis.documenters.ModuleDocumenter)
            and not documenter.is_nominative
        ):
            result.append((documenter, documenter.member_documenters_by_section))
        for module_documenter in documenter.module_documenters:
            result.extend(self._recurse(module_documenter))
        return result


class HiddenDoctestDirective(docutils.parsers.rst.Directive):
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


class ShellDirective(docutils.parsers.rst.Directive):
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
        with _contextmanagers.TemporaryDirectoryChange(configuration.abjad_directory):
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
        literal = docutils.nodes.literal_block(code, code)
        literal["language"] = "console"
        sphinx.util.nodes.set_source_info(self, literal)
        return [literal]


class ThumbnailDirective(docutils.parsers.rst.Directive):
    """
    A thumbnail directive.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    final_argument_whitespace = True
    has_content = False
    option_spec = {
        "class": docutils.parsers.rst.directives.class_option,
        "group": docutils.parsers.rst.directives.unchanged,
        "title": docutils.parsers.rst.directives.unchanged,
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


class thumbnail_block(
    docutils.nodes.image, docutils.nodes.General, docutils.nodes.Element
):
    __documentation_ignore_inherited__ = True


def visit_thumbnail_block_html(self, node):
    template = uqbar.strings.normalize(
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
    raise docutils.nodes.SkipNode


def visit_thumbnail_block_latex(self, node):
    raise docutils.nodes.SkipNode


def on_builder_inited(app):
    app.env.thumbnails = {}  # separate so Sphinx doesn't purge it
    install_lightbox_static_files(app)
    (pathlib.Path(app.builder.outdir) / "_images").mkdir(exist_ok=True)


class LilyPondExtension(Extension):
    class Kind(enum.Enum):
        IMAGE = 1
        AUDIO = 2

    class lilypond_block(docutils.nodes.General, docutils.nodes.FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            _io.Illustrator,
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
            _io.Player,
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
        cls.add_option("lilypond/no-trim", docutils.parsers.rst.directives.flag)
        cls.add_option("lilypond/pages", docutils.parsers.rst.directives.unchanged)
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
            illustration = _illustrators.illustrate(self.illustrable, **self.keywords)
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
        lilypond_io = _io.LilyPondIO(
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
        raise docutils.nodes.SkipNode


table_row_open_template = '<div class="table-row">'
table_row_close_template = "</div>"
basic_image_template = uqbar.strings.normalize(
    """
    <div class="uqbar-book">
        <a href="{source_path}"><img src="{relative_path}"/></a>
    </div>
    """
)
thumbnail_template = uqbar.strings.normalize(
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
        sphinx.util.console.brown,
        len(relative_file_paths),
    ):
        source_path = os.path.join(source_static_path, relative_file_path)
        target_path = os.path.join(target_static_path, relative_file_path)
        target_directory = os.path.dirname(target_path)
        if not os.path.exists(target_directory):
            sphinx.util.osutil.ensuredir(target_directory)
        sphinx.util.osutil.copyfile(source_path, target_path)
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
