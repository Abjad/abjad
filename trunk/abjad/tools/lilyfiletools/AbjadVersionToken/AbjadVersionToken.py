from abjad.core import _Immutable
from abjad.tools.iotools.get_abjad_version_string import get_abjad_version_string


class AbjadVersionToken(_Immutable):
   '''.. versionadded:: 1.1.2

   Abjad version token::

      abjad> lilyfiletools.AbjadVersionToken( )
      AbjadVersionToken(Abjad revision 3719)
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.format)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Format contribution of Abjad version token:

      ::

         abjad> lilyfiletools.AbjadVersionToken( ).format
         'Abjad revision 3719'
      '''
      abjad_version_string = get_abjad_version_string( )
      return 'Abjad revision %s' % abjad_version_string
