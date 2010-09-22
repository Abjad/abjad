from abjad.tools.iotools.get_lilypond_version import get_lilypond_version


def _write_lilypond_version(outfile):
   outfile.write(r'\version "%s"' % get_lilypond_version( ))
   outfile.write('\n')
