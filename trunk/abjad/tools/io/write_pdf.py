from abjad.cfg.log_render_lilypond_input import _log_render_lilypond_input
import os

def write_pdf(expr, file_name, template = None, title = None, lilytime = 10):
   '''Render ``expr`` as `LilyPond` input, call `LilyPond`
   and write the resulting PDF as ``file_name``::

      abjad> t = Note(0, (1, 4))
      abjad> write_pdf(t, 'one_note.pdf')'''

   current_directory = os.path.abspath('.')

   name = _log_render_lilypond_input(expr, template, title, lilytime)

   ## copy PDF file to current dir
   pdf_name = name[:-3] + '.pdf'
   full_file_name = os.path.join(current_directory, file_name)
   os.system('mv %s %s' % (pdf_name, full_file_name))

   print 'LilyPond PDF written to %s.' % full_file_name
