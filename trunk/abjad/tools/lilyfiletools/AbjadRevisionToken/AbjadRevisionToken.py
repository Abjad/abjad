from abjad.core import _Immutable
from abjad.tools.cfgtools.get_abjad_revision_string import get_abjad_revision_string


class AbjadRevisionToken(_Immutable):
   '''.. versionadded:: 1.1.2

   Abjad version token::

      abjad> lilyfiletools.AbjadRevisionToken( )
      AbjadRevisionToken(Abjad revision 3719)
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.format)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Format contribution of Abjad version token:

      ::

         abjad> lilyfiletools.AbjadRevisionToken( ).format
         'Abjad revision 3719'
      '''
      abjad_revision_string = get_abjad_revision_string( )
      return 'Abjad revision %s' % abjad_revision_string
