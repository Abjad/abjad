import copy
import os
import subprocess
import uqbar.graphs


def graph(
    argument,
    image_format='pdf',
    layout='dot',
    graph_attributes=None,
    node_attributes=None,
    edge_attributes=None,
    **keywords
    ) -> None:
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
    from abjad import system
    from abjad import abjad_configuration

    if isinstance(argument, str):
        graphviz_format = argument
    else:
        if hasattr(argument, '__graph__'):
            graphviz_graph = argument.__graph__(**keywords)
        elif isinstance(argument, uqbar.graphs.Graph):
            graphviz_graph = copy.deepcopy(argument)
        else:
            raise TypeError('Cannot graph {!r}'.format(type(argument)))
        if graph_attributes:
            graphviz_graph.attributes.update(graph_attributes)
        if node_attributes:
            graphviz_graph.node_attributes.update(node_attributes)
        if edge_attributes:
            graphviz_graph.edge_attributes.update(edge_attributes)
        graphviz_format = format(graphviz_graph, 'graphviz')

    assert image_format in ('pdf', 'png')
    valid_layouts = (
        'circo',
        'dot',
        'fdp',
        'neato',
        'osage',
        'sfdp',
        'twopi',
        )
    assert layout in valid_layouts

    message = 'cannot find `{}` command-line tool.'
    message = message.format(layout)
    message += ' Please download Graphviz from graphviz.org.'
    assert system.IOManager.find_executable(layout), message

    ABJADOUTPUT = abjad_configuration['abjad_output_directory']
    system.IOManager._ensure_directory_existence(ABJADOUTPUT)
    dot_path = os.path.join(
        ABJADOUTPUT,
        system.IOManager.get_next_output_file_name(file_extension='dot'),
        )
    img_path = os.path.join(ABJADOUTPUT, dot_path.replace('dot', 'pdf'))

    with open(dot_path, 'w') as f:
        f.write(graphviz_format)

    command = '{} -v -T{} {} -o {}'
    command = command.format(layout, image_format, dot_path, img_path)
    subprocess.call(command, shell=True)

    pdf_viewer = abjad_configuration['pdf_viewer']
    ABJADOUTPUT = abjad_configuration['abjad_output_directory']
    system.IOManager.open_file(img_path, pdf_viewer)
