from abjad import *
import py.test
py.test.skip('DEPRECATED. Use TempoMark instead.')


def test_TempoSpanner_01( ):
   '''Tempo spanner works on notes in voice.'''

   t = Voice(macros.scale(4))
   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   p = spannertools.TempoSpanner(t[:], tempo_indication)

   r'''
   \new Voice {
           \tempo 8=38
           c'8
           d'8
           e'8
           f'8
           %% tempo 8=38 ends here
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t%% tempo 8=38 ends here\n}"

   assert t[0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[2].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[3].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)


def test_TempoSpanner_02( ):
   '''Tempo spanner and forced attributes play well together.
      Tempo forced on a single spanned leaf applies only to that leaf.'''

   t = Voice(macros.scale(4))
   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   p = spannertools.TempoSpanner(t[:], tempo_indication)
   t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 8), 44)

   r'''
   \new Voice {
           \tempo 8=38
           c'8
           d'8
           \tempo 8=44
           e'8
           \tempo 8=38
           f'8
           %% tempo 8=38 ends here
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\t\\tempo 8=44\n\te'8\n\t\\tempo 8=38\n\tf'8\n\t%% tempo 8=38 ends here\n}"

   assert t[0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[2].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 44)
   assert t[3].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)


def test_TempoSpanner_03( ):
   '''Tempo spanner works with containers.'''

   t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
   p = spannertools.TempoSpanner(t[:], tempotools.TempoIndication(Rational(1, 8), 38))

   r'''
   \new Voice {
           {
                   \time 2/8
                   \tempo 8=38
                   c'8
                   c'8
           }
           {
                   \time 2/8
                   c'8
                   c'8
                   %% tempo 8=38 ends here
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\t\\tempo 8=38\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\tc'8\n\t\t%% tempo 8=38 ends here\n\t}\n}"

   assert t[0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[0][0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[0][1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1][0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1][1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
