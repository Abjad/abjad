from abjad import *
import py.test


def test_get_dominant_spanners_01( ):
   '''Return Python list of (spanner, index) pairs.
      Each (spanner, index) pair gives a spanner which dominates
      all components in list, together with the start-index
      at which spanner attaches to subelement of first
      component in list.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   r'''\new Voice {
      {
         c'8 [ \startTrillSpan
         d'8
      }
      {
         e'8 \glissando
         f'8 ] \glissando
      }
      {
         g'8 \glissando
         a'8 \stopTrillSpan
      }
   }'''

   receipt = get_dominant_spanners(t[:1])

   "Beam and trill dominate first sequential."

   assert len(receipt) == 2
   assert (beam, 0) in receipt
   assert (trill, 0) in receipt


def test_get_dominant_spanners_02( ):
   '''Beam, glissando and trill all dominante second sequential.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t[1:2])

   assert len(receipt) == 3
   assert (beam, 1) in receipt
   assert (glissando, 0) in receipt
   assert (trill, 2) in receipt


def test_get_dominant_spanners_03( ):
   '''Glissando and trill dominate last sequential.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t[-1:])

   assert len(receipt) == 2
   assert (glissando, 1) in receipt
   assert (trill, 4) in receipt


def test_get_dominant_spanners_04( ):
   '''Beam and trill dominate first two sequentials.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t[:2])

   assert len(receipt) == 2
   assert (beam, 0) in receipt
   assert (trill, 0) in receipt


def test_get_dominant_spanners_05( ):
   '''Glissando and trill dominate last two sequentials.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t[-2:])

   assert len(receipt) == 2
   assert (glissando, 0) in receipt
   assert (trill, 2) in receipt


def test_get_dominant_spanners_06( ):
   '''Only trill dominates all three sequentials.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t[:])

   assert len(receipt) == 1
   assert (trill, 0) in receipt


def test_get_dominant_spanners_07( ):
   '''Only trill dominates voice.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners([t])

   assert len(receipt) == 1
   assert (trill, 0) in receipt


def test_get_dominant_spanners_08( ):
   '''Only trill dominates first two notes.
      Note that trill attaches to notes.
      Note that beam and glissando attach to sequentials.'''

   t = Voice(Container(run(2)) * 3)
   pitches.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = get_dominant_spanners(t.leaves[:2])

   assert len(receipt) == 1
   assert (trill, 0) in receipt


def test_get_dominant_spanners_09( ):
   '''Lone components raise ContiguityError.'''

   notes = scale(4)
   b1 = Beam(notes[:2])
   b2 = Beam(notes[2:])
   crescendo = Crescendo(notes)

   assert py.test.raises(ContiguityError, 'get_dominant_spanners(notes[1:3])')
