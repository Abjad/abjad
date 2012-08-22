from abjad.tools.abjadbooktools.OutputFormat import OutputFormat


class LaTeXOutputFormat(OutputFormat):

    ### INITIALIZER ###

    def __init__(self):
        code_block_opening = '\\begin{lstlisting}'
        code_block_opening += '[basicstyle=\\footnotesize, tabsize=4, '
        code_block_opening += 'showtabs=false, showspaces=false]\n'
        code_block_closing = '\\end{lstlisting}\n'
        code_indent = 0
        image_block = '\\includegraphics{images/{}.pdf}\n'
        image_format = 'pdf'
        OutputFormat.__init__(self, code_block_opening, code_block_closing,
            code_indent, image_block, image_format)
