from abjad import *


def test_cfgtools_list_environment_variables_01( ):

   environment_variables = cfgtools.list_environment_variables( )

   assert all([isinstance(x, tuple) for x in environment_variables])
