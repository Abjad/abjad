from abjad import *


def test_cfgtools_get_python_version_string_01( ):

   
   python_version_string = cfgtools.get_python_version_string( )

   assert isinstance(python_version_string, str)
   assert python_version_string.count('.') == 2
