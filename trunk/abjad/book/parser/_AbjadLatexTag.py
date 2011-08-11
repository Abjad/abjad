from abjad.book.parser._AbjadTag import _AbjadTag


class _AbjadLatexTag(_AbjadTag):

    def __init__(self, lines, skip_rendering):
        _AbjadTag.__init__(self, lines, skip_rendering)

        self._target_open_tag = '\\begin{lstlisting}'
        self._target_open_tag += '[basicstyle=\\footnotesize, tabsize=4, '
        self._target_open_tag += 'showtabs=false, showspaces=false]\n'

        self._target_close_tag = '\\end{lstlisting}\n'

        self._image_tag = '\\includegraphics{images/%s.pdf}\n'
