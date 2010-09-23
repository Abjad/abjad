from abjad.tools.iotools.get_abjad_version_string import get_abjad_version_string
import time


def _write_abjad_header(outfile):
   cur_time = time.strftime('%Y-%m-%d %H:%M')
   outfile.write('%% Abjad revision %s\n' % get_abjad_version_string( ))
   outfile.write('%% %s\n\n' % cur_time)
