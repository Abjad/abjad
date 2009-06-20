from abjad.notehead.format import _NoteHeadFormatInterface
from abjad.notehead.interface import _NoteHeadInterface
#from abjad.pitch.pitch import Pitch


class NoteHead(_NoteHeadInterface):

   def __init__(self, client, pitch = None):
      _NoteHeadInterface.__init__(self, client)
      self._formatter = _NoteHeadFormatInterface(self)
      self._style = None
      self.pitch = pitch
      self._unregister_if_necessary( )

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, NoteHead):
         if self.pitch == expr.pitch:
            return True
      return False

   def __repr__(self):
      if self.pitch:
         return 'NoteHead(%s)' % self.pitch
      else:
         return 'NoteHead( )'

   def __str__(self):
      if self.pitch:
         return str(self.pitch)
      else:
         return ''

   ## PRIVATE METHODS ##

   def _unregister_if_necessary(self):
      '''Note noteheads should register as format contributors.
         Chord noteheads should not register as format contributors.'''
      from abjad.chord import Chord
      client = getattr(self, '_client', None)
      if client is not None:
         if isinstance(client, Chord):
            client.interfaces._contributors.remove(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return self.formatter.format

   @property
   def formatter(self):
      return self._formatter

   @apply
   def pitch( ):
      def fget(self):
         return self._pitch
      def fset(self, arg):
         from abjad.pitch.pitch import Pitch
         if arg is None:
            self._pitch = None
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         elif isinstance(arg, tuple):
            self._pitch = Pitch(*arg) 
         elif isinstance(arg, Pitch):
            self._pitch = arg
         elif isinstance(arg, NoteHead):
            self._pitch = arg.pitch
         else:
            raise ValueError('Can not set _NoteHead.pitch = %s' % arg)
      return property(**locals( ))

   @apply
   def style( ):
      def fget(self):
         return self._style
      def fset(self, expr):
         if expr is None:
            self._style = None
         elif isinstance(expr, str):
            self._style = expr
         else:
            raise ValueError('can not set notehead style.')
      return property(**locals( ))
