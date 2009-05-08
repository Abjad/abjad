import math


def pitch_number_adjustment_to_octave(pitchNumber, adjustment):
   return int(math.floor((pitchNumber - adjustment) / 12)) + 4
