from abjad.cfg.cfg import ABJADCONFIG
from abjad.cfg.verify_config_file import _verify_config_file

def _read_config_file( ):
   '''Read the content of the config file $HOME/.abjad/config.'''
   _verify_config_file( )
   f = open(ABJADCONFIG, 'r')
   lines = f.readlines( )
   f.close( )
   return lines   
