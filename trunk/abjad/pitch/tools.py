from abjad.accidental.accidental import Accidental
from abjad.core.abjadcore import _Abjad
from math import floor


class _PitchTools(_Abjad):

   def __init__(self, _client):
      self._client = _client

   ## UTILITIES ##

   pcToPitchName = {
      0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'dqf',
      2:  'd',     2.5: 'dqs',    3: 'ef',    3.5:  'eqf',
      4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
      6:  'fs',    6.5: 'gqf',    7: 'g',     7.5:  'gqs',
      8:  'af',    8.5: 'aqf',    9: 'a',     9.5:  'aqs',
      10: 'bf',   10.5: 'bqf',   11: 'b',    11.5:  'bqs' }

   pcToPitchNameFlats = {
      0:  'c',     0.5: 'dtqf',    1: 'df',    1.5:  'dqf',
      2:  'd',     2.5: 'etqf',    3: 'ef',    3.5:  'eqf',
      4:  'e',     4.5: 'fqf',     5: 'f',     5.5:  'gtqf',
      6:  'gf',    6.5: 'gqf',     7: 'g',     7.5:  'atqf',
      8:  'af',    8.5: 'aqf',     9: 'a',     9.5:  'btqf',
      10: 'bf',   10.5: 'bqf',    11: 'b',    11.5:  'cqf' }

   pcToPitchNameSharps = {
      0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'ctqs',
      2:  'd',     2.5: 'dqs',    3: 'ds',    3.5:  'dtqs',
      4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
      6:  'fs',    6.5: 'ftqs',   7: 'g',     7.5:  'gqs',
      8:  'gs',    8.5: 'gtqs',   9: 'a',     9.5:  'aqs',
      10: 'as',   10.5: 'atqs',  11: 'b',    11.5:  'bqs' }

   letterToPC = {
      'c': 0,  'd': 2,  'e': 4,  'f': 5,  'g': 7,  'a': 9,  'b': 11 }

   letterToDiatonicScaleDegree = {
      'c': 1,  'd': 2,  'e': 3,  'f': 4,  'g': 5,  'a': 6,  'b': 7 }

   diatonicScaleDegreeToLetter = {
      1: 'c',  2: 'd',  3: 'e',  4: 'f',  5: 'g',  6: 'a',  7: 'b' }

   diatonicIntervalToStaffSpaces = {
      'unison': 0,   'second': 1,   'third': 2,
      'fourth': 3,   'fifth': 4,    'sixth': 5,
      'seventh': 6,  'octave': 7,   'ninth': 8,
      'tenth': 9,    'eleventh': 10, 'twelth': 11,
      'thirteenth': 12 }

   diatonicIntervalToAbsoluteInterval = {
      'perfect unison': 0, 'minor second': 1, 'major second': 2,
      'minor third': 3, 'major third': 4, 'perfect fourth': 5,
      'augmented fourth': 6, 'diminished fifth': 6, 'perfect fifth': 7,
      'minor sixth': 8, 'major sixth': 9, 'minor seventh': 10,
      'major seventh': 11, 'perfect octave': 12 }
   
   def letterPitchNumberToNearestAccidentalString(self, letter, pitchNumber):
      givenPC = self.letterToPC[letter]
      adjustment = pitchNumber - givenPC
      if adjustment % 12 > 6:
         adjustment %= -12
      else:
         adjustment %= 12
      return Accidental.adjustmentToAccidentalString[adjustment]

   def nearestNeighbor(self, pitchNumber, pc):
      targetPC = pitchNumber % 12
      down = (targetPC - pc) % 12
      up = (pc - targetPC) % 12
      if up < down:
         return pitchNumber + up
      else:
         return pitchNumber - down

   def pitchNumberToOctave(self, pitchNumber):
      return int(floor(pitchNumber / 12)) + 4

   def pitchNumberAdjustmentToOctave(self, pitchNumber, adjustment):
      return int(floor((pitchNumber - adjustment) / 12)) + 4

   def letterPitchNumberToOctave(self, letter, pitchNumber):
      # pitch number 12 notated as letter 'b' with accidentals
      accidentalString = self.letterPitchNumberToNearestAccidentalString(
         letter, pitchNumber)
      adjustment = Accidental.accidentalStringToAdjustment[accidentalString]
      adjustedPitchNumber = pitchNumber - adjustment
      return self.pitchNumberToOctave(adjustedPitchNumber)

   def addStaffSpaces(self, staffSpaces):
      scaleDegree = (self._client.degree + staffSpaces) % 7
      if scaleDegree == 0:
         scaleDegree = 7
      return scaleDegree

   def nameToLetterAccidental(self, name):
      if len(name) == 1:
         return name, ''
      else:
         return name[0], name[1:]
