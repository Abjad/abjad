#from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg._read_config_file import _read_config_file
import os
import re


def _get_last_output( ):
   pattern = re.compile('\d{4,4}.ly')
   all_file_names = os.listdir(_read_config_file( )['abjad_output']) 
   all_output = [fn for fn in all_file_names if pattern.match(fn)]
   if all_output == [ ]:
      last_output = None
   else:
      last_output = sorted(all_output)[-1]
   return last_output   
