from abjad.tools.abjadbooktools.OutputFormat import OutputFormat


class ReSTOutputFormat(OutputFormat):

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '::\n\n'
        code_block_closing = '\n'
        code_indent = 3
        image_block = '.. image:: images/{}.png\n'
        image_format = 'png'
        OutputFormat.__init__(self, code_block_opening, code_block_closing,
            code_indent, image_block, image_format)
