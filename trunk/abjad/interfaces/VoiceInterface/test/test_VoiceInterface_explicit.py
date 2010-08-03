from abjad import *


def test_VoiceInterface_explicit_01( ):
   '''Return first explicit *Abjad* ``Voice`` in parentage of client.
      Otherwise ``None``.'''

   t = Score([Staff([Voice(macros.scale(4))])])
   voice = t[0][0]

   r'''
   \new Score <<
           \new Staff {
                   \new Voice {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           }
   >>
   '''

   assert t.leaves[0].voice.explicit is voice
   assert t[0][0].voice.explicit is voice
   assert t[0].voice.explicit is None
   assert t.voice.explicit is None


def test_VoiceInterface_explicit_02( ):
   '''Return first explicit *Abjad* ``Voice`` in parentage of client.
      Otherwise ``None``.'''

   t = Note(0, (1, 4))
   
   assert t.voice.explicit is None
