from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _SpanBarInterface(_Interface, _GrobHandler):
   '''.. versionadded:: 1.1.1

   Manage barlines that span the space between staves
   in a single system. ::

      abjad> t = Note(0, (1, 4))
      abjad> t.barline
      <_SpanBarInterface>

   Override LilyPond ``SpanBar`` grob.

   ::

      abjad> t.spanbar.color = 'red'
      abjad> t.spanbar.promote('color', 'Score')
      abjad> print t.format
      \once \override Score.SpanBar #'color = #red
      c'4
   '''
   
   def __init__(self, _client):
      '''Bind to client.'''

      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'SpanBar')
