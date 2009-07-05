from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.log_render_lilypond_input import _log_render_lilypond_input
import os
import shutil

def write_pdf(expr, file_name, template = None, 
   title = None, footer = None, lilytime = 10):
   '''Render `expr` as LilyPond input.

   Call LilyPond and write the resulting PDF as `file_name`. ::

      abjad> t = Note(0, (1, 4))
      abjad> write_pdf(t, 'one_note.pdf')
   '''

   ## massage file_name
   file_name = os.path.expanduser(file_name)
   if not file_name.endswith('.pdf'):
      file_name += '.pdf'

   name = _log_render_lilypond_input(expr, template = template, 
      title = title, footer = footer, lilytime = lilytime)

   ## copy PDF file to file_name
   pdf_name = name[:-3] + '.pdf'
   full_path_pdf_name = os.path.join(ABJADOUTPUT, pdf_name)
   shutil.move(full_path_pdf_name, file_name)

   print 'LilyPond PDF written to %s.' % os.path.basename(file_name)
