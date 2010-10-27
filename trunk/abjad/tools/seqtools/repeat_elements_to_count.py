def repeat_elements_to_count(l, count):
   '''Copy each element ``l[i]`` in `l` and insert `count` new copies
   of ``l[i]`` immediately after ``l[i]`` in `l`.

   ::

      abjad> l = [1, 1, 2, 3, 5, 5, 6]
      abjad> seqtools.repeat_elements_to_count(l, 2)
      [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]

   ::

      abjad> l = [1, -1, 2, -3, 5, -5, 6]
      abjad> seqtools.repeat_elements_to_count(l, 2)
      [1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6]

   Raise :exc:`TypeError` when `l` is not a list::

      abjad> seqtools.repeat_elements_to_count('foo')
      TypeError

   .. todo:: Generalize `count` from a single integer count to a list \
      of integer counts. Read values cyclically.
   '''

   if not isinstance(l, (list)):
      raise TypeError

   result = [ ]

   for x in l:
      result.extend([x] * count)

   return result
