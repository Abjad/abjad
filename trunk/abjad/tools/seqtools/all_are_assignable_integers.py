from abjad.tools import mathtools


def all_are_assignable_integers(sequence):
   '''.. versionadded:: 1.1.2

   True when all elements in `sequence` are notehead-assignable integers::

      abjad> sequence = [1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16]
      abjad> seqtools.all_are_assignable_integers(sequence)
      True

   True on empty `sequence`::
   
      abjad> sequence = [ ]
      abjad> seqtools.all_are_assignable_integers(sequence)
      True

   False otherwise::

      abjad> sequence = [1, 2, 3, 4, 5]
      abjad> seqtools.all_are_assignable_integers(sequence)
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_assignable( )`` to 
      ``seqtools.all_are_assignable_integers( )``.
   '''

   return all([mathtools.is_assignable_integer(x) for x in sequence])
