from abjad.cfg._read_config_file import _read_config_file


def _read_config_value(key):
   '''Read the configuration value for the given key in the config file.
      The key can be a any configuration parameter. 
      DEBUG is the only parameter available for now.'''

   assert isinstance(key, str)
   lines = _read_config_file( )
   for l in lines:
      l.strip( )
      if l.startswith(key):
         value = l.split('=')[1].strip( )
         if value != '':
            return value
         else:
            return None
