import math


def pitch_number_to_octave(pitchNumber):
   return int(math.floor(pitchNumber / 12)) + 4
