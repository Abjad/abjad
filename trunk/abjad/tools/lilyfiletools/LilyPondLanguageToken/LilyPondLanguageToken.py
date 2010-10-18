from abjad.cfg._read_config_file import _read_config_file
from abjad.core import _Immutable
from abjad.tools.cfgtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondLanguageToken(_Immutable):
   r'''.. versionadded:: 1.1.2

   LilyPond language token::

      abjad> lilyfiletools.LilyPondLanguageToken( )
      LilyPondVersionToken(\include "english.ly")
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.format)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      r'''Format contribution of LilyPond language token:

      ::

         abjad> lilyfiletools.LilyPondVersionToken( ).format
         '\\include "english.ly"
      '''
      lilypond_language = _read_config_file( )['lilypond_lang']
      return r'\include "%s.ly"' % lilypond_language.lower( )
