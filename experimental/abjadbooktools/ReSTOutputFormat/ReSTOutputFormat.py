from experimental.abjadbooktools.OutputFormat import OutputFormat


class ReSTOutputFormat(OutputFormat):

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '::\n\n'
        code_block_closing = '\n'
        image_block = '.. image:: images/%s.png\n'
        image_format = 'png'
        OutputFormat.__init__(self, code_block_opening, code_block_closing,
            image_block, image_format)
