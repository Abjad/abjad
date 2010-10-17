Assignability
=============

Western notation readily admits rational values like ``1/4``. 
But values like ``1/5`` notate only with tuplet brackets or special time signatures.
Abjad formalizes the difference between rationals like ``1/4`` and ``1/5`` in the
definition of rational assignability.

Rational values ``n/d`` are assignable when and only when ``n`` is of the
form ``k(2**u-j)`` and ``d`` is of the form ``2**v`` , with integers ``u,v≥0``, 
with integer ``k>0``, and with integer ``j∈{0,1}``.

Abjad initializes notes, rests and chords with assignable durations only.
