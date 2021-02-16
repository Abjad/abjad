import cProfile
import datetime
import hashlib
import io
import os
import pathlib
import pstats
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
import typing

import uqbar

import abjad

from .configuration import Configuration
from .contextmanagers import Timer
from .illustrators import illustrate
from .lilypondfile import Block
from .parentage import Parentage
from .score import Container, Leaf, Tuplet

configuration = Configuration()


class AbjadGrapher(uqbar.graphs.Grapher):
    """
    Abjad grapher.
    """

    ### INTIALIZER ###

    def __init__(self, graphable, format_="pdf", layout="dot"):
        uqbar.graphs.Grapher.__init__(self, graphable, format_=format_, layout=layout)

    ### PUBLIC METHODS ###

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(configuration["abjad_output_directory"])

    def open_output_path(self, output_path):
        open_file(str(output_path))


class LilyPondIO:
    """
    LilyPond IO.
    """

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
        for directory in self.get_stylesheets_directories():
            for path in directory.glob("*.*ly"):
                shutil.copy(path, render_directory)

    def get_lilypond_path(self):
        lilypond_path = configuration.get("lilypond_path")
        if not lilypond_path:
            lilypond_paths = find_executable("lilypond")
            if lilypond_paths:
                lilypond_path = lilypond_paths[0]
            else:
                lilypond_path = "lilypond"
        return lilypond_path

    def get_openable_paths(self, output_paths) -> typing.Generator:
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
        return lilypond_file._get_lilypond_format()

    def get_stylesheets_directories(self) -> typing.List[pathlib.Path]:
        directories = []
        path = getattr(abjad, "__path__")
        abjad_path = pathlib.Path(path[0])
        directory = abjad_path / ".." / "docs" / "source" / "_stylesheets"
        directories.append(directory)
        if "sphinx_stylesheets_directory" in configuration:
            string = configuration["sphinx_stylesheets_directory"]
            directory = pathlib.Path(string)
            directories.append(directory)
        return directories

    def migrate_assets(
        self, render_prefix, render_directory, output_directory
    ) -> typing.Sequence[pathlib.Path]:
        migrated_assets = []
        for old_path in render_directory.iterdir():
            if not old_path.name.startswith(render_prefix):
                continue
            new_path = output_directory / old_path.name
            shutil.copy(old_path, new_path)
            migrated_assets.append(new_path)
        return migrated_assets

    def open_output_path(self, output_path):
        open_file(str(output_path))

    def persist_log(self, string, input_path):
        input_path.write_text(string)

    def persist_string(self, string, input_path):
        input_path.write_text(string)

    def run_command(self, command):
        completed_process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        text = completed_process.stdout.decode("utf-8")
        success = completed_process.returncode == 0
        return text, success


class Illustrator(LilyPondIO):
    """
    Illustrator.
    """

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> typing.Generator:
        for path in output_paths:
            if path.suffix == ".pdf":
                yield path


class Player(LilyPondIO):
    """
    Player.
    """

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> typing.Generator:
        for path in output_paths:
            if path.suffix in (".mid", ".midi"):
                yield path

    def get_string(self) -> str:
        lilypond_file = illustrate(self.illustrable, **self.keywords)
        assert hasattr(lilypond_file, "score_block")
        block = Block(name="midi")
        lilypond_file.score_block.items.append(block)
        return lilypond_file._get_lilypond_format()


### PRIVATE FUCTIONS ###


