from experimental.abjadbooktools.OutputFormat import OutputFormat


class HTMLOutputFormat(OutputFormat):

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '<pre class="abjad">\n'
        code_block_closing = '</pre>\n'
        image_block = '<img alt="" src="images/{}.png"/>\n'
        image_format = 'png'
        OutputFormat.__init__(self, code_block_opening, code_block_closing,
            image_block, image_format)
