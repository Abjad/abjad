from abjad import *


def test_DynamicTextInterface_01( ):
   '''Dynamics default to no mark, no hairpin and no effective dynamic.'''

   staff = Staff([Note(n, (1, 8)) for n in range(8)])

   r'''
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   for note in staff:
      assert note.dynamics.mark is None
      assert note.dynamics.effective is None
      assert not note.dynamics.spanned


def test_DynamicTextInterface_02( ):
   '''Marks grant an effective dynamic to notes following after.'''

   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].dynamics.mark = 'p'
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamics.mark == 'p'
         assert not note.dynamics.spanned
         assert note.dynamics.effective is 'p'
      else:
         assert note.dynamics.mark is None
         assert not note.dynamics.spanned
         assert note.dynamics.effective is 'p'

   r'''
   \new Staff {
           c'8 \pX
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_DynamicTextInterface_03( ):
   '''Dynamics interface maps to DynamicText.'''

   t = Note(0, (1, 4))
   t.override.dynamic_text.self_alignment_X = -0.5
   assert t.format == "\\once \\override DynamicText #'self-alignment-X = #-0.5\nc'4"

   r'''
   \once \override DynamicText #'self-alignment-X = #-0.5
   c'4
   '''


def test_DynamicTextInterface_04( ):
   '''Dynamics interface implements first, last, only.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   CrescendoSpanner(t.leaves)
   assert t[0].dynamics.first
   assert t[-1].dynamics.last
   assert not t[0].dynamics.only

   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8 \!
   }
   '''
