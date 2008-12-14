from abjad.cfg.cfg import ABJADPATH


def _write_abjad_include(outfile):
   if ABJADPATH is not None:
      outfile.write('\\include "%s/scm/abjad.scm"\n' % ABJADPATH)