def _as_graphviz_node(component):
    score_index = Parentage(component).score_index()
    score_index = "_".join(str(_) for _ in score_index)
    class_name = type(component).__name__
    if score_index:
        name = f"{class_name}_{score_index}"
    else:
        name = class_name
    node = uqbar.graphs.Node(name=name, attributes={"margin": 0.05, "style": "rounded"})
    table = uqbar.graphs.Table(attributes={"border": 2, "cellpadding": 5})
    node.append(table)

    if isinstance(component, Container):
        node[0].append(
            uqbar.graphs.TableRow(
                [
                    uqbar.graphs.TableCell(
                        type(component).__name__, attributes={"border": 0}
                    )
                ]
            )
        )

    if isinstance(component, Tuplet):
        node[0].extend(
            [
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            label=type(component).__name__, attributes={"border": 0}
                        )
                    ]
                ),
                uqbar.graphs.HRule(),
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            label=f"* {component.multiplier!s}",
                            attributes={"border": 0},
                        )
                    ]
                ),
            ]
        )

    if isinstance(component, Leaf):
        lilypond_format = component._get_compact_representation()
        lilypond_format = lilypond_format.replace("<", "&lt;")
        lilypond_format = lilypond_format.replace(">", "&gt;")
        node[0].extend(
            [
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            type(component).__name__, attributes={"border": 0}
                        )
                    ]
                ),
                uqbar.graphs.HRule(),
                uqbar.graphs.TableRow(
                    [uqbar.graphs.TableCell(lilypond_format, attributes={"border": 0})]
                ),
            ]
        )

    return node


def _graph_container(container):
    assert isinstance(container, Container), repr(container)

    def recurse(component, leaf_cluster):
        component_node = _as_graphviz_node(component)
        node_mapping[component] = component_node
        node_order = [component_node.name]
        if isinstance(component, Container):
            graph.append(component_node)
            this_leaf_cluster = uqbar.graphs.Graph(
                name=component_node.name,
                attributes={"color": "grey75", "penwidth": 2},
            )
            all_are_leaves = True
            pending_node_order = []
            for child in component:
                if not isinstance(child, Leaf):
                    all_are_leaves = False
                child_node, child_node_order = recurse(child, this_leaf_cluster)
                pending_node_order.extend(child_node_order)
                edge = uqbar.graphs.Edge()
                edge.attach(component_node, child_node)
            if all_are_leaves:
                pending_node_order.reverse()
            node_order.extend(pending_node_order)
            if len(this_leaf_cluster):
                leaf_cluster.append(this_leaf_cluster)
        else:
            leaf_cluster.append(component_node)
        return component_node, node_order

    node_order = []
    node_mapping = {}
    graph = uqbar.graphs.Graph(
        name="G",
        attributes={"style": "rounded"},
        edge_attributes={},
        node_attributes={"fontname": "Arial", "shape": "none"},
    )
    leaf_cluster = uqbar.graphs.Graph(name="leaves")
    component_node, node_order = recurse(container, leaf_cluster)
    if len(leaf_cluster) == 1:
        graph.append(leaf_cluster[0])
    elif len(leaf_cluster):
        graph.append(leaf_cluster)
    graph._node_order = node_order
    return graph


def _compare_backup(path):
    if isinstance(path, str):
        paths = [path]
    elif isinstance(path, pathlib.Path):
        paths = [str(path)]
    elif isinstance(path, (tuple, list)):
        paths = [str(_) for _ in path]
    else:
        raise TypeError(path)
    for path in paths:
        backup_path = path + ".backup"
        if not compare_files(path, backup_path):
            return False
    return True


def _compare_lys(path_1, path_2):
    """
    Compares LilyPond file ``path_1`` to LilyPond file ``path_2``.

    Performs line-by-line comparison.

    Discards blank lines.

    Discards any LilyPond version statements.

    Discards any lines beginning with ``%``.

    Returns true or false.
    """
    file_1_lines = _normalize_ly(path_1)
    file_2_lines = _normalize_ly(path_2)
    return file_1_lines == file_2_lines


def _compare_text_files(path_1, path_2):
    """
    Compares text file ``path_1`` to text file ``path_2``.

    Performs line-by-line comparison.

    Discards blank lines.

    Trims whitespace from the end of each line.

    Returns true or false.
    """
    file_1_lines, file_2_lines = [], []
    with open(path_1, "r") as file_pointer:
        for line in file_pointer.readlines():
            line = line.strip()
            if line == "":
                continue
            file_1_lines.append(line)
    with open(path_2, "r") as file_pointer:
        for line in file_pointer.readlines():
            line = line.strip()
            if line == "":
                continue
            file_2_lines.append(line)
    return file_1_lines == file_2_lines


def _normalize_ly(path):
    lines = []
    with open(path, "r") as file_pointer:
        for line in file_pointer.readlines():
            line = line.strip()
            if line == "":
                continue
            if line.startswith(r"\version"):
                continue
            elif line.startswith("%"):
                continue
            lines.append(line)
    return lines


