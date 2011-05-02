from abjad.tools import contexttools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class Bassoon(_DoubleReedInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the bassoon.
   '''

   def __init__(self):
      self.primary_clefs = [contexttools.ClefMark('bass')]
      self.all_clef = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
