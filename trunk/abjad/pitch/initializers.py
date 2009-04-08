from abjad.accidental.accidental import Accidental
from abjad.cfg.cfg import accidental_spelling
from abjad.core.abjadcore import _Abjad
from abjad.tools import pitch
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
      if client.accidental_spelling == 'mixed':
         pitchName = client.tools.pcToPitchName[pitchNumber % 12]
      elif client.accidental_spelling == 'sharps':
         pitchName = client.tools.pcToPitchNameSharps[pitchNumber % 12]
      elif client.accidental_spelling == 'flats':
         pitchName = client.tools.pcToPitchNameFlats[pitchNumber % 12]
      else:
         raise ValueError('unknown accidental spelling.')
      client.letter = pitchName[0]
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
      client.accidental = Accidental(pitchReference.accidental._string)
      client.octave = pitchReference.octave


class _InitializeByPitchPair(_PitchInit):
    
   def matchSignature(self, *args):
      return len(args) == 1 and pitch.is_pair(args[0])

   def initialize(self, client, pitchPair):
      name, octave = pitchPair
      client.letter = name[0]
      client.accidental = Accidental(name[1:])
      client.octave = octave


class _InitializeByPitchNameAndOctave(_PitchInit):

   def matchSignature(self, *args):
      return len(args) == 2 and isinstance(args[0], str)

   def initialize(self, client, pitchName, octave):
      client.letter = pitchName[0]
      client.accidental = Accidental(pitchName[1:])
      client.octave = octave


class _InitializeByPitchNumberAndLetter(_PitchInit):

   def matchSignature(self, *args):
      return len(args) == 2  and isinstance(args[0], (int, long, float))

   def initialize(self, client, pitchNumber, letter):
      pc = client.tools.letterToPC[letter]
      nearestNeighbor = client.tools.nearestNeighbor(pitchNumber, pc)
      adjustment = pitchNumber - nearestNeighbor
      accidentalString = Accidental.adjustmentToAccidentalString[adjustment]
      pitchName = letter + accidentalString
      octave = client.tools.pitchNumberAdjustmentToOctave ( 
         pitchNumber, adjustment)
      client.letter = letter
      client.accidental = Accidental(pitchName[1:])
      client.octave = octave
