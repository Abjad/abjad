#from abjad.cfg.cfg import LILYPONDLANG
from abjad.cfg._read_config_file import _read_config_file


def _write_lilypond_language(outfile):
   LILYPONDLANG = _read_config_file( )['lilypondlang']
   outfile.write(r'\include "%s.ly"' % LILYPONDLANG.lower( ))
   outfile.write('\n')
