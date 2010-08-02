from abjad import *


def test_ScoreInterface_explicit_01( ):
   '''First explicit *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Score([Staff(macros.scale(4))])
   t.name = 'foo'

   r'''
   \context Score = "foo" <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert t.leaves[0].score.explicit is t
   assert t[0].score.explicit is t
   assert t.score.explicit is t


def test_ScoreInterface_explicit_02( ):
   '''First explicit *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Staff(macros.scale(4))
   t.name = 'foo'

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t[0].score.explicit is None
   assert t.score.explicit is None
