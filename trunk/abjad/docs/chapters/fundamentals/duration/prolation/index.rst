Prolation
=========


Abjad uses **prolation** as a cover term for rhythmic augmentation and diminution.
Augmentation increases the duration of notes, rests and chords.
Diminution does the opposite. 
Western notation employs tuplet brackets and special types of time signature to effect prolation.


Tuplet prolation
----------------

Tuplets prolated their contents:

::

	abjad> tuplet = tuplettools.FixedDurationTuplet((5, 8), Note(0, (1, 8)) * 4)
	abjad> staff = stafftools.RhythmicStaff([Measure((5, 8), [tuplet])])
	abjad> spannertools.BeamSpanner(tuplet)
	abjad> tuplet.duration.is_augmentation
	True

.. image:: images/example1.png

::

  abjad> tuplet.duration.multiplier
  Fraction(4, 5)

::

  abjad> note = tuplet[0]
  abjad> note.duration.written
  Fraction(1, 8)

::

  abjad> note.duration.prolation
  Fraction(5, 4)

::

  abjad> note.duration.prolated
  Fraction(5, 32)

Notes here with written duration equal to ``1/8`` carry prolated duration equal to ``4/5``.


Meter prolation
---------------

Time signatures in western notation usually carry a denominator equal 
to a nonnegative integer power of ``2``. 
Abjad calls these conventional meters **binary meters**.
Denominators equal to integers other than integer powers of ``2`` are also possible. 
Such **nonbinary meters** prolate the music they contain:

::

	abjad> measure = Measure((4, 10), Note(0, (1, 8)) * 4)
	abjad> spannertools.BeamSpanner(measure)
	abjad> staff = stafftools.RhythmicStaff([measure])
	abjad> note = staff.leaves[0]
	abjad> note.duration.prolation
	Fraction(4, 5)

.. image:: images/example2.png

::

  abjad> note.duration.prolated
  Fraction(1, 10)

Notes here with written duration equal to ``1/8`` carry prolated duration ``1/10``.

Nonbinary meters rhythmically diminish the contents of the measures they govern;
nonbinary meters never rhythmically augment the contents of the measures they govern.


The prolation chain
-------------------

Tuplets nest. 
And tuplet prolation and meter prolation combine freely. 
When two or more **prolation donors** conspire, the prolation factor they 
collectively bestow on leaf-level music equals the cumulative product of all 
prolation factors in the **prolation chain**:

::

	abjad> tuplet = tuplettools.FixedDurationTuplet((4, 8), Note(0, (1, 16)) * 7)
	abjad> spannertools.BeamSpanner(tuplet)
	abjad> measure = Measure((4, 10), [tuplet])
	abjad> staff = stafftools.RhythmicStaff([measure])
	abjad> tuplet.duration.multiplier
	Fraction(8, 7)

.. image:: images/example3.png

::

  abjad> measure.duration.multiplier
  Fraction(4, 5)

::

  abjad> note = measure.leaves[0]
  abjad> note.duration.prolation
  Fraction(32, 35)

::

  abjad> note.duration.prolated
  Fraction(2, 35)

Notes here with written duration equal to ``1/16`` carry prolated duration ``2/35``.

All durated components carry a prolation chain.
But only the prolation chains of nested objects are interesting.

.. note::

   Western notation does not recognize tuplet brackets carrying one-to-one ratios.  Such **trivial tuplets** may, however, be useful during different stages of composition, and Abjad allows them for that reason.  Trivial tuplets carry **zero prolation**. Zero-prolated tuplets neither augment nor diminish the music they contain.

.. note::

   Abjad implements one of two competing nonbinary **meter-interpretation schemes**.  The first, **implicit meter-interpretation** given here, follows, for example, Ferneyhough, in that nonbinary meters prolate the contents of the measures they govern implicitly, ie, without recourse to tuplet brackets.  The second, **explicit meter-interpretation**, which we find in, for example, Sciarrino, insists instead on the presence of some tuplet bracket, usually engraved in some broken or incomplete way.  The implicit meter-interpretation that Abjad implements differs from the explicit meter-interpretation native to LilyPond.  Abjad will eventually implement both implicit and explicit meter-interpretation, settable on a container-by-container basis.

.. note::

   Nonbinary meter ``n/d`` rhythmically diminishes the contents of the measure it governs 
   by a factor ``j/k``, with ``k=d``, and with ``j`` equal to the greatest integer power 
   of ``2`` less than ``d``.  That is, ``j=2**int(log2(d))``. 