def _ensure_directory_existence(directory):
    if not directory:
        directory = "."
    if not os.path.isdir(directory):
        lines = []
        line = f"Attention: {directory!r} does not exist on your system."
        lines.append(line)
        lines.append("Abjad will now create it to store all output files.")
        lines.append("Press any key to continue.")
        message = "\n".join(lines)
        input(message)
        os.makedirs(directory)


def _read_from_pipe(pipe):
    lines = []
    string = pipe.read()
    for line in string.splitlines():
        line = line.decode(errors="ignore")
        lines.append(line)
    return "\n".join(lines)


### FUNCTIONS ###


def count_function_calls(
    argument: str,
    *,
    global_context: dict = None,
    local_context: dict = None,
    fixed_point: bool = True,
) -> int:
    """
    Counts function calls required to execute ``argument``.
    """

    def extract_count(profile_output) -> int:
        return int(profile_output.splitlines()[2].split()[0])

    if fixed_point:
        # profile at least twice to ensure consist results from profiler;
        # not sure why but profiler eventually levels off to consistent
        # output
        last_result, current_result = -1, 0
        while current_result != last_result:
            last_result = current_result
            string = profile(
                argument,
                print_to_terminal=False,
                global_context=global_context,
                local_context=local_context,
            )
            assert isinstance(string, str)
            current_result = extract_count(string)
        return current_result
    result = profile(
        argument,
        print_to_terminal=False,
        global_context=global_context,
        local_context=local_context,
    )
    assert isinstance(result, str)
    count = extract_count(result)
    return count


