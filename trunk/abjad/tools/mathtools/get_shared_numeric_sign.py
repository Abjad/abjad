def get_shared_numeric_sign(l):
   '''Return ``1`` when all elements in `l` are positive::

      abjad> mathtools.get_shared_numeric_sign([1, 2, 3])
      1
   
   Return ``-1`` when all elements in `l` are negative::

      abjad> mathtools.get_shared_numeric_sign([-1, -2, -3])
      -1

   Return ``0`` when `l` is empty::

      abjad> mathtools.get_shared_numeric_sign([ ])
      0

   Otherwise, return none::

      abjad> mathtools.get_shared_numeric_sign([1, 2, -3]) is None
      True

   .. versionchanged:: 1.1.2
      renamed ``seqtools.sign( )`` to 
      ``mathtools.get_shared_numeric_sign( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_shared_numeric_sign( )`` to
      ``mathtools.get_shared_numeric_sign( )``.
   '''

   if len(l) == 0:
      return 0
   elif all([0 < x for x in l]):
      return 1
   elif all([x < 0 for x in l]):
      return -1
   else:
      return None
