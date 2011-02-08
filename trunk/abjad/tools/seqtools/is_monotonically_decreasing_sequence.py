def is_monotonically_decreasing_sequence(expr):
   r'''.. versionadded:: 1.1.2

   True when `expr` is a sequence and the elements in `expr` decrease monotonically::

      abjad> expr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      True

   ::

      abjad> expr = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      True

   ::
   
      abjad> expr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      True

   False when `expr` is a sequence and the elements in `expr` do not decrease monotonically::

      abjad> expr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      False

   ::

      abjad> expr = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      False

   True when `expr` is a sequence and `expr` is empty::

      abjad> expr = [ ]
      abjad> seqtools.is_monotonically_decreasing_sequence(expr)
      True

   False when `expr` is not a sequence::

      abjad> seqtools.is_monotonically_decreasing_sequence(17)
      False
      
   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_decreasing_monotonically( )`` to
      ``seqtools.is_monotonically_decreasing_sequence( )``.
   '''

   try:
      prev = None
      for cur in expr:
         if prev is not None:
            if not cur <= prev:
               return False
         prev = cur
      return True

   except TypeError:
      return False
