from abjad import *


def test_cfgtools_list_abjad_templates_01( ):

   templates = cfgtools.list_abjad_templates( )

   assert all([isinstance(x, str) for x in templates])
