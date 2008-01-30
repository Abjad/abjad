from accidental import _Accidental
from initializer import _PitchInitializer
from tools import _PitchTools
from math import floor

class Pitch(object):

   def __init__(self, *args):
      self.tools = _PitchTools(self)
      self.initializer = _PitchInitializer( )
      self.initializer.initialize(self, *args)

   ### PROPERTIES ###

   @property
   def diatonicScaleDegree(self):
      if self.letter:
         return self.tools.letterToDiatonicScaleDegree[self.letter]
      else:
         return None

   @property
   def name(self):
      if self.letter and self.accidental:
         return '%s%s' % (self.letter, self.accidental)
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

   @property
   def number(self):
      if self.isSet( ):
         return self.tools.letterToPC[self.letter] + \
            self.accidental.adjustment + (self.octave - 4) * 12
      else:
         return None

   @property
   def pc(self):
      if self.isSet( ):
         return self.number % 12
      else:
         return None
      
   @property
   def pair(self):
      if self.name and self.octave is not None:
         return (self.name, self.octave)
      else:
         return None

   ### PREDICATES ###

   def isSet(self):
      return bool(self.letter and self.accidental and not self.octave is None)

   ### REPR ###

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

   ### MANAGED ATTRIBUTES ###

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
      
   ### MATH AND COMPARISON TESTING ###

   def __cmp__(self, arg):
      return cmp(self.number, arg.number)

   def enharmonicCompare(self, arg):
      result = cmp(self.number, arg.number)
      if result == 0:
         return -cmp(
            self.accidental.adjustment, arg.accidental.adjustment)
      else:
         return result

   ### TRANSPOSITION ###

   # p.staffSpaceTranspose(-1, 0.5)
   def staffSpaceTranspose(self, staffSpaces, absoluteInterval):
      pitchNumber = self.number + absoluteInterval
      diatonicScaleDegree = self.tools.addStaffSpaces(staffSpaces)
      letter = self.tools.diatonicScaleDegreeToLetter[diatonicScaleDegree]
      return Pitch(pitchNumber, letter)

   def diatonicTranspose(self, diatonicInterval):
      quality, interval = diatonicInterval.split()
      staffSpaces = self.tools.diatonicIntervalToStaffSpaces[interval]
      diatonicScaleDegree = self.tools.addStaffSpaces(staffSpaces)
      letter = self.tools.diatonicScaleDegreeToLetter[diatonicScaleDegree]
      pitchNumber = self.number + \
         self.tools.diatonicIntervalToAbsoluteInterval[diatonicInterval]
      accidentalString = self.tools.letterPitchNumberToNearestAccidentalString(
         letter, pitchNumber)
      pitchName = letter + accidentalString
      octave = self.tools.letterPitchNumberToOctave(letter, pitchNumber)
      return Pitch(pitchName, octave) 

   ### FORMATTING ###

   @property
   def lily(self):
      return str(self)
