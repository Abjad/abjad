from abjad import *


def test_score_interface_effective_01( ):
   '''Effective *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Score([Staff(construct.scale(4))])
   t.name = 'foo'

   r'''\context Score = "foo" <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>'''

   assert t.leaves[0].score.effective is t
   assert t[0].score.effective is t
   assert t.score.effective is t


def test_score_interface_effective_02( ):
   '''Effective *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Staff(construct.scale(4))
   t.name = 'foo'

   r'''\new Staff {
           c'8
           d'8
           e'8
           f'8
   }'''

   assert t[0].score.effective is None
   assert t.score.effective is None
