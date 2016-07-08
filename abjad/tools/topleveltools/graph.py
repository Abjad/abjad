# -*- coding: utf-8 -*-
import os
import subprocess


def graph(
    expr,
    image_format='pdf',
    layout='dot',
    graph_attributes=None,
    node_attributes=None,
    edge_attributes=None,
    **kwargs
    ):
    r'''Graphs `expr` with graphviz and opens resulting image in
    the default image viewer.

    ::

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> rhythm_tree = rhythmtreetools.RhythmTreeParser()(rtm_syntax)[0]
        >>> print(rhythm_tree.pretty_rtm_format)
        (3 (
            (2 (
                2
                1))
            2))

    ::

        >>> topleveltools.graph(rhythm_tree) # doctest: +SKIP

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import systemtools

    if isinstance(expr, str):
        graphviz_format = expr
    else:
        assert hasattr(expr, '__graph__')
        graphviz_graph = expr.__graph__(**kwargs)
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
