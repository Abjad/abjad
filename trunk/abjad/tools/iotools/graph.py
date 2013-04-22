import os
import subprocess


def graph(expr, image_format='pdf', layout='dot'):
    '''Graph `expr` with graphviz, and open resulting image in the default image viewer:

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

        >>> graph(rhythm_tree) # doctest: +SKIP

    Return None.
    '''

    from abjad import ABJCFG
    from abjad.tools import iotools
    from abjad.tools.iotools._open_file import _open_file
    from abjad.tools.iotools._verify_output_directory import _verify_output_directory

    assert image_format in ('pdf', 'png')
    assert layout in ('circo', 'dot', 'fdp', 'neato', 'osage', 'sfdp', 'twopi')
    assert iotools.which(layout), 'Cannot find `{}` command-line tool.'.format(layout)

    if isinstance(expr, str):
        graphviz_format = expr
    else:
        graphviz_format = expr.graphviz_format

    current_directory = os.path.abspath('.')
    ABJADOUTPUT = ABJCFG['abjad_output']
    _verify_output_directory(ABJADOUTPUT)
    dot_path = os.path.join(ABJADOUTPUT, iotools.get_next_output_file_name(file_extension='dot'))
    img_path = os.path.join(ABJADOUTPUT, dot_path.replace('dot', 'pdf'))

    with open(dot_path, 'w') as f:
        f.write(graphviz_format)

    command = '{} -v -T{} {} -o {}'.format(layout, image_format, dot_path, img_path)
    subprocess.call(command, shell=True)

    pdf_viewer = ABJCFG['pdf_viewer']
    ABJADOUTPUT = ABJCFG['abjad_output']
    _open_file(img_path, pdf_viewer)
