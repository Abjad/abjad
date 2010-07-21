from abjad import *


def test_RC___init____01( ):
   '''Init from modulo and residue.'''

   rc = sievetools.RC(6, 0)

   assert isinstance(rc, sievetools.RC)
   assert rc.modulo == 6
   assert rc.residue == 0


def test_RC___init____02( ):
   '''Init from other rc instance.'''

   rc = sievetools.RC(sievetools.RC(6, 0))

   assert isinstance(rc, sievetools.RC)
   assert rc.modulo == 6
   assert rc.residue == 0
