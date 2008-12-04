from abjad.cfg.lilypond_version import lilypond_version


def _write_lilypond_version(outfile):
   outfile.write(r'\version "%s"' % lilypond_version)
   outfile.write('\n')
