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
from abjad.lilypondfile import Block
from abjad.system import AbjadConfiguration, IOManager, Timer

_configuration = AbjadConfiguration()


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
        lilypond_path = _configuration.get("lilypond_path")
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
        return pathlib.Path(_configuration["abjad_output_directory"])

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
        lilypond_file = self.illustrable.__illustrate__(**self.keywords)
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
        return pathlib.Path(_configuration["abjad_output_directory"])

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
    if not hasattr(illustrable, "__illustrate__"):
        raise ValueError(r"Cannot illustrate {illustrable!r}")
    illustrator = Illustrator(illustrable, **keywords)
    result = illustrator()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time
