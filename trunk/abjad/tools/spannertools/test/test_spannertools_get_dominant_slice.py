from abjad import *


def test_spannertools_get_dominant_slice_01( ):
   '''Get dominant spanners over zero-length 'crack'.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''
   \new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }
   '''

   receipt = spannertools.get_dominant_slice(t, 2, 2)

   assert len(receipt) == 1
   assert (glissando, 2) in receipt


def test_spannertools_get_dominant_slice_02( ):
   '''Get dominant spanners over one-component slice.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''
   \new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }
   '''

   receipt = spannertools.get_dominant_slice(t, 1, 2)

   assert len(receipt) == 2
   assert (beam, 1) in receipt
   assert (glissando, 1) in receipt


def test_spannertools_get_dominant_slice_03( ):
   '''Get dominant spanners over four-component slice.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''
   \new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }
   '''

   receipt = spannertools.get_dominant_slice(t, 0, 4)

   assert len(receipt) == 1
   assert (glissando, 0) in receipt
