import os
import subprocess


def graph(expr, image_format='pdf', layout='dot'):
    r'''Graph `expr` with graphviz, and open resulting image in 
    the default image viewer:

    ::

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> rhythm_tree = rhythmtreetools.RhythmTreeParser()(rtm_syntax)[0]
        >>> print rhythm_tree.pretty_rtm_format
        (3 (
            (2 (
                2
                1))
            2))

    ::

        >>> iotools.graph(rhythm_tree) # doctest: +SKIP

    Return None.
    '''

    from abjad import abjad_configuration
    from abjad.tools import iotools

    assert image_format in ('pdf', 'png')
    assert layout in ('circo', 'dot', 'fdp', 'neato', 'osage', 'sfdp', 'twopi')
    assert iotools.which(layout), 'Cannot find `{}` command-line tool.'.format(layout)

    if isinstance(expr, str):
        graphviz_format = expr
    else:
        graphviz_format = expr.graphviz_format

    current_directory = os.path.abspath('.')
    ABJADOUTPUT = abjad_configuration['abjad_output']
    iotools.verify_output_directory(ABJADOUTPUT)
    dot_path = os.path.join(
        ABJADOUTPUT,
        iotools.get_next_output_file_name(file_extension='dot')
        )
    img_path = os.path.join(ABJADOUTPUT, dot_path.replace('dot', 'pdf'))

    with open(dot_path, 'w') as f:
        f.write(graphviz_format)

    command = '{} -v -T{} {} -o {}'.format(
        layout, image_format, dot_path, img_path)
    subprocess.call(command, shell=True)

    pdf_viewer = abjad_configuration['pdf_viewer']
    ABJADOUTPUT = abjad_configuration['abjad_output']
    iotools.open_file(img_path, pdf_viewer)
