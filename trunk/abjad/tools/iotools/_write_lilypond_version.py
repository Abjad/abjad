from abjad.tools.iotools.get_lilypond_version_string import get_lilypond_version_string


def _write_lilypond_version(outfile):
   outfile.write(r'\version "%s"' % get_lilypond_version_string( ))
   outfile.write('\n')
