from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces._Interface import _Interface


class NonMusicalPaperColumnInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.2.

   Handle the LilyPond NonMusicalPaperColumn grob. ::

      abjad> t = Score([Staff(macros.scale(4))])
      abjad> t.non_musical_paper_column.line_break_permission = False
      abjad> t.non_musical_paper_column.page_break_permission = False

   ::

      abjad> print t.format
      \new Score \with {
              \override NonMusicalPaperColumn #'line-break-permission = ##f
              \override NonMusicalPaperColumn #'page-break-permission = ##f
      } <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
      >>
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'NonMusicalPaperColumn')
