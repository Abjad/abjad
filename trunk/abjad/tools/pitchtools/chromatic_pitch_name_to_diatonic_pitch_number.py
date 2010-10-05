def chromatic_pitch_name_to_diatonic_pitch_number(chromatic_pitch_name):
   '''.. versionadded:: 1.1.2

   Convert `chromatic_pitch_name` to diatonic pitch number.
   '''
   from abjad.tools import pitchtools

   ## add regex type check ##

   #diatonic_pitch_class_name = pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name(
   #   chromatic_pitch_name)
