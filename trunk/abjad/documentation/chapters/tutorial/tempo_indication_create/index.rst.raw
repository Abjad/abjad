Creating tempo indications
==========================

LilyPond tempo indications look like this. ::

   \tempo 8.=72

You can create LilyPond-style tempo indications with the 
``TempoIndication`` class in the Abjad ``tempotools`` package. ::

   abjad> tempo_indication = tempotools.TempoIndication(Rational(3, 16), 72)
   abjad> tempo_indication
   TempoIndication(8., 72)

Abjad tempo indications format like LilyPond tempo indications. ::

   abjad> print tempo_indication.format
   \tempo 8.=72
