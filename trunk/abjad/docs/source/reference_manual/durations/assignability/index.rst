Assignability
=============

Western notation readily admits rational values like ``1/4``. 
But values like ``1/5`` notate only with tuplet brackets or special time signatures.
Abjad formalizes the difference between rationals like ``1/4`` and ``1/5`` in the
definition of rational assignability.

Rational values ``n/d`` are assignable when and only when numerator ``n`` is of the
form ``k(2**u-j)`` and denominator ``d`` is of the form ``2**v``. 
In this definition ``u`` and ``v`` must be nonnegative integers,
``k`` must be a positive integer, and ``j`` must be either ``0`` or ``1``.

Abjad initializes notes, rests and chords with assignable durations only.
