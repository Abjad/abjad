from abjad.tools import mathtools
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval


def diatonic_and_chromatic_interval_numbers_to_diatonic_interval(
   diatonic_interval_number, chromatic_interval_number):
   '''.. versionadded:: 1.1.2

   Return diatonic interval equal to both `chromatic_interval_number`
   and `diatonic_interval_number`. ::

      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(1, 0)
      DiatonicInterval(perfect unison)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(1, 1)
      DiatonicInterval(augmented unison)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(2, 0)
      DiatonicInterval(ascending diminished second)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(2, 1)
      DiatonicInterval(ascending minor second)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(2, 2)
      DiatonicInterval(ascending major second)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(2, 3)
      DiatonicInterval(ascending augmented second)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(5, 6)
      DiatonicInterval(ascending diminished fifth)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(5, 7)
      DiatonicInterval(ascending perfect fifth)
      abjad> pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval(5, 8)
      DiatonicInterval(ascending augmented fifth)
   '''

   #print diatonic_interval_number, chromatic_interval_number
   direction_number = mathtools.sign(chromatic_interval_number)

   if diatonic_interval_number == 1:
      if chromatic_interval_number == -1:
         quality_string = 'augmented'
      elif chromatic_interval_number == 0:
         quality_string = 'perfect'
      elif chromatic_interval_number == 1:
         quality_string = 'augmented'
      if not direction_number == 0:
         diatonic_interval_number *= direction_number
      diatonic_interval = DiatonicInterval(
         quality_string, diatonic_interval_number)
      return diatonic_interval

   if diatonic_interval_number in [7, 8]:
      diatonic_interval_class_number = diatonic_interval_number
   else:
      diatonic_interval_class_number = diatonic_interval_number % 7

   chromatic_interval_class_number = abs(chromatic_interval_number) % 12

   #print diatonic_interval_class_number, chromatic_interval_class_number

   if diatonic_interval_class_number == 2:
      if chromatic_interval_class_number == 0:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 1:
         quality_string = 'minor'
      elif chromatic_interval_class_number == 2:
         quality_string = 'major'
      elif chromatic_interval_class_number == 3:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 3:
      if chromatic_interval_class_number == 2:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 3:
         quality_string = 'minor'
      elif chromatic_interval_class_number == 4:
         quality_string = 'major'
      elif chromatic_interval_class_number == 5:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 4:
      if chromatic_interval_class_number == 4:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 5:
         quality_string = 'perfect'
      elif chromatic_interval_class_number == 6:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 5:
      if chromatic_interval_class_number == 6:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 7:
         quality_string = 'perfect'
      elif chromatic_interval_class_number == 8:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 6:
      if chromatic_interval_class_number == 7:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 8:
         quality_string = 'minor'
      elif chromatic_interval_class_number == 9:
         quality_string = 'major'
      elif chromatic_interval_class_number == 10:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 7:
      if chromatic_interval_class_number == 9:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 10:
         quality_string = 'minor'
      elif chromatic_interval_class_number == 11:
         quality_string = 'major'
      elif chromatic_interval_class_number == 0:
         quality_string = 'augmented'
   elif diatonic_interval_class_number == 8:
      if chromatic_interval_class_number == 11:
         quality_string = 'diminished'
      elif chromatic_interval_class_number == 0:
         quality_string = 'perfect'
      elif chromatic_interval_class_number == 1:
         quality_string = 'augmented'

   if not direction_number == 0:
      diatonic_interval_number *= direction_number

   diatonic_interval = DiatonicInterval(
      quality_string, diatonic_interval_number)

   return diatonic_interval
