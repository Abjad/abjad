from abjad.cfg.cfg import ABJADCONFIG
from abjad.cfg._write_config_file import _write_config_file
import os


def _verify_config_file( ):
   try:
      f = open(ABJADCONFIG, 'r')
      f.close( )
   except IOError:
      raw_input('Attention: "%s" does not exist in your system.\n\
      Abjad will now create it to store all configuration settings. \n\
      You may want to edit this file to configure Abjad to your liking.\n\
      Press any key to continue.' % ABJADCONFIG)

      abjad_config_dir = os.path.dirname(ABJADCONFIG) 
      if not os.path.isdir(abjad_config_dir):
         os.mkdir(abjad_config_dir)
      _write_config_file(ABJADCONFIG)

