from abjad.tools.sievetools.rc import RC
from abjad.tools.sievetools.rcexpression import RCexpression


def _cycle_token_to_sieve(cycle_token):
   r'''.. versionadded:: 1.1.2

   Make Xenakis sieve from `cycle_token`.

   When `cycle_token` has length 2, interpret `cycle_token` as
   ``modulo, residues`` pair. ::

      abjad> cycle_token = (6, [0, 4, 5])
      abjad> sievetools.cycle_token_to_sieve(cycle_token)
      {RC(6, 0) | RC(6, 4) | RC(6, 5)}

   When `cycle_token` has length 3, interpret `cycle_token` as
   ``modulo, residues, offset`` triple. ::

      abjad> cycle_token = (10, [0, 1, 2], 6)
      abjad> sievetools.cycle_token_to_sieve(cycle_token)
      {RC(10, 6) | RC(10, 7) | RC(10, 8)}
   '''

   ## parse cycle token
   modulo = cycle_token[0]
   residues = cycle_token[1]
   try:
      offset = cycle_token[2]
   except IndexError:
      offset = 0 

   ## create residue classes from cycle token
   residue_classes = [ ]
   for residue in residues:
      adjusted_residue = (residue + offset) % modulo
      residue_class = RC(modulo, adjusted_residue)
      residue_classes.append(residue_class)

   residue_classes.sort(lambda x, y: cmp(x.residue, y.residue))

   ## return sieve as residue class combination
   sieve = RCexpression(residue_classes, operator = 'or')
   return sieve
