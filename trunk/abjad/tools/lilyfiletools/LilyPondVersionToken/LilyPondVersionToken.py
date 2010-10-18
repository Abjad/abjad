from abjad.core import _Immutable
from abjad.tools.cfgtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondVersionToken(_Immutable):
   r'''.. versionadded:: 1.1.2

   LilyPond version token::

      abjad> lilyfiletools.LilyPondVersionToken( )
      LilyPondVersionToken(\version "2.13.32")
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.format)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      r'''Format contribution of LilyPond version token:

      ::

         abjad> lilyfiletools.LilyPondVersionToken( ).format
         '\\version "2.13.32"'
      '''
      return r'\version "%s"' % get_lilypond_version_string( )