def graph(
    graphable,
    format_="pdf",
    layout="dot",
    return_timing=False,
    **keywords,
):
    r"""
    Graphs ``argument``.

    ..  container:: example

        Graphs staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__(), "graphviz"))
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

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4

    ..  container:: example

        Shows staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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
    illustrator = Illustrator(illustrable, **keywords)
    result = illustrator()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def compare_files(path_1, path_2):
    """
    Compares file ``path_1`` to file ``path_2``.

    For all file types::

    * Performs line-by-line comparison
    * Discards blank lines

    For LilyPond files, additionally::

    * Discards any LilyPond version statements
    * Discards any lines beginning with ``%``

    Returns true when files compare the same and false when files compare
    differently.
    """
    path_1 = str(path_1)
    path_2 = str(path_2)
    if os.path.exists(path_1) and not os.path.exists(path_2):
        return False
    elif not os.path.exists(path_1) and os.path.exists(path_2):
        return False
    elif not os.path.exists(path_1) and not os.path.exists(path_2):
        return True
    if path_1.endswith(".backup"):
        path_1 = path_1.strip(".backup")
    if path_2.endswith(".backup"):
        path_2 = path_2.strip(".backup")
    base_1, extension_1 = os.path.splitext(path_1)
    base_2, extension_2 = os.path.splitext(path_2)
    assert extension_1 == extension_2
    if extension_1 == ".ly":
        return _compare_lys(path_1, path_2)
    else:
        return _compare_text_files(path_1, path_2)


def execute_file(
    path: str = None, *, attribute_names: typing.Tuple[str] = None
) -> typing.Optional[typing.Tuple[str]]:
    """
    Executes file ``path``.

    Returns ``attribute_names`` from file.
    """
    assert path is not None
    assert isinstance(attribute_names, tuple)
    path_ = pathlib.Path(path)
    if not path_.is_file():
        return None
    file_contents_string = path_.read_text()
    try:
        result = execute_string(file_contents_string, attribute_names=attribute_names)
    except Exception:
        message = f"Exception raised in {path_}."
        # use print instead of display
        # to force to terminal even when called in silent context
        print(message)
        traceback.print_exc()
    return result


def execute_string(
    string: str,
    *,
    attribute_names: typing.Tuple[str] = None,
    local_namespace: dict = None,
):
    """
    Executes ``string``.

    ..  container:: example

        >>> string = 'foo = 23'
        >>> attribute_names = ('foo', 'bar')
        >>> abjad.io.execute_string(
        ...     string,
        ...     attribute_names=attribute_names,
        ...     )
        (23, None)

    Returns ``attribute_names`` from executed string.
    """
    assert isinstance(string, str)
    assert isinstance(attribute_names, tuple)
    if local_namespace is None:
        local_namespace = {}
    assert isinstance(local_namespace, dict)
    local_namespace = {}
    try:
        exec(string, local_namespace, local_namespace)
    except SyntaxError:
        return
    result = []
    for name in attribute_names:
        if name in local_namespace:
            result.append(local_namespace[name])
        else:
            result.append(None)
    return tuple(result)


def find_executable(name: str, *, flags: int = os.X_OK) -> typing.List[pathlib.Path]:
    """
    Finds executable ``name``.

    Similar to Unix ``which`` command.

    Returns list of zero or more full paths to ``name``.
    """
    result = []
    extensions = [x for x in os.environ.get("PATHEXT", "").split(os.pathsep) if x]
    PATH = os.environ.get("PATH", None)
    if PATH is None:
        return []
    for path_ in os.environ.get("PATH", "").split(os.pathsep):
        path = pathlib.Path(path_) / name
        if os.access(path, flags):
            result.append(path)
        for extension in extensions:
            path_extension = path / extension
            if os.access(path_extension, flags):
                result.append(path_extension)
    return result


# TODO: merge into run_command()
def make_subprocess(command: str) -> subprocess.Popen:
    """
    Makes Popen instance.

    Defined equal to:

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )

    Redirects stderr to stdout.
    """
    # TODO: replace with subprocess.run()
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def open_file(
    file_path: str,
    *,
    application: str = None,
    line_number: int = None,
    test: bool = None,
):
    """
    Opens ``file_path``.

    Uses ``application`` when ``application`` is not none.

    Uses Abjad configuration file ``text_editor`` when
    ``application`` is none.

    Takes best guess at operating system-specific file opener when both
    ``application`` and Abjad configuration file ``text_editor`` are none.

    Respects ``line_number`` when ``file_path`` can be opened with text
    editor.
    """
    if sys.platform.lower().startswith("win"):
        startfile = getattr(os, "startfile", None)
        assert startfile is not None
        startfile(file_path)
        return
    viewer = None
    if sys.platform.lower().startswith("linux"):
        viewer = application or "xdg-open"
    elif file_path.endswith(".pdf"):
        viewer = application or configuration["pdf_viewer"]
    elif file_path.endswith((".log", ".py", ".rst", ".txt")):
        viewer = application or configuration["text_editor"]
    elif file_path.endswith((".mid", ".midi")):
        viewer = application or configuration["midi_player"]
    viewer = viewer or "open"
    if line_number:
        command = f"{viewer} +{line_number} {file_path}"
    else:
        command = f"{viewer} {file_path}"
    if not test:
        spawn_subprocess(command)


def open_last_log() -> None:
    """
    Opens LilyPond log file in operating system-specific text editor.
    """
    text_editor = configuration.get("text_editor")
    file_path = configuration.lilypond_log_file_path
    open_file(str(file_path), application=text_editor)


def profile(
    argument: str,
    *,
    global_context: dict = None,
    line_count: int = 12,
    local_context: dict = None,
    print_callers: bool = False,
    print_callees: bool = False,
    print_to_terminal: bool = True,
    sort_by: str = "cumulative",
    strip_dirs: bool = True,
) -> typing.Optional[str]:
    """
    Profiles ``argument``.

    ..  container:: example

        ::

            >>> argument = 'abjad.Staff("c8 c8 c8 c8 c8 c8 c8 c8")'
            >>> abjad.io.profile(
            ...     argument,
            ...     global_context=globals(),
            ...     ) # doctest: +SKIP
            Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                    2852 function calls (2829 primitive calls) in 0.006 CPU seconds

            Ordered by: cumulative time
            List reduced from 118 to 12 due to restriction <12>

            ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                    1    0.000    0.000    0.006    0.006 <string>:1(<module>)
                    1    0.001    0.001    0.003    0.003 make_notes.py:12(make_not
                    1    0.000    0.000    0.003    0.003 Staff.py:21(__init__)
                    1    0.000    0.000    0.003    0.003 Context.py:11(__init__)
                    1    0.000    0.000    0.003    0.003 Container.py:23(__init__)
                    1    0.000    0.000    0.003    0.003 Container.py:271(_initial
                    2    0.000    0.000    0.002    0.001 all_are_logical_voice_con
                52    0.001    0.000    0.002    0.000 component_to_logical_voic
                    1    0.000    0.000    0.002    0.002 _construct_unprolated_not
                    8    0.000    0.000    0.002    0.000 make_tied_note.py:5(make_
                    8    0.000    0.000    0.002    0.000 make_tied_leaf.py:5(make_

    Wraps the built-in Python ``cProfile`` module.

    Set ``argument`` to any string of Abjad input.

    Set ``sort_by`` to ``'cumulative'``, ``'time'`` or ``'calls'``.

    Set ``line_count`` to any nonnegative integer.

    Set ``strip_dirs`` to true to strip directory names from output lines.

    See the `Python docs <http://docs.python.org/library/profile.html>`_
    for more information on the Python profilers.

    Returns none when ``print_to_terminal`` is false.

    Returns string when ``print_to_terminal`` is true.
    """
    now_string = datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y")
    profile = cProfile.Profile()
    local_context = local_context or locals()
    if global_context is None:
        profile = profile.run(argument)
    else:
        profile = profile.runctx(argument, global_context, local_context)
    stats_stream = io.StringIO()
    stats = pstats.Stats(profile, stream=stats_stream)
    if sort_by == "cum":
        sort_by = "cumulative"
    if strip_dirs:
        stats.strip_dirs().sort_stats(sort_by).print_stats(line_count)
    else:
        stats.sort_stats(sort_by).print_stats(line_count)
    if print_callers:
        stats.sort_stats(sort_by).print_callers(line_count)
    if print_callees:
        stats.sort_stats(sort_by).print_callees(line_count)
    result = now_string + "\n\n" + stats_stream.getvalue()
    stats_stream.close()
    if print_to_terminal:
        print(result)
        return None
    return result


def run_command(command: str) -> typing.List[str]:
    """
    Runs command in subprocess.

    Returns list of strings read from subprocess stdout.
    """
    process = make_subprocess(command)
    lines = _read_from_pipe(process.stdout)
    lines = lines.splitlines()
    return lines


def run_lilypond(
    ly_path: str,
    *,
    flags: str = None,
    lilypond_log_file_path: pathlib.Path = None,
) -> bool:
    """
    Runs LilyPond on ``ly_path``.

    Writes redirected output of Unix ``date`` to top line of LilyPond log
    file.

    Then appends redirected output of LilyPond output to the LilyPond log
    file.
    """
    ly_path = str(ly_path)
    lilypond_path_ = configuration.get("lilypond_path")
    if lilypond_path_ is not None:
        assert isinstance(lilypond_path_, str), repr(lilypond_path_)
    if not lilypond_path_:
        lilypond_paths = find_executable("lilypond")
        if lilypond_paths:
            lilypond_path_ = str(lilypond_paths[0])
        else:
            lilypond_path_ = "lilypond"
    lilypond_base, extension = os.path.splitext(ly_path)
    flags = flags or ""
    date = datetime.datetime.now().strftime("%c")
    if lilypond_log_file_path is None:
        log_file_path = configuration.lilypond_log_file_path
    else:
        log_file_path = lilypond_log_file_path
    command = "{} {} -dno-point-and-click -o {} {}".format(
        lilypond_path_, flags, lilypond_base, ly_path
    )
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    subprocess_output, _ = process.communicate()
    subprocess_output_string = subprocess_output.decode(errors="ignore")
    exit_code = process.returncode
    with open(log_file_path, "w") as file_pointer:
        file_pointer.write(date + "\n")
        file_pointer.write(subprocess_output_string)
    postscript_path = ly_path.replace(".ly", ".ps")
    try:
        os.remove(postscript_path)
    except OSError:
        pass
    # TODO: maybe just 'return exit_code'?
    if exit_code:
        return False
    return True


def spawn_subprocess(command: str) -> int:
    """
    Spawns subprocess and runs ``command``.

    The function is basically a reimplementation of the
    deprecated ``os.system()`` using Python's ``subprocess`` module.

    Redirects stderr to stdout.
    """
    return subprocess.call(command, shell=True)
