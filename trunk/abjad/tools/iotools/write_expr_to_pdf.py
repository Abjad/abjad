from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.iotools._log_render_lilypond_input import _log_render_lilypond_input
import os
import shutil


def write_expr_to_pdf(expr, file_name, template = None):
   '''Write `expr` to pdf `file_name`::

      abjad> note = Note(0, (1, 4))
      abjad> write_expr_to_pdf(note, 'one_note.pdf')

   Write `expr` to pdf `file_name` with `template`::

      abjad> note = Note(0, (1, 4))
      abjad> write_expr_to_pdf(note, 'one_note.pdf', 'paris')
   '''

   ## massage file_name
   file_name = os.path.expanduser(file_name)
   if not file_name.endswith('.pdf'):
      file_name += '.pdf'

   name = _log_render_lilypond_input(expr, template = template)

   ## copy PDF file to file_name
   pdf_name = name[:-3] + '.pdf'
   ABJADOUTPUT = _read_config_file( )['abjad_output']
   full_path_pdf_name = os.path.join(ABJADOUTPUT, pdf_name)
   shutil.move(full_path_pdf_name, file_name)

   print 'LilyPond PDF written to %s.' % os.path.basename(file_name)
