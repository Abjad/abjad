from abjad.tools.durtools.Duration import Duration


class Offset(Duration):
   '''.. versionadded:: 1.1.2

   Abjad model of offset value of musical time::

      abjad> from abjad.tools import durtools

   ::

      abjad> durtools.Offset(121, 16)
      Offset(121, 16)

   Offset inherits from duration (which inherits from built-in ``Fraction``).
   '''

   pass
