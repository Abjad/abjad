import copy
import enum
import hashlib
import pathlib

from docutils.nodes import FixedTextElement, General, SkipNode
from docutils.parsers.rst import Directive

from abjad.io import Illustrator, LilyPondIO, Player
from abjad.lilypondfile import Block
from uqbar.book.extensions import Extension


class HiddenDoctestDirective(Directive):
    """
    An hidden doctest directive.

    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

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
            lambda self: console.push_proxy(cls(self.illustrable, cls.Kind.IMAGE)),
        )
        monkeypatch.setattr(
            Player,
            "__call__",
            lambda self: console.push_proxy(cls(self.illustrable, cls.Kind.AUDIO)),
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.lilypond_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )

    def __init__(self, illustrable, kind, **keywords):
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
        output_directory = pathlib.Path(self.builder.outdir) / "_images"
        render_prefix = "lilypond-{}".format(hashlib.sha256(node[0].encode()).hexdigest())
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
        for path in output_directory.glob(glob):
            relative_path = (pathlib.Path(self.builder.imgpath) / path.name)
            if path.suffix in (".mid", ".midi"):
                pass
            else:
                self.body.append(f'<img src="{relative_path}" />')
        raise SkipNode


def setup(app):
    app.add_directive("docs", HiddenDoctestDirective)
