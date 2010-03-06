from abjad import *


def test_durtools_token_unpack_01( ):

   assert durtools.token_unpack(Rational(1, 4)) == (1, 4)
   assert durtools.token_unpack((1, 4)) == (1, 4)
   assert durtools.token_unpack([1, 4]) == (1, 4)
   assert durtools.token_unpack((2, )) == (2, 1)
   assert durtools.token_unpack([2]) == (2, 1)
   assert durtools.token_unpack(2) == (2, 1)
   assert durtools.token_unpack('8.') == (3, 16)
