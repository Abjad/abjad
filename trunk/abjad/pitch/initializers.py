#from abjad.accidentals.accidental import _Accidental
#from abjad.accidentals.accidental import Accidental
from abjad.accidental.accidental import Accidental
from abjad.core.abjadcore import _Abjad
from abjad.helpers.is_pitch_pair import _is_pitch_pair
from math import floor


class _PitchInit(_Abjad):

   pass


class _Clear(_PitchInit):

   def matchSignature(self, *args):
      return len(args) == 0

   def initialize(self, client):
      client.letter = None
      client.accidental = None
      client.octave = None


class _InitializeByPitchNumber(_PitchInit):
    
   def matchSignature(self, *args):
      if len(args) == 1 and isinstance(args[0], (int, long, float)):
         return True
      else:
         return False

   def initialize(self, client, pitchNumber):
      pitchName = client.tools.pcToPitchName[pitchNumber % 12]
      client.letter = pitchName[0]
      #client.accidental = _Accidental(pitchName[1:])
      client.accidental = Accidental(pitchName[1:])
      client.octave = int(floor(pitchNumber / 12)) + 4


class _InitializeByPitchReference(_PitchInit):
    
   def matchSignature(self, *args):
      if len(args) == 1 and args[0].__class__.__name__ == 'Pitch':
         return True
      else:
         return False

   def initialize(self, client, pitchReference):
      client.letter = pitchReference.letter
      #client.accidental = _Accidental(pitchReference.accidental._string)
      client.accidental = Accidental(pitchReference.accidental._string)
      client.octave = pitchReference.octave


class _InitializeByPitchPair(_PitchInit):
    
   def matchSignature(self, *args):
      return len(args) == 1 and _is_pitch_pair(args[0])

   def initialize(self, client, pitchPair):
      name, octave = pitchPair
      client.letter = name[0]
      #client.accidental = _Accidental(name[1:])
      client.accidental = Accidental(name[1:])
      client.octave = octave


class _InitializeByPitchNameAndOctave(_PitchInit):

   def matchSignature(self, *args):
      return len(args) == 2 and isinstance(args[0], str)

   def initialize(self, client, pitchName, octave):
      client.letter = pitchName[0]
      #client.accidental = _Accidental(pitchName[1:])
      client.accidental = Accidental(pitchName[1:])
      client.octave = octave


class _InitializeByPitchNumberAndLetter(_PitchInit):

   def matchSignature(self, *args):
      return len(args) == 2  and isinstance(args[0], (int, long, float))

   def initialize(self, client, pitchNumber, letter):
      pc = client.tools.letterToPC[letter]
      nearestNeighbor = client.tools.nearestNeighbor(pitchNumber, pc)
      adjustment = pitchNumber - nearestNeighbor
      #accidentalString = _Accidental.adjustmentToAccidentalString[adjustment]
      accidentalString = Accidental.adjustmentToAccidentalString[adjustment]
      pitchName = letter + accidentalString
      octave = client.tools.pitchNumberAdjustmentToOctave ( 
         pitchNumber, adjustment)
      client.letter = letter
      #client.accidental = _Accidental(pitchName[1:])
      client.accidental = Accidental(pitchName[1:])
      client.octave = octave
