from abjad import *


def test_sievetools_cycle_token_to_sieve_01( ):
   '''Length-2 cycle token with modulo and residue list.'''

   cycle_token = (6, [0, 4, 5])
   sieve = sievetools.cycle_token_to_sieve(cycle_token)
   RC = sievetools.RC

   assert sieve.rcs == [RC(6, 0), RC(6, 4), RC(6, 5)]


def test_sievetools_cycle_token_to_sieve_02( ):
   '''Length-3 cycle token with modulo, residue list and offset.'''

   cycle_token = (6, [0, 4, 5], 1)
   sieve = sievetools.cycle_token_to_sieve(cycle_token)
   RC = sievetools.RC

   assert sieve.rcs == [RC(6, 0), RC(6, 1), RC(6, 5)]


def test_sievetools_cycle_token_to_sieve_03( ):
   '''Large offset.'''

   cycle_token = (6, [0, 4, 5], 99)
   sieve = sievetools.cycle_token_to_sieve(cycle_token)
   RC = sievetools.RC

   assert sieve.rcs == [RC(6, 1), RC(6, 2), RC(6, 3)]


def test_sievetools_cycle_token_to_sieve_04( ):
   '''Unsorted residues are sorted on initialization.'''

   cycle_token = (6, [5, 0, 4])
   sieve = sievetools.cycle_token_to_sieve(cycle_token)
   RC = sievetools.RC

   assert sieve.rcs == [RC(6, 0), RC(6, 4), RC(6, 5)]
