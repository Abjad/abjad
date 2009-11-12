Changing tempo indications
==========================

Create a tempo indicatication like this. ::

   abjad> tempo_indication = tempotools.TempoIndication(Rational(3, 16), 72)
   abjad> print tempo_indication.format
   \tempo 8.=72

Once you create a tempo indication, you can change its duration. ::

   abjad> tempo_indication.duration = Rational(1, 4)
   abjad> print tempo_indication.format
   \tempo 4=72

You can change its units per minute, too. ::

   abjad> tempo_indication.per_minute = 84
   abjad> print tempo_indication.format
   \tempo 4=84
