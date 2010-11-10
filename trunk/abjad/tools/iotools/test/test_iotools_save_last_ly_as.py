from abjad import *
import os


def test_iotools_save_last_ly_as_01( ):

   iotools.save_last_ly_as('tmp_foo.ly')
   assert os.path.exists('tmp_foo.ly') 
   
   os.remove('tmp_foo.ly')
   assert not os.path.exists('tmp_foo.ly') 
