from abjad.cfg.lilypond_version import _get_lilypond_version


def _write_lilypond_version(outfile):
   outfile.write(r'\version "%s"' % _get_lilypond_version( ))
   outfile.write('\n')
