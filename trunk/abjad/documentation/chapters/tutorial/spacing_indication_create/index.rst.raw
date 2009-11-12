Creating spacing indications
============================

Use the Abjad ``SpacingIndication`` class to establish a relationship
between tempo and the horizontal spacing of music in your score.

First create a tempo indication. This tempo indication specifies
72 dotted eighth-notes per minute. ::

   abjad> tempo_indication = tempotools.TempoIndication(Rational(3, 16), 72)

Then create a spacing indication. This spacing indication sets up
a relationship between our tempo indication of 72 dotted eighth-notes
per minute and the rational number 1/68. ::

   abjad> spacing_indication = spacing.SpacingIndication(tempo_indication, Rational(1, 68))
   
That's all there is to it. These two steps are what it takes to create
a spacing indication. To understand what a spacing indication actually
does, read a little further.

The Abjad spacing indication gives you a way to set up spacing for a
score that contains many different tempi. Imagine, for example, that 
you build a score that opens at eighth = 72 and then increases in tempo to 
eighth = 84. That is, you build a score that estabilshes 
two different tempo regions, with the first somewhat slower than the second.
Now imagine that you would like the horizontal spacing of the music
in your score to reflect the two spacing regions in your score in a special
way. This is the point of the Abjad spacing indication explained here.
The Abjad spacing indication that, for example, we created above
basically says something like the following:

"In the sections of my score where
the tempo equals eighth = 72, or equivalent, please set LilyPond
proportional notation duration to 1/68th of a whole note in order to
horizontally space the music in these sections of my score in an exact way. 
In the sections of my score where the tempo is *faster* than eighth = 72,
dynamically set LilyPond proportional notation duration to a value that is
proportionally *smaller* than 1/68th of a whole note in order to
horizontally space the music in these sections *tighter* than before.
On the other hand, in the sections of my score where the tempo is *slower*
than eighth = 72, dynamically set LilyPond proportional notation duration
to a value that is proportionally *greater* than 1/68th of a whole note
in order to horizontally space the music in these sections *looser*
than before."

That is, the Abjad spacing indication *set up a global relationship*
that you want to hold throughout an entire score. 
Abjad will then dynamically vary the spacing of different sections of
your score as you add different tempi to your score by hand.

The examples in the next few sections of the tutorial show 
these ideas in action.
