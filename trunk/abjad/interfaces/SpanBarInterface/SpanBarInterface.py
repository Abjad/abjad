from abjad.core import _GrobHandler
from abjad.interfaces._Interface import _Interface


class SpanBarInterface(_Interface, _GrobHandler):
   '''.. versionadded:: 1.1.1

   Manage bar lines that span the space between staves
   in a single system. ::

      abjad> t = Note(0, (1, 4))
      abjad> t.span_bar
      <SpanBarInterface>

   Override LilyPond ``SpanBar`` grob.

   ::

      abjad> t.override.score.span_bar.color = 'red'
      \once \override Score.SpanBar #'color = #red
      c'4
   '''
   
   def __init__(self, _client):
      '''Bind to client.'''

      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'SpanBar')
