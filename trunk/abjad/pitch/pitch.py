from abjad.cfg.cfg import accidental_spelling
from abjad.core.abjadcore import _Abjad
from abjad.accidental.accidental import Accidental
from abjad.pitch.initializer import _PitchInitializer
#from abjad.pitch.tools import _PitchTools


class Pitch(_Abjad):

   accidental_spelling = accidental_spelling

   def __init__(self, *args):
      #self.tools = _PitchTools(self)
      self.initializer = _PitchInitializer( )
      self.initializer.initialize(self, *args)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, Pitch):
         if self.altitude == arg.altitude:
            if self.accidental.adjustment == arg.accidental.adjustment:
               return True
      return False

   def __ge__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude > arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.adjustment >= arg.accidental.adjustment)

   def __gt__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude > arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.adjustment > arg.accidental.adjustment)

   def __le__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude < arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.adjustment <= arg.accidental.adjustment)

   def __lt__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude < arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.adjustment < arg.accidental.adjustment)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      if self.name and not self.octave is None:
         return 'Pitch(%s, %s)' % (self.name, self.octave)
      else:
         return 'Pitch( )'

   def __str__(self):
      if self.name and not self.octave is None:
         return '%s%s' % (self.name, self.ticks)
      else:
         return ''

   ## PRIVATE METHODS ##

   def _isSet(self):
      return bool(self.letter and self.accidental and not self.octave is None)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def accidental( ):
      def fget(self):
         return self._accidental
      def fset(self, expr):
         if expr is None:
            self._accidental = Accidental('')
         elif isinstance(expr, str):
            self._accidental = Accidental(expr)
         elif isinstance(expr, Accidental):
            self._accidental = expr
         else:
            raise ValueError('can not set accidental.')
      return property(**locals( ))

   @property
   def altitude(self):
      if self.letter:
         return (self.octave - 4) * 7 + self.degree - 1
      else:
         return None
      
   @property
   def degree(self):
      from abjad.tools.pitchtools.letter_to_diatonic_scale_degree \
         import letter_to_diatonic_scale_degree
      if self.letter:
         #return self.tools.letterToDiatonicScaleDegree[self.letter]
         return letter_to_diatonic_scale_degree(self.letter)
      else:
         return None

   @property
   def format(self):
      return str(self)

   @apply
   def name( ):
      def fget(self):
         if self.letter and self.accidental:
            return '%s%s' % (self.letter, self.accidental)
         else:
            return None
      def fset(self, name):
         from abjad.tools.pitchtools.name_to_letter_accidental \
            import name_to_letter_accidental
         #letter, accidental = self.tools.nameToLetterAccidental(name)
         letter, accidental = name_to_letter_accidental(name)
         self.letter = letter
         self.accidental = accidental
      return property(**locals( ))

   @apply
   def number( ):
      def fget(self):
         from abjad.tools.pitchtools.letter_to_pc import letter_to_pc
         if self._isSet( ):
            #return self.tools.letterToPC[self.letter] + \
            #   self.accidental.adjustment + (self.octave - 4) * 12
            return letter_to_pc(self.letter) + \
               self.accidental.adjustment + (self.octave - 4) * 12
         else:
            return None
      def fset(self, arg):
         self.__init__(arg)
      return property(**locals( ))

   @property
   def pair(self):
      if self.name and self.octave is not None:
         return (self.name, self.octave)
      else:
         return None

   @property
   def pc(self):
      if self._isSet( ):
         return self.number % 12
      else:
         return None
      
   @property
   def ticks(self):
      if self.octave is not None:
         if self.octave <= 2:
            return ',' * (3 - self.octave)
         elif self.octave == 3:
            return ''
         else:
            return "'" * (self.octave - 3)
      else:
         return None

   ## PUBLIC METHODS ##

   ## DEPRECATED: Use pitchtools.diatonic_transpose( ) instead ##

#   def diatonicTranspose(self, diatonicInterval):
#      quality, interval = diatonicInterval.split()
#      staffSpaces = self.tools.diatonicIntervalToStaffSpaces[interval]
#      degree = self.tools.addStaffSpaces(staffSpaces)
#      letter = self.tools.diatonicScaleDegreeToLetter[degree]
#      pitchNumber = self.number + \
#         self.tools.diatonicIntervalToAbsoluteInterval[diatonicInterval]
#      accidentalString = self.tools.letterPitchNumberToNearestAccidentalString(
#         letter, pitchNumber)
#      pitchName = letter + accidentalString
#      octave = self.tools.letterPitchNumberToOctave(letter, pitchNumber)
#      return Pitch(pitchName, octave) 

   ## DEPRECATED: use p1.altitude == p2.altitude instead ##

#   def enharmonicCompare(self, arg):
#      result = cmp(self.number, arg.number)
#      if result == 0:
#         return -cmp(
#            self.accidental.adjustment, arg.accidental.adjustment)
#      else:
#         return result

   ## DEPRECATED: Use pitchtools.staff_space_transpose( ) instead. ##

#   # p.staffSpaceTranspose(-1, 0.5)
#   def staffSpaceTranspose(self, staffSpaces, absoluteInterval):
#      '''p.staffSpaceTranspose(-1, 0.5)'''
#      pitchNumber = self.number + absoluteInterval
#      degree = self.tools.addStaffSpaces(staffSpaces)
#      letter = self.tools.diatonicScaleDegreeToLetter[degree]
#      return Pitch(pitchNumber, letter)
