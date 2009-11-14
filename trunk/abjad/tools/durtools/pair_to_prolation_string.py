def pair_to_prolation_string(pair):
   '''.. versionadded:: 1.1.2

   Format positive integer `pair` as a colon-separated
   prolation string. ::

      abjad> durtools.pair_to_prolation_string((1, 1))
      '1:1'
      abjad> durtools.pair_to_prolation_string((1, 2))
      '2:1'
      abjad> durtools.pair_to_prolation_string((2, 2))
      '2:2'
      abjad> durtools.pair_to_prolation_string((1, 3))
      '3:1'
      abjad> durtools.pair_to_prolation_string((2, 3))
      '3:2'
      abjad> durtools.pair_to_prolation_string((3, 3))
      '3:3'
      abjad> durtools.pair_to_prolation_string((1, 4))
      '4:1'
      abjad> durtools.pair_to_prolation_string((2, 4))
      '4:2'
      abjad> durtools.pair_to_prolation_string((3, 4))
      '4:3'
      abjad> durtools.pair_to_prolation_string((4, 4))
      '4:4'
   '''

   numerator, denominator = pair
   if not 0 < numerator:
      raise ValueError('numerator must be positive.')
   if not 0 < denominator:
      raise ValueError('denominator must be positive.')

   prolation_string = '%s:%s' % (denominator, numerator)

   return prolation_string
