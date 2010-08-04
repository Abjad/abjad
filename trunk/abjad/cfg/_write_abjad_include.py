from abjad.cfg.cfg import ABJADPATH
import os


def _write_abjad_include(outfile):
   if ABJADPATH is not None:
      #abjad_include = os.path.join(ABJADPATH, 'scm', 'abjad.scm')
      abjad_include = os.path.join(ABJADPATH, 'cfg', 'abjad.scm')
      outfile.write('\\include "%s"\n' % abjad_include)
