from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class AccidentalInterface(_Interface, _GrobHandler):
   '''Interface to all accidental-related settings and information.

      *  Manage *LilyPond* ``Accidental`` grob.
      *  Manage *LilyPond* ``set-accidental-style`` function.

      ::

         abjad> t = Staff(construct.scale(4))
         abjad> t.accidental
         <AccidentalInterface>'''

   def __init__(self, _client):
      '''Bind client and set style to None.'''

      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'Accidental')
      self._style = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contribution at container opening.'''
      result = [ ]
      style = self.style
      if style:
         result.append(r"#(set-accidental-style '%s)" % style)
      return result

   @apply
   def style( ):
      def fget(self):
         r'''Read / write *LilyPond* accidental style.
      
            *  Default value: ``None``.
            *  All values: *LilyPond* accidental style string, ``None``.

            ::

               abjad> t = Staff(construct.scale(4))
               abjad> t.accidental.style = 'forget'

            ::

               abjad> print t.format
               \new Staff {
                       #(set-accidental-style 'forget)
                       c'8
                       d'8
                       e'8
                       f'8
               }'''

         return self._style
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._style = arg
      return property(**locals( ))
