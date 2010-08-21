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
      #assert note.dynamics.mark is None
      assert note.dynamic_mark is None
      #assert note.dynamics.effective is None
      assert not spannertools.is_component_with_spanner_attached(
         note, spannertools.HairpinSpanner)


def test_DynamicTextInterface_02( ):
   '''Marks grant an effective dynamic to notes following after.'''

   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   #staff[0].dynamics.mark = 'p'
   staff[0].dynamic_mark = 'p'
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamic_mark == 'p'
         #assert not note.dynamics.spanned
         assert not spannertools.is_component_with_spanner_attached(
            note, spannertools.HairpinSpanner)
         #assert note.dynamics.effective is 'p'
      else:
         assert note.dynamic_mark is None
         #assert not note.dynamics.spanned
         assert not spannertools.is_component_with_spanner_attached(
            note, spannertools.HairpinSpanner)
         #assert note.dynamics.effective is 'p'

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
