from abjad.accidental.accidental import Accidental
from abjad.cfg.cfg import accidental_spelling
from abjad.core.abjadcore import _Abjad
import math



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
      from abjad.tools.pitchtools.pc_to_pitch_name import \
         pc_to_pitch_name
      from abjad.tools.pitchtools.pc_to_pitch_name_flats import \
         pc_to_pitch_name_flats
      from abjad.tools.pitchtools.pc_to_pitch_name_sharps import \
         pc_to_pitch_name_sharps
      pc = pitchNumber % 12
      if client.accidental_spelling == 'mixed':
         pitchName = pc_to_pitch_name(pc)
      elif client.accidental_spelling == 'sharps':
         pitchName = pc_to_pitch_name_sharps(pc)
      elif client.accidental_spelling == 'flats':
         pitchName = pc_to_pitch_name_flats(pc)
      else:
         raise ValueError('unknown accidental spelling.')
      client.letter = pitchName[0]
      client.accidental = Accidental(pitchName[1:])
      client.octave = int(math.floor(pitchNumber / 12)) + 4


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
      from abjad.tools import pitchtools
      return len(args) == 1 and pitchtools.is_pair(args[0])

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
      from abjad.tools.pitchtools.letter_to_pc import letter_to_pc
      from abjad.tools.pitchtools.nearest_neighbor import nearest_neighbor
      from abjad.tools.pitchtools.pitch_number_adjustment_to_octave import \
         pitch_number_adjustment_to_octave
      pc = letter_to_pc(letter)
      nearestNeighbor = nearest_neighbor(pitchNumber, pc)
      adjustment = pitchNumber - nearestNeighbor
      accidentalString = Accidental.adjustmentToAccidentalString[adjustment]
      pitchName = letter + accidentalString
      octave = pitch_number_adjustment_to_octave(
         pitchNumber, adjustment)
      client.letter = letter
      client.accidental = Accidental(pitchName[1:])
      client.octave = octave
