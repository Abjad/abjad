import datetime
import hashlib
import pathlib
import re
import shutil
import subprocess
import tempfile
from typing import Generator, Sequence

from uqbar.graphs import Grapher

import abjad

from .illustrate import illustrate
from .lilypondfile import Block
from .system.Configuration import Configuration
from .system.IOManager import IOManager
from .system.Timer import Timer

configuration = Configuration()


class LilyPondIO:

    ### INITIALIZER ###

    def __init__(
        self,
        illustrable,
        *,
        flags=None,
        output_directory=None,
        render_prefix=None,
        should_copy_stylesheets=False,
        should_open=True,
        should_persist_log=True,
        string=None,
        **keywords,
    ):
        self.flags = flags or []
        self.illustrable = illustrable
        self.keywords = keywords
        self.output_directory = output_directory
        self.render_prefix = render_prefix
        self.should_copy_stylesheets = bool(should_copy_stylesheets)
        self.should_open = bool(should_open)
        self.should_persist_log = bool(should_persist_log)
        self.string = string

    ### SPECIAL METHODS ###

    def __call__(self):
        with Timer() as format_timer:
            string = self.string or self.get_string()
        format_time = format_timer.elapsed_time
        render_prefix = self.render_prefix or self.get_render_prefix(string)
        render_directory = self.get_render_directory()
        input_path = (render_directory / render_prefix).with_suffix(".ly")
        self.persist_string(string, input_path)
        lilypond_path = self.get_lilypond_path()
        if self.should_copy_stylesheets:
            self.copy_stylesheets(render_directory)
        render_command = self.get_render_command(input_path, lilypond_path)
        with Timer() as render_timer:
            log, success = self.run_command(render_command)
        render_time = render_timer.elapsed_time
        if self.should_persist_log:
            self.persist_log(log, input_path.with_suffix(".log"))
        output_directory = pathlib.Path(
            self.output_directory or self.get_output_directory()
        )
        output_paths = self.migrate_assets(
            render_prefix, render_directory, output_directory
        )
        openable_paths = []
        for output_path in self.get_openable_paths(output_paths):
            openable_paths.append(output_path)
            if self.should_open:
                self.open_output_path(output_path)
        return openable_paths, format_time, render_time, success, log

    ### PUBLIC METHODS ###

    def copy_stylesheets(self, render_directory):
        for path in self.get_stylesheets_path().glob("*.*ly"):
            shutil.copy(path, render_directory)

    def get_lilypond_path(self):
        lilypond_path = configuration.get("lilypond_path")
        if not lilypond_path:
            lilypond_paths = IOManager.find_executable("lilypond")
            if lilypond_paths:
                lilypond_path = lilypond_paths[0]
            else:
                lilypond_path = "lilypond"
        return lilypond_path

    def get_openable_paths(self, output_paths) -> Generator:
        for path in output_paths:
            if path.suffix in (".pdf", ".mid", ".midi", ".svg", ".png"):
                yield path

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(configuration["abjad_output_directory"])

    def get_render_command(self, input_path, lilypond_path) -> str:
        parts = [
            str(lilypond_path),
            *self.flags,
            "-dno-point-and-click",
            "-o",
            str(input_path.with_suffix("")),
            str(input_path),
        ]
        return " ".join(parts)

    def get_render_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def get_render_prefix(self, string) -> str:
        timestamp = re.sub(r"[^\w]", "-", datetime.datetime.now().isoformat())
        checksum = hashlib.sha1(string.encode()).hexdigest()[:7]
        return f"{timestamp}-{checksum}"

    def get_string(self) -> str:
        if hasattr(self.illustrable, "__illustrate__"):
            lilypond_file = self.illustrable.__illustrate__(**self.keywords)
        else:
            lilypond_file = illustrate(self.illustrable, **self.keywords)
        return format(lilypond_file, "lilypond")

    def get_stylesheets_path(self) -> pathlib.Path:
        path = getattr(abjad, "__path__")
        abjad_path = pathlib.Path(path[0])
        return abjad_path / ".." / "docs" / "source" / "_stylesheets"

    def migrate_assets(
        self, render_prefix, render_directory, output_directory
    ) -> Sequence[pathlib.Path]:
        migrated_assets = []
        for old_path in render_directory.iterdir():
            if not old_path.name.startswith(render_prefix):
                continue
            new_path = output_directory / old_path.name
            shutil.copy(old_path, new_path)
            migrated_assets.append(new_path)
        return migrated_assets

    def open_output_path(self, output_path):
        IOManager.open_file(str(output_path))

    def persist_log(self, string, input_path):
        input_path.write_text(string)

    def persist_string(self, string, input_path):
        input_path.write_text(string)

    def run_command(self, command):
        completed_process = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        text = completed_process.stdout.decode("utf-8")
        success = completed_process.returncode == 0
        return text, success


