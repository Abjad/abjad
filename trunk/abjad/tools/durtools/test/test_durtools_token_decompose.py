from abjad import *


def test_durtools_token_decompose_01( ):
   '''Return big-endian list of notehead-assignable duration tokens.'''

   assert durtools.token_decompose((10, 16)) == ((8, 16), (2, 16))
   assert durtools.token_decompose((11, 16)) == ((8, 16), (3, 16))
   assert durtools.token_decompose((12, 16)) == ((12, 16), )
   assert durtools.token_decompose((13, 16)) == ((12, 16), (1, 16))
   assert durtools.token_decompose((14, 16)) == ((14, 16), )
   assert durtools.token_decompose((15, 16)) == ((15, 16), )
   assert durtools.token_decompose((16, 16)) == ((16, 16), )
   assert durtools.token_decompose((17, 16)) == ((16, 16), (1, 16))
   assert durtools.token_decompose((18, 16)) == ((16, 16), (2, 16))
   assert durtools.token_decompose((19, 16)) == ((16, 16), (3, 16))
