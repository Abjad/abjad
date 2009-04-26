from abjad.book.parser.abjadtag import _AbjadTag

class AbjadLatexTag(_AbjadTag):
   def __init__(self, lines):
      _AbjadTag.__init__(self, lines)
#      self._target_open_tag = '\\begin{minipage}{5in} \\footnotesize \\begin{verbatim}\n'
#      self._target_close_tag = '\\end{verbatim} \\normalsize \\end{minipage}\n'
      self._target_open_tag = '\\begin{lstlisting}[basicstyle=\\footnotesize, tabsize=4, showtabs=false, showspaces=false]\n'
      self._target_close_tag = '\\end{lstlisting}\n'

      self._image_tag = '\\begin{center}\n \\includegraphics{images/%s.png}\n\\end{center}'
