def is_restricted_growth_function(l):
   '''.. versionadded:: 1.2.2

   True when `l` meets the criteria for a restricted
   growth function:

   * ``l[0] == 1``
   * ``l[i] <= max(l[:i]) + 1`` for ``1 <= i <= len(l)``

   ::

      abjad> seqtools.is_restricted_growth_array([1, 1, 1, 1])
      True
      abjad> seqtools.is_restricted_growth_array([1, 1, 1, 2])
      True
      abjad> seqtools.is_restricted_growth_array([1, 1, 2, 1])
      True
      abjad> seqtools.is_restricted_growth_array([1, 1, 2, 2])
      True

   Otherwise false. ::

      abjad> seqtools.is_restricted_growth_array([1, 1, 1, 3])
      False
   '''

   for i, n in enumerate(l):
      if i == 0:
         if not n == 1:
            return False
      else:
         if not n <= max(l[:i]) + 1:
            return False

   return True
