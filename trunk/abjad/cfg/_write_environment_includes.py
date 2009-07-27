#from abjad.cfg.cfg import LILYPONDINCLUDES
from abjad.cfg._read_config_file import _read_config_file


def _write_environment_includes(outfile):
   LILYPONDINCLUDES  = _read_config_file( )['lilypondincludes']
   if LILYPONDINCLUDES is not None:
      includes = LILYPONDINCLUDES.split(':')
      for i in includes:
         outfile.write('\\include "%s"\n' % i)
