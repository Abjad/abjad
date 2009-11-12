Setting tempo scorewide
=======================

You set tempo for an entire score by forcing a tempo indication
on the top-level score component.

::

	abjad> staff = RhythmicStaff(construct.run(8))
	abjad> score = Score([staff])
	abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 8), 72)
	abjad> score.tempo.forced = tempo_indication
	abjad> show(score)

.. image:: images/1.png

Once you do this all components in the score will know their
effective tempo. ::

   abjad> score.tempo.effective
   TempoIndication(8, 72)
   abjad> staff.tempo.effective
   TempoIndication(8, 72)
   abjad> staff.leaves[0].tempo.effective
   TempoIndication(8, 72)
