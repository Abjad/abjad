from abjad.core._LilyPondObjectProxy import _LilyPondObjectProxy


class LilyPondGrobProxy(_LilyPondObjectProxy):
   '''.. versionadded:: 1.1.2

   LilyPond grob proxy.
   '''

   def __copy__(self):
      return eval(repr(self))
