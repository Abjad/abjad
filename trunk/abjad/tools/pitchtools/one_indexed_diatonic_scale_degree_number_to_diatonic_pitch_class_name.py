def one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(diatonic_scale_degree):
   '''.. versionadded:: 1.1.1

   Convert one-indexed `diatonic_scale_degree` number to diatonic pitch-class name::

      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(1)
      'c'

   Raise type error on noninteger input.

   Raise value error on input not of one-indexed diatonic scale degree format.

   Return string.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.diatonic_scale_degree_to_letter( )`` to
      ``pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name( )``.
   '''

   if not isinstance(diatonic_scale_degree, (int, long)):
      raise TypeError

   diatonic_scale_degree_class = diatonic_scale_degree % 7
   if diatonic_scale_degree_class == 0:
      diatonic_scale_degree_class = 7

   try:
      return _diatonic_scale_degree_class_to_letter[diatonic_scale_degree_class]
   except KeyError:
      raise ValueError

_diatonic_scale_degree_class_to_letter = {
   1: 'c',  2: 'd',  3: 'e',  4: 'f',  5: 'g',  6: 'a',  7: 'b' }
