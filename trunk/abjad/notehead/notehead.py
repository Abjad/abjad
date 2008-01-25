from .. core.interface import _Interface
from formatter import NoteHeadFormatter
from .. pitch.pitch import Pitch


class NoteHead(_Interface):

   def __init__(self, client, pitch = None):
      _Interface.__init__(self, client, 'NoteHead', [ ])
      self._client = client
      self._formatter = NoteHeadFormatter(self)
      self.pitch = pitch

   ### REPR ###

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

   ### PROPERTIES ###

   @apply
   def pitch( ):
      def fget(self):
         return self._pitch
      def fset(self, arg):
         if arg is None:
            self._pitch = None
         elif isinstance(arg, Pitch):
            self._pitch = arg
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         else:
            raise ValueError('Can not set NoteHead.pitch = %s' % arg)
      return property(**locals( ))

   ### FORMATTING ###

   @property
   def _before(self):
      result = [ ]
      if self._client.kind('Chord'):
         for key, value in self.__dict__.items( ):
            if not key.startswith('_'):
               result.append(r'\tweak %s %s' % (
                  self._parser.formatAttribute(key),
                  self._parser.formatValue(value)))
      else:
         result.extend(_Interface._before.fget(self))
      return result

   @property
   def format(self):
      return self._formatter.lily
