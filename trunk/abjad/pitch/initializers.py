from math import floor
from accidental import Accidental

class _PitchInit(object):

    pass

class Clear(_PitchInit):

    def matchSignature(self, *args):
        return len(args) == 0

    def initialize(self, client):
        client.letter = None
        client.accidental = None
        client.octave = None


class InitializeByPitchNumber(_PitchInit):
    
    def matchSignature(self, *args):
        return len(args) == 1

    def initialize(self, client, pitchNumber):
        pitchName = client.tools.pcToPitchName[pitchNumber % 12]
        client.letter = pitchName[0]
        client.accidental = Accidental(pitchName[1:])
        client.octave = int(floor(pitchNumber / 12)) + 4

class InitializeByPitchNameAndOctave(_PitchInit):

    def matchSignature(self, *args):
        return len(args) == 2 and isinstance(args[0], str)

    def initialize(self, client, pitchName, octave):
        client.letter = pitchName[0]
        client.accidental = Accidental(pitchName[1:])
        client.octave = octave

class InitializeByPitchNumberAndLetter(_PitchInit):

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
