from abjad.tools.pitchtools.DiatonicIntervalClass import DiatonicIntervalClass


def list_all_diatonic_interval_classes( ):
   '''.. versionadded:: 1.1.2

   List all 11 diatonic interval classes. ::

      abjad> for dic in pitchtools.list_all_diatonic_interval_classes( ):
      ...     dic
      ... 
      DiatonicIntervalClass(perfect unison)
      DiatonicIntervalClass(augmented unison)
      DiatonicIntervalClass(minor second)
      DiatonicIntervalClass(major second)
      DiatonicIntervalClass(augmented second)
      DiatonicIntervalClass(diminished third)
      DiatonicIntervalClass(minor third)
      DiatonicIntervalClass(major third)
      DiatonicIntervalClass(diminished fourth)
      DiatonicIntervalClass(perfect fourth)
      DiatonicIntervalClass(augmented fourth)

   It is an open question as to whether octaves should be included.
   '''

   return [
      DiatonicIntervalClass('perfect', 1),
      DiatonicIntervalClass('augmented', 1),

      DiatonicIntervalClass('minor', 2),
      DiatonicIntervalClass('major', 2),
      DiatonicIntervalClass('augmented', 2),

      DiatonicIntervalClass('diminished', 3),
      DiatonicIntervalClass('minor', 3),
      DiatonicIntervalClass('major', 3),

      DiatonicIntervalClass('diminished', 4),
      DiatonicIntervalClass('perfect', 4),
      DiatonicIntervalClass('augmented', 4),
      ]
