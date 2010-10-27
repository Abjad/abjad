def is_monotonically_decreasing_sequence(l):
   r'''.. versionadded:: 1.1.2

   True when the elements in `l` decrease monotonically. ::

      abjad> l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      True

   ::

      abjad> l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      True

   ::
   
      abjad> l = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      True

   False when the elements in `l` do not decrease monotonically. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      False

   ::

      abjad> l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      False

   True by definition when `l` is empty. ::

      abjad> l = [ ]
      abjad> seqtools.is_monotonically_decreasing_sequence(l)
      True

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_decreasing_monotonically( )`` to
      ``seqtools.is_monotonically_decreasing_sequence( )``.
   '''

   prev = None
   for cur in l:
      if prev is not None:
         if not cur <= prev:
            return False
      prev = cur

   return True
