# -*- encoding: utf-8 -*-
from abjad.tools.abjadbooktools.OutputFormat import OutputFormat


class LaTeXOutputFormat(OutputFormat):
    r'''LaTeX output format.
    '''

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '\\begin{lstlisting}\n'
        code_block_closing = '\n\end{lstlisting}\n'
        code_indent = 0
        image_block = '\\noindent\\includegraphics[scale={scale}]'
        image_block += '{{images/{image_file_name}.pdf}}\n'
        image_format = 'pdf'
        OutputFormat.__init__(
            self,
            code_block_opening,
            code_block_closing,
            code_indent,
            image_block,
            image_format,
            )