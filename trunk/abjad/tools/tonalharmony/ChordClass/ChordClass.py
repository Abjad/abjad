from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.NamedPitchClassSet import NamedPitchClassSet
from abjad.tools.tonalharmony.ChordQualityIndicator import \
   ChordQualityIndicator


class ChordClass(NamedPitchClassSet):
   '''.. versionadded:: 1.1.2

   Abjad model of tonal chords like G 7, G 6/5, G half-diminished 6/5, etc.

   Note that notions like G 7 represent an entire *class of* chords because
   there are many different spacings and registrations of a G 7 chord.
   '''

   def __new__(klass, root, *args):
      root = NamedPitchClass(root)
      quality_indicator = ChordQualityIndicator(*args)
      npcs = [ ]
      for hdi in quality_indicator:
         mdi = hdi.melodic_diatonic_interval_ascending
         npc = root + mdi
         npcs.append(npc)
      bass = npcs[0]
      self = NamedPitchClassSet.__new__(klass, npcs)
      self._root = root
      self._quality_indicator = quality_indicator
      self._bass = bass
      return self

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.root == arg.root:
            if self.quality_indicator == arg.quality_indicator:
               if self.inversion == arg.inversion:
                  return True
      return False

   def __ne__(self, arg):
      return not self == arg
         
   def __repr__(self):
      root = self.root.name.title( )
      quality = self.quality_indicator._title_case_name
      return root + quality

   ## PUBLIC ATTRIBUTES ##

   @property
   def bass(self):
      return self._bass

   @property
   def inversion(self):
      return self._quality_indicator.inversion

   @property
   def quality_indicator(self):
      return self._quality_indicator

   @property
   def root(self):
      return self._root

   ## PUBLIC METHODS ##

   def transpose(self, mdi):
      raise Exception(NotImplemented)
