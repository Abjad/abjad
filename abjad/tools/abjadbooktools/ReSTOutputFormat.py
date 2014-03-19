# -*- encoding: utf-8 -*-
from abjad.tools.abjadbooktools.OutputFormat import OutputFormat


class ReSTOutputFormat(OutputFormat):
    r'''ReST output format.
    '''

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '::\n\n'
        code_block_closing = '\n'
        code_indent = 3
        image_block = '.. image:: images/{image_file_name}.png\n'
        image_format = 'png'
        OutputFormat.__init__(
            self,
            code_block_opening,
            code_block_closing,
            code_indent,
            image_block,
            image_format,
            )
