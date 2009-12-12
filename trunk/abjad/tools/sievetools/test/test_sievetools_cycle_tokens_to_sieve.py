from abjad import *


def test_sievetools_cycle_tokens_to_sieve_01( ):
   '''Arbitrarily many cycle tokens.'''

   cycle_token_1 = (6, [0, 4, 5])
   cycle_token_2 = (10, [0, 1, 2])
   sieve = sievetools.cycle_tokens_to_sieve(cycle_token_1, cycle_token_2)

   "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 0) | RC(10, 1) | RC(10, 2)}"

   RC = sievetools.RC
   assert sieve.rcs == [
      RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 0), RC(10, 1), RC(10, 2)]


def test_sievetools_cycle_tokens_to_sieve_02( ):
   '''Unsorted RCs are sorted on initialization.'''

   cycle_token_1 = (6, [0, 4, 5])
   cycle_token_2 = (10, [0, 1, 2])
   sieve = sievetools.cycle_tokens_to_sieve(cycle_token_2, cycle_token_1)

   "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 0) | RC(10, 1) | RC(10, 2)}"

   RC = sievetools.RC
   assert sieve.rcs == [
      RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 0), RC(10, 1), RC(10, 2)]


def test_sievetools_cycle_tokens_to_sieve_03( ):
   '''Cycle tokens allow optional offset values.'''

   cycle_token_1 = (6, [0, 4, 5])
   cycle_token_2 = (10, [0, 1, 2], 6)
   sieve = sievetools.cycle_tokens_to_sieve(cycle_token_2, cycle_token_1)

   "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 6) | RC(10, 7) | RC(10, 8)}"

   RC = sievetools.RC
   assert sieve.rcs == [
      RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 6), RC(10, 7), RC(10, 8)]
