from abjad import *


def test_RC___init____01( ):
   '''Init from modulo and residue.'''

   rc = sievetools.ResidueClass(6, 0)

   assert isinstance(rc, sievetools.ResidueClass)
   assert rc.modulo == 6
   assert rc.residue == 0


def test_RC___init____02( ):
   '''Init from other rc instance.'''

   rc = sievetools.ResidueClass(sievetools.ResidueClass(6, 0))

   assert isinstance(rc, sievetools.ResidueClass)
   assert rc.modulo == 6
   assert rc.residue == 0
