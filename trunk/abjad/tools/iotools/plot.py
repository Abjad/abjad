# -*- encoding: utf-8 -*-
import os
import subprocess


def plot(expr, image_format='png', width=640, height=320):
    r'''Plot `expr` with gnuplot, and open resulting image in 
    the default image viewer.

    Return None.
    '''

    from abjad import abjad_configuration
    from abjad.tools import iotools

    assert image_format in ('pdf', 'png')
    assert isinstance(width, int) and 0 < width
    assert isinstance(height, int) and 0 < height
    assert iotools.which('gnuplot'), 'Cannot find `gnuplot` command-line tool.'

    gnuplot_format = expr.gnuplot_format

    current_directory = os.path.abspath('.')
    ABJADOUTPUT = abjad_configuration['abjad_output']
    iotools.verify_output_directory(ABJADOUTPUT)
    txt_path = os.path.join(
        ABJADOUTPUT, iotools.get_next_output_file_name(file_extension='txt'))
    img_path = os.path.join(ABJADOUTPUT, txt_path.replace('txt', image_format))

    if image_format == 'png':
        image_format = 'pngcairo'

    gnuplot_format = gnuplot_format.format(
        filename=img_path,
        image_format=image_format,
        height=height,
        width=width
        )

    with open(txt_path, 'w') as f:
        f.write(gnuplot_format)

    command = 'gnuplot {}'.format(txt_path)
    subprocess.call(command, shell=True)

    pdf_viewer = abjad_configuration['pdf_viewer']
    ABJADOUTPUT = abjad_configuration['abjad_output']
    iotools.open_file(img_path, pdf_viewer)
