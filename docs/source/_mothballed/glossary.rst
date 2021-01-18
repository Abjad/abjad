:orphan:

Glossary
========

**Assignability.** Western notation makes it easy to notate notes, rests and chords with
durations like ``1/4`` and ``3/16``. But notating notes, rests and chords with durations
like ``1/3`` can only be done with recourse to tuplets or ties. Abjad formalizes the
difference between durations like ``1/4`` and ``1/5`` in the concept of assignability: a
duration ``n/d`` is assignable when and only when numerator ``n`` is of the form
``2**i-2**j`` with ``i>j`` and denominator ``d`` is of the form ``2**v``. In this
definition ``i`` must be a positive integer, and ``j`` and ``v`` must be nonnegative
integers. Assignability is important because it explains why you can set the duration of
any note, rest or chord to ``1/4`` or ``7/4`` but never to ``1/5`` or ``7/5``.
