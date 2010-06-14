from abjad import *


def test_score_interface_explicit_01( ):
   '''First explicit *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Score([Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))])
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


def test_score_interface_explicit_02( ):
   '''First explicit *Abjad* ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage, return ``None``.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
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
