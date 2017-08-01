# -*- coding: utf-8 -*-
import os
import subprocess


def graph(
    argument,
    image_format='pdf',
    layout='dot',
    graph_attributes=None,
    node_attributes=None,
    edge_attributes=None,
    **keywords
    ):
    r'''Graphs `argument`.

    ::

        >>> import abjad

    ..  container:: example

        Graphs staff:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__()))
            graphtools.GraphvizGraph(
                attributes={
                    'style': 'rounded',
                    },
                children=(
                    graphtools.GraphvizNode(
                        attributes={
                            'margin': 0.05,
                            },
                        children=(
                            graphtools.GraphvizTable(
                                children=(
                                    graphtools.GraphvizTableRow(
                                        children=(
                                            graphtools.GraphvizTableCell(
                                                label='Staff',
                                                attributes={
                                                    'border': 0,
                                                    },
                                                ),
                                            ),
                                        ),
                                    ),
                                attributes={
                                    'border': 2,
                                    'cellpadding': 5,
                                    'style': 'rounded',
                                    },
                                ),
                            ),
                        name='Staff',
                        ),
                    graphtools.GraphvizSubgraph(
                        attributes={
                            'color': 'grey75',
                            'penwidth': 2,
                            },
                        children=(
                            graphtools.GraphvizNode(
                                attributes={
                                    'margin': 0.05,
                                    },
                                children=(
                                    graphtools.GraphvizTable(
                                        children=(
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label='Note',
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            graphtools.GraphvizTableHorizontalRule(),
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label="c'4",
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        attributes={
                                            'border': 2,
                                            'cellpadding': 5,
                                            'style': 'rounded',
                                            },
                                        ),
                                    ),
                                name='Note_0',
                                ),
                            graphtools.GraphvizNode(
                                attributes={
                                    'margin': 0.05,
                                    },
                                children=(
                                    graphtools.GraphvizTable(
                                        children=(
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label='Note',
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            graphtools.GraphvizTableHorizontalRule(),
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label="d'4",
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        attributes={
                                            'border': 2,
                                            'cellpadding': 5,
                                            'style': 'rounded',
                                            },
                                        ),
                                    ),
                                name='Note_1',
                                ),
                            graphtools.GraphvizNode(
                                attributes={
                                    'margin': 0.05,
                                    },
                                children=(
                                    graphtools.GraphvizTable(
                                        children=(
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label='Note',
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            graphtools.GraphvizTableHorizontalRule(),
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label="e'4",
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        attributes={
                                            'border': 2,
                                            'cellpadding': 5,
                                            'style': 'rounded',
                                            },
                                        ),
                                    ),
                                name='Note_2',
                                ),
                            graphtools.GraphvizNode(
                                attributes={
                                    'margin': 0.05,
                                    },
                                children=(
                                    graphtools.GraphvizTable(
                                        children=(
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label='Note',
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            graphtools.GraphvizTableHorizontalRule(),
                                            graphtools.GraphvizTableRow(
                                                children=(
                                                    graphtools.GraphvizTableCell(
                                                        label="f'4",
                                                        attributes={
                                                            'border': 0,
                                                            },
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        attributes={
                                            'border': 2,
                                            'cellpadding': 5,
                                            'style': 'rounded',
                                            },
                                        ),
                                    ),
                                name='Note_3',
                                ),
                            ),
                        edge_attributes={
                            },
                        is_cluster=True,
                        name='Staff',
                        node_attributes={
                            },
                        ),
                    ),
                edge_attributes={
                    },
                is_digraph=True,
                name='G',
                node_attributes={
                    'fontname': 'Arial',
                    'shape': 'none',
                    },
                )

    ..  container:: example

        Graphs rhythm tree:

        ::

            >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
            >>> parser = abjad.rhythmtreetools.RhythmTreeParser()
            >>> rhythm_tree = parser(rtm_syntax)[0]
            >>> topleveltools.graph(rhythm_tree) # doctest: +SKIP

        ..  docs::

            >>> print(format(rhythm_tree.__graph__()))
            graphtools.GraphvizGraph(
                attributes={
                    'bgcolor': 'transparent',
                    'truecolor': True,
                    },
                children=(
                    graphtools.GraphvizNode(
                        attributes={
                            'label': '3',
                            'shape': 'triangle',
                            },
                        ),
                    graphtools.GraphvizNode(
                        attributes={
                            'label': '2',
                            'shape': 'triangle',
                            },
                        ),
                    graphtools.GraphvizNode(
                        attributes={
                            'label': '2',
                            'shape': 'box',
                            },
                        ),
                    graphtools.GraphvizNode(
                        attributes={
                            'label': '1',
                            'shape': 'box',
                            },
                        ),
                    graphtools.GraphvizNode(
                        attributes={
                            'label': '2',
                            'shape': 'box',
                            },
                        ),
                    ),
                edge_attributes={
                    },
                is_digraph=True,
                name='G',
                node_attributes={
                    },
                )

    Creates GraphViz object.

    Opens image in default image viewer.

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import systemtools

    if isinstance(argument, str):
        graphviz_format = argument
    else:
        assert hasattr(argument, '__graph__')
        graphviz_graph = argument.__graph__(**keywords)
        if graph_attributes:
            graphviz_graph.attributes.update(graph_attributes)
        if node_attributes:
            graphviz_graph.node_attributes.update(node_attributes)
        if edge_attributes:
            graphviz_graph.edge_attributes.update(edge_attributes)
        graphviz_format = str(graphviz_graph)

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
    assert systemtools.IOManager.find_executable(layout), message

    ABJADOUTPUT = abjad_configuration['abjad_output_directory']
    systemtools.IOManager._ensure_directory_existence(ABJADOUTPUT)
    dot_path = os.path.join(
        ABJADOUTPUT,
        systemtools.IOManager.get_next_output_file_name(file_extension='dot'),
        )
    img_path = os.path.join(ABJADOUTPUT, dot_path.replace('dot', 'pdf'))

    with open(dot_path, 'w') as f:
        f.write(graphviz_format)

    command = '{} -v -T{} {} -o {}'
    command = command.format(layout, image_format, dot_path, img_path)
    subprocess.call(command, shell=True)

    pdf_viewer = abjad_configuration['pdf_viewer']
    ABJADOUTPUT = abjad_configuration['abjad_output_directory']
    systemtools.IOManager.open_file(img_path, pdf_viewer)
