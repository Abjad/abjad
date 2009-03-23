from abjad import *
from abjad.helpers.get_dominant_spanners_slice import \
   _get_dominant_spanners_slice


def test_get_dominant_spanners_slice_01( ):
   '''Get dominant spanners over zero-length 'crack'.'''

   t = Voice(scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''\new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }'''

   receipt = _get_dominant_spanners_slice(t, 2, 2)

   assert len(receipt) == 1
   assert (glissando, 2) in receipt


def test_get_dominant_spanners_slice_02( ):
   '''Get dominant spanners over one-component slice.'''

   t = Voice(scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''\new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }'''

   receipt = _get_dominant_spanners_slice(t, 1, 2)

   assert len(receipt) == 2
   assert (beam, 1) in receipt
   assert (glissando, 1) in receipt


def test_get_dominant_spanners_slice_03( ):
   '''Get dominant spanners over four-component slice.'''

   t = Voice(scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[:])

   r'''\new Voice {
           c'8 [ \glissando
           d'8 ] \glissando
           e'8 \glissando
           f'8
   }'''

   receipt = _get_dominant_spanners_slice(t, 0, 4)

   assert len(receipt) == 1
   assert (glissando, 0) in receipt
