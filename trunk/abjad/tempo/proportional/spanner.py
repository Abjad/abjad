from abjad.tempo.proportional.format import _TempoProportionalFormatInterface
from abjad.tempo.spanner import Tempo
import types


class TempoProportional(Tempo):
   '''Tempo spanner aware of score-global spacing.'''

   def __init__(self, music = None, indication = None):
      '''Init ``TempoProportional`` as type of ``Tempo`` spanner.'''
      Tempo.__init__(self, music, indication)
      self._format = _TempoProportionalFormatInterface(self)
