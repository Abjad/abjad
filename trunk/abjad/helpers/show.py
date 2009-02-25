from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.cfg import ABJADTEMPLATES
from abjad.cfg.cfg import PDFVIEWER
from abjad.cfg.get_next_output import _get_next_output
from abjad.cfg.open_file import _open_file
from abjad.cfg.run_lilypond import _run_lilypond
from abjad.cfg.verify_output_directory import _verify_output_directory
from abjad.cfg.wrap_format import _wrap_format
from abjad.cfg.write_preamble import _write_preamble
#from abjad.cfg.write_abjad_header import _write_abjad_header
#from abjad.cfg.write_abjad_include import _write_abjad_include
#from abjad.cfg.write_environment_includes import _write_environment_includes
#from abjad.cfg.write_layout_template import _write_layout_template
#from abjad.cfg.write_lilypond_language import _write_lilypond_language
#from abjad.cfg.write_lilypond_version import _write_lilypond_version
from abjad.cfg.write_title import _write_title
import os


def show(ly, template = None, title = None):
   '''
   Interprets a complete .ly file in ABJADOUTPUT directory.
   Logs to ABJADOUTPUT/lily.log.
   Opens the resulting PDF with PDFVIEWER.
   '''

   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = _get_next_output( )
   outfile = open(name, 'w')
#   _write_abjad_header(outfile)
#   _write_lilypond_version(outfile)
#   _write_lilypond_language(outfile)
#   _write_abjad_include(outfile)
#   _write_environment_includes(outfile)
#   _write_layout_template(outfile, template)
#   outfile.write('\n')
   _write_preamble(outfile, template)
   _write_title(outfile, title)
   outfile.write(_wrap_format(ly.format))
   outfile.close( )
   _run_lilypond(name)
   _open_file('%s.pdf' % name[:-3], PDFVIEWER)
