from abjad.markup import Markup
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

   ## PRIVATE ATTRIBUTES ##

   ## TODO: Externalize in tonalharmony module. ##
   @property
   def _markup_inversion(self):
      extent, inversion = self.extent, self.inversion
      if extent == 5:
         if inversion == 0:
            return ''
         elif inversion == 1:
            return '6/3'
         elif inversion == 2:
            return '6/4'
      elif extent == 7:
         if inversion == 0:
            return '7'
         elif inversion == 1:
            return '6/5'
         elif inversion == 2:
            return '4/3'
         elif inversion == 3:
            return '4/2'
      elif extent == 9:
         if inversion == 0:
            return ''
         elif inversion == 1:
            return 'foo'
         elif inversion == 2:
            return 'foo'
         elif inversion == 3:
            return 'foo'
         elif inversion == 4:
            return 'foo'

   @property
   def _markup_root(self):
      if self.quality_indicator._quality_string in (
         'major', 'augmented', 'dominant'):
         root = self.root.name.upper( )
      else:
         root = self.root.name.lower( )
      if len(root) == 2:
         if root[-1] == 's':
            root = root[0] + r'\sharp '
         elif root[-1] == 'f':
            root = root[0] + r'\flat '
         else:
            raise ValueError('unknown note name.')
      return root
         
   @property
   def _markup_symbol(self):
      if self.quality_indicator._quality_string == 'augmented':
         return '+'
      elif self.quality_indicator._quality_string == 'diminished':
         return 'o'
      elif self.quality_indicator._quality_string == 'half diminished':
         return '@'
      elif self.quality_indicator._quality_string == 'major' and \
         5 < self.extent:
         return 'M'
      elif self.quality_indicator._quality_string == 'minor' and \
         5 < self.extent:
         return 'm'
      else:
         return ''

   ## PUBLIC ATTRIBUTES ##

   @property
   def bass(self):
      return self._bass

   @property
   def cardinality(self):
      return len(self)

   @property
   def extent(self):
      from abjad.tools.tonalharmony.chord_class_cardinality_to_extent import \
         chord_class_cardinality_to_extent
      return chord_class_cardinality_to_extent(self.cardinality)

   @property
   def inversion(self):
      return self._quality_indicator.inversion

   @property
   def markup(self):
      markup = [self._markup_root, self._markup_symbol, self._markup_inversion]
      markup = ''.join(markup)
      return Markup(markup)

   @property
   def quality_indicator(self):
      return self._quality_indicator

   @property
   def root(self):
      return self._root

   ## PUBLIC METHODS ##

   def transpose(self, mdi):
      raise Exception(NotImplemented)
