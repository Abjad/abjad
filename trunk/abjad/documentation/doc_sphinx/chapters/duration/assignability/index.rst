Assignability
=============

Western notation admits rational values like 1/4 readily. But values
like 1/5 notate only without recourse to tuplet brackets or special
time signatures.

We can capture the instinct that quarter notes appear more frequently,
in western notation, than fifth notes, by an appeal to `assignability`.
Abjad identifies those rational values that can assign to notes,
rests, chords and skips directly as `assignable`.

Which rational values meet the conditions of assignability?

Rational values n/d are assignable when, and only when, n is of the
form k * (2 ** u - j) and d is of the form 2 ** v , with integers u, v
≥ 0 , with integer k > 0 , and with integer j ∈ {0, 1} .



.. note::

   Abjad relies on these conditions of assignability to determine which
   rational values can initialize notes, rests, chords and skips, and
   which can't.

   This explains why initializing ``Note(0, (1, 4))`` works where ``Note(0,
   (1, 5))`` doesn't.