class AbjadGrapher(Grapher):

    ### INTIALIZER ###

    def __init__(self, graphable, format_="pdf", layout="dot"):
        Grapher.__init__(
            self, graphable, format_=format_, layout=layout,
        )

    ### PUBLIC METHODS ###

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(configuration["abjad_output_directory"])

    def open_output_path(self, output_path):
        IOManager.open_file(str(output_path))


class Illustrator(LilyPondIO):

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> Generator:
        for path in output_paths:
            if path.suffix == ".pdf":
                yield path


class Player(LilyPondIO):

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> Generator:
        for path in output_paths:
            if path.suffix in (".mid", ".midi"):
                yield path

    def get_string(self) -> str:
        lilypond_file = self.illustrable.__illustrate__(**self.keywords)
        assert hasattr(lilypond_file, "score_block")
        block = Block(name="midi")
        lilypond_file.score_block.items.append(block)
        return format(lilypond_file, "lilypond")


def graph(
    graphable, format_="pdf", layout="dot", return_timing=False, **keywords,
):
    r"""
    Graphs ``argument``.

    ..  container:: example

        Graphs staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__(), 'graphviz'))
            digraph G {
                graph [style=rounded];
                node [fontname=Arial,
                    shape=none];
                Staff_0 [label=<
                    <TABLE BORDER="2" CELLPADDING="5">
                        <TR>
                            <TD BORDER="0">Staff</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05,
                    style=rounded];
                subgraph Staff {
                    graph [color=grey75,
                        penwidth=2];
                    Note_0 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">c'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_1 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">d'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_2 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">e'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_3 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">f'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                }
                Staff_0 -> Note_0;
                Staff_0 -> Note_1;
                Staff_0 -> Note_2;
                Staff_0 -> Note_3;
            }

    ..  container:: example

        Graphs rhythm tree:

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> rhythm_tree = parser(rtm_syntax)[0]
        >>> abjad.graph(rhythm_tree) # doctest: +SKIP

        ..  docs::

            >>> print(format(rhythm_tree.__graph__(), 'graphviz'))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="3",
                    shape=triangle];
                node_1 [label="2",
                    shape=triangle];
                node_2 [label="2",
                    shape=box];
                node_3 [label="1",
                    shape=box];
                node_4 [label="2",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_4;
                node_1 -> node_2;
                node_1 -> node_3;
            }

    Opens image in default image viewer.
    """
    grapher = AbjadGrapher(graphable, format_=format_, layout=layout, **keywords)
    result = grapher()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def play(illustrable, return_timing=False, **keywords):
    """
    Plays ``argument``.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems.

    Opens MIDI file.
    """
    if not hasattr(illustrable, "__illustrate__"):
        raise ValueError(r"Cannot illustrate {illustrable!r}")
    player = Player(illustrable, **keywords)
    result = player()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def show(illustrable, return_timing=False, **keywords):
    r"""
    Shows ``argument``.

    ..  container:: example

        Shows note:

        >>> note = abjad.Note("c'4")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4

    ..  container:: example

        Shows staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

    Makes LilyPond input files and output PDF.

    Writes LilyPond input file and output PDF to Abjad output directory.

    Opens output PDF.

    Returns none when ``return_timing`` is false.

    Returns pair of ``abjad_formatting_time`` and ``lilypond_rendering_time``
    when ``return_timing`` is true.
    """
    #    if not hasattr(illustrable, "__illustrate__"):
    #        raise ValueError(f"Cannot illustrate {illustrable!r}")
    illustrator = Illustrator(illustrable, **keywords)
    result = illustrator()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time
