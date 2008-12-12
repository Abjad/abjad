from abjad.core.abjadcore import _Abjad
from abjad.accidentals.accidental import _Accidental
from abjad.pitch.initializer import _PitchInitializer
from abjad.pitch.tools import _PitchTools
from math import floor


class Pitch(_Abjad):

   def __init__(self, *args):
      self.tools = _PitchTools(self)
      self.initializer = _PitchInitializer( )
      self.initializer.initialize(self, *args)

   ### OVERLOADS ###

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

   ### PRIVATE METHODS ###

   def _isSet(self):
      return bool(self.letter and self.accidental and not self.octave is None)

   ### PUBLIC ATTRIBUTES ###

   @apply
   def accidental( ):
      def fget(self):
         return self._accidental
      def fset(self, expr):
         if expr is None:
            self._accidental = _Accidental('')
         elif isinstance(expr, str):
            self._accidental = _Accidental(expr)
         elif isinstance(expr, _Accidental):
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
      if self.letter:
         return self.tools.letterToDiatonicScaleDegree[self.letter]
      else:
         return None

   @property
   def lily(self):
      return str(self)

   @property
   def name(self):
      if self.letter and self.accidental:
         return '%s%s' % (self.letter, self.accidental)
      else:
         return None

   @property
   def number(self):
      if self._isSet( ):
         return self.tools.letterToPC[self.letter] + \
            self.accidental.adjustment + (self.octave - 4) * 12
      else:
         return None

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

   ### PUBLIC METHODS ###

   def diatonicTranspose(self, diatonicInterval):
      quality, interval = diatonicInterval.split()
      staffSpaces = self.tools.diatonicIntervalToStaffSpaces[interval]
      degree = self.tools.addStaffSpaces(staffSpaces)
      letter = self.tools.diatonicScaleDegreeToLetter[degree]
      pitchNumber = self.number + \
         self.tools.diatonicIntervalToAbsoluteInterval[diatonicInterval]
      accidentalString = self.tools.letterPitchNumberToNearestAccidentalString(
         letter, pitchNumber)
      pitchName = letter + accidentalString
      octave = self.tools.letterPitchNumberToOctave(letter, pitchNumber)
      return Pitch(pitchName, octave) 

   ### DEPRECATED: use p1.altitude == p2.altitude instead
#   def enharmonicCompare(self, arg):
#      result = cmp(self.number, arg.number)
#      if result == 0:
#         return -cmp(
#            self.accidental.adjustment, arg.accidental.adjustment)
#      else:
#         return result

   # p.staffSpaceTranspose(-1, 0.5)
   def staffSpaceTranspose(self, staffSpaces, absoluteInterval):
      pitchNumber = self.number + absoluteInterval
      degree = self.tools.addStaffSpaces(staffSpaces)
      letter = self.tools.diatonicScaleDegreeToLetter[degree]
      return Pitch(pitchNumber, letter)
