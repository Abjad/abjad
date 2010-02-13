from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.NamedPitchClassSegment import NamedPitchClassSegment
from abjad.tools.tonalharmony.ChordQualityIndicator import \
   ChordQualityIndicator


class ChordClass(NamedPitchClassSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of tonal chords like G 7, G 6/5, G half-diminished 6/5, etc.

   Note that notions like G 7 represent an entire *class of* chords because
   there are many different spacings and registrations of a G 7 chord.
   '''

   def __init__(self, root, *args):
      root = NamedPitchClass(root)
      self._root = root
      quality_indicator = ChordQualityIndicator(*args)
      self._quality_indicator = quality_indicator
      npcs = [ ]
      for hdi in quality_indicator:
         mdi = MelodicDiatonicInterval(hdi.quality_string, hdi.number)
         npc = root + mdi
         npcs.append(npc)
      self.extend(npcs)

   ## PUBLIC ATTRIBUTES ##

   @property
   def quality_indicator(self):
      return self._quality_indicator

   @property
   def root(self):
      return self._root
