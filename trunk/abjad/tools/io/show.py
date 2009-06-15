from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.log_render_lilypond_input import _log_render_lilypond_input
from abjad.cfg.open_file import _open_file
from abjad.cfg.read_config_value import _read_config_value
import os


## TODO: Implement show( ) 'footer' keyword to allow dynamic footer. ##
## TODO: Extend show( ) 'title' keyword to allow multiple lines. ##

def show(expr, template = None, title = None, lilytime = 10):
   '''Render *expr* as `LilyPond` input, call `LilyPond` \
      and open the resulting PDF.

      Examples.

      Render ``t`` and open the resulting PDF:

      ::

         abjad> t = Note(0, (1, 4))
         abjad> show(t)

      Render ``t`` with the ``tangiers.ly`` template \ 
      and then open the resulting PDF:

      ::

         abjad> show(t, template = 'tangiers')

      Render ``t`` with a score title and open the reuslting PDF:

      ::

         abjad> show(t, title = 'Score Title')

      Render ``t``, open the resulting PDF and alert the composer \
      if *LilyPond* takes greater than 60 seconds to render:

      ::

         abjad> show(t, lilytime = 60)

      .. note::
         By default, `Abjad` writes `LilyPond` input files
         to the ``~/.abjad/output`` directory, otherwise to 
         ``$ABJADOUTPUT``, if the environment variable is set.'''

   name = _log_render_lilypond_input(expr, template, title, lilytime)
   pdfviewer = _read_config_value('pdfviewer')
   name = os.path.join(ABJADOUTPUT, name)
   _open_file('%s.pdf' % name[:-3], pdfviewer)
