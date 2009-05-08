def add_staff_spaces(pitch, staffSpaces):
      scaleDegree = (pitch.degree + staffSpaces) % 7
      if scaleDegree == 0:
         scaleDegree = 7
      return scaleDegree
