from abjad.core.formatcontributor import _FormatContributor
from abjad.core.parser import _Parser


class _GrobHandler(_FormatContributor):
   '''Abstract class from which all concrete Abjad grob handlers inherit.

   Concrete Abjad grob handlers include the accidentals interface, dots
   interface, text interface and tuplet bracket interface.

   See :term:`grob` for information on the core LilyPond concept.'''

   def __init__(self, grob):
      _FormatContributor.__init__(self)
      self._grob = grob
      self._parser = _Parser( )
      self._promotions = { }

   ## OVERLOADS ##

   ## TODO: Deprecate _GrobHandler.__len__ because not semantic. ##

   def __len__(self):
      return len([kvp for kvp in vars(self).items( ) 
         if not kvp[0].startswith('_')])

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in vars(self):
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ## PRIVATE METHODS ##

   def _promotedGrob(self, attribute):
      context = self._promotions.get(attribute, None)
      if context:
         return '%s.%s' % (str(context), self._grob)
      else:
         return '%s' % self._grob

   ## PRIVATE ATTRIBUTES ##

   @property
   def _frequencyIndicator(self):
      from abjad.leaf.leaf import _Leaf
      if hasattr(self, '_client') and isinstance(self._client, _Leaf):
         return r'\once '
      else:
         return ''

   ## PUBLIC ATTRIBUTES ##

   @property
   def _before(self):
      '''Read-only list of strings to contribute at format time.'''

      result = [ ]
      return result

   @property
   def overrides(self):
      r'''Read-only, alphabetized list of LilyPond \override strings 
      to contribute at format time.'''

      result = [ ]
      for key, value in sorted(vars(self).items( )):
         if not key.startswith('_'):
            result.append(r'%s\override %s %s = %s' % (
               self._frequencyIndicator,
               self._promotedGrob(key),
               self._parser.formatAttribute(key),
               self._parser.formatValue(value)))
      return result

   @property
   def reverts(self):
      r'''Read-only list of LilyPond \revert strings to contribute
      at format time.'''

      result = [ ]
      for key, value in vars(self).items( ):
         if not key.startswith('_'):
            result.append(r'%s\revert %s %s' % (
               self._frequencyIndicator,
               self._promotedGrob(key),
               self._parser.formatAttribute(key)))
      return result

   ## PUBLIC METHODS ##

   def clear(self):
      '''Remove all grob settings.'''

      for key, value in vars(self).items( ):
         if not key.startswith('_'):
            delattr(self, key)

   def promote(self, attribute, context):
      r'''Promote `attribute` to LilyPond `context`.
      Both `attribute` and `context` must be strings. ::

         abjad> staff = Staff(construct.scale(4))
         abjad> staff[0].clef.color = 'red'
         abjad> staff[0].clef.promote('color', 'Staff')

         abjad> print staff.format
         \new Staff {
                 \once \override Staff.Clef #'color = #red
                 c'8
                 d'8
                 e'8
                 f'8
         }

      This code overrides the color of the clef preceding the first
      note in staff and then promotes that color override to the 
      LilyPond staff context. This is important because the LilyPond
      engraver that creates clef symbols lives at the staff context
      and does not live at the lower level of the voice context.
      '''

      assert isinstance(context, str)
      if hasattr(self, attribute):
         self._promotions[attribute] = context
      else:
         raise AttributeError('no %s attribute.' % attribute)
