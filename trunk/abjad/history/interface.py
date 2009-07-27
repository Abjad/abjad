from abjad.core.interface import _Interface


class HistoryInterface(_Interface):
   '''Completely empty namespace available for composer labelling.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> t.history.previous_transform = 'foo'
      abjad> t.history.previous_transform
      'foo'

   Abjad ignores HistoryInterface attributes and usage completely.

   The HistoryInterface handles no LilyPond grob.
   '''

   def __init__(self, _client):
      _Interface.__init__(self, _client)
