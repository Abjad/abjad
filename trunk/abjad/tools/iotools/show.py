from abjad.cfg._log_render_lilypond_input import _log_render_lilypond_input
from abjad.cfg._open_file import _open_file
from abjad.cfg._read_config_file import _read_config_file
import os


def show(expr, template = None, title = None, footer = None, 
   lily_time = 10, format_time = 10, return_timing = False,
   suppress_pdf = False):
   '''Format `expr` as a valid string of LilyPond input.

   Call LilyPond on the formatted version of `expr`.

   Open the PDF that LilyPond creates.

   Render `t` and open the resulting PDF::

      abjad> t = Note(0, (1, 4))
      abjad> show(t)

   Render `t` with the ``tangiers.ly`` template and then 
   open the resulting PDF::

      abjad> show(t, template = 'tangiers')

   Render `t` with a score title and open the resulting PDF::

      abjad> show(t, title = 'Score Title')

   Render `t` with a multiline score title and open the resulting PDF::

      abjad> show(t, title = ['Score Title', 'score subtitle', 'more subtitle'])

   .. versionadded:: 1.1.1
      Render `t` with a footer and open the resulting PDF:

   ::

      abjad> show(t, footer = '"This is footer text."')

   Render `t` and open the resulting PDF. Alert the composer
   if LilyPond takes greater than 60 seconds to render::

      abjad> show(t, lily_time = 60)

   .. versionadded:: 1.1.2
      Render `t` and open the resulting PDF. Alert the composer
      if Abjad takes greater than 10 seconds to format `t`:

   ::

      abjad> show(t, format_time = 10)

   .. versionadded:: 1.1.2
      Render `t`, open the resulting PDF, and return both the number
      of seconds it took Abjad to format `t` and also the number
      of seconds it took LilyPond to render `t`:

   ::

      abjad> show(t, return_timing = True)

   .. note:: 
      By default, Abjad writes LilyPond input files
      to the ``~/.abjad/output`` directory. You may change this by
      setting the ``abjad_output`` variable in the ``config.py`` file.
   '''

   ## format expr and write lilypond input file
   name, actual_format_time, actual_lily_time = _log_render_lilypond_input(
      expr, template = template, title = title, footer = footer, 
      lily_time = lily_time, format_time = format_time)

   ## do not open PDF if we're running py.test regression battery
   if not suppress_pdf:
      config = _read_config_file( )
      pdf_viewer = config['pdf_viewer']
      ABJADOUTPUT = config['abjad_output']
      name = os.path.join(ABJADOUTPUT, name)
      _open_file('%s.pdf' % name[:-3], pdf_viewer)

   ## return timing if requested
   if return_timing:
      return actual_format_time, actual_lily_time
