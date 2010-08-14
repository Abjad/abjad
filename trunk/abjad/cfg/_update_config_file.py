from abjad.cfg.cfg import ABJADCONFIG
from abjad.cfg._write_config_file import _write_config_file


def _update_config_file(new_dict, old_dict):
   '''
   new_dict is drawn from abjad.cfg._config_file_dict.
   old_dict is drawn from abjad.cfg._read_config_file.
   '''

   for key in new_dict:
      try:
         new_dict[key]['value'] = old_dict[key]
      except KeyError:
         pass

   _write_config_file(ABJADCONFIG, new_dict)
