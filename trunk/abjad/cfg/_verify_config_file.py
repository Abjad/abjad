from abjad.cfg.cfg import ABJADCONFIG
from abjad.cfg._config_file_dict import _config_file_dict as dict
from abjad.cfg._config_file_to_dict import _config_file_to_dict
from abjad.cfg._write_config_file import _write_config_file
from abjad.cfg._update_config_file import _update_config_file
import os


def _verify_config_file( ):
   try:
      f = open(ABJADCONFIG, 'r')
      f.close( )
      old_dict = _config_file_to_dict()

      if sorted(dict.keys()) != sorted(old_dict.keys()):
         raw_input( '\nAttention:\n\
         Your current Abjad configuration file ("%s") is out of date.\n\
         Abjad will now overwrite the old with a new configuration file.\n\
         Any relavent keys from your old configuration will be maintained.\n\
         Press any key to continue.' % ABJADCONFIG)
         _update_config_file(dict, old_dict)

   except IOError:
      raw_input( '\nAttention:\n\
      "%s" does not exist in your system.\n\
      Abjad will now create it to store all configuration settings.\n\
      You may want to edit this file to configure Abjad to your liking.\n\
      Press any key to continue.' % ABJADCONFIG)
      _write_config_file(ABJADCONFIG, dict)
