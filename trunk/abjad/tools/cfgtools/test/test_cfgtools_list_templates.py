from abjad import *


def test_cfgtools_list_templates_01( ):

   templates = cfgtools.list_templates( )

   assert all([isinstance(x, str) for x in templates])
