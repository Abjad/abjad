from abjad.tools.sievetools._cycle_token_to_sieve import \
   _cycle_token_to_sieve


def cycle_tokens_to_sieve(*cycle_tokens):
   '''.. versionadded:: 1.1.2

   Make Xenakis sieve from arbitrarily many `cycle_tokens`. ::

      abjad> cycle_token_1 = (6, [0, 4, 5])
      abjad> cycle_token_2 = (10, [0, 1, 2], 6) 
      abjad> sievetools.cycle_tokens_to_sieve(cycle_token_1, cycle_token_2)
      {RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 6) | RC(10, 7) | RC(10, 8)}

   Cycle token comprises mandatory `modulo`, mandatory `residues` 
   and optional `offset`.
   '''

   sieves = [ ]
   for cycle_token in cycle_tokens:
      sieve = _cycle_token_to_sieve(cycle_token)
      sieves.append(sieve)

   cur_sieve = sieves[0]
   for sieve in sieves[1:]:
      cur_sieve = cur_sieve | sieve   

   return cur_sieve
