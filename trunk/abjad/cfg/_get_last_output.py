from abjad.cfg.cfg import ABJADOUTPUT
import os
import re


def _get_last_output( ):
   pattern = re.compile('\d{4,4}.ly')
   all_file_names = os.listdir(ABJADOUTPUT) 
   all_output = [fn for fn in all_file_names if pattern.match(fn)]
   if all_output == [ ]:
      last_output = None
   else:
      last_output = sorted(all_output)[-1]
   return last_output   
