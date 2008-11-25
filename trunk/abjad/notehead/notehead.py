from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.notehead.formatter import _NoteHeadFormatter
from abjad.pitch.pitch import Pitch


class _NoteHead(_Interface, _GrobHandler):

   def __init__(self, client, pitch = None):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'NoteHead')
      self._formatter = _NoteHeadFormatter(self)
      self.pitch = pitch
      self._style = None

   ### OVERLOADS ###

   def __cmp__(self, arg):
      raise Exception(NotImplemented)

   def __eq__(self, arg):
      return id(self) == id(arg)

   def __ne__(self, arg):
      return id(self) == id(arg)

   def __repr__(self):
      if self.pitch:
         return '_NoteHead(%s)' % self.pitch
      else:
         return '_NoteHead( )'

   def __str__(self):
      if self.pitch:
         return str(self.pitch)
      else:
         return ''

   ### PRIVATE ATTRIBUTES ###

   _abjadLilyStyles = {
      'triangle' : 'do',         'semicircle' : 're',    'diamond' : 'mi',
      'tiltedtriangle' : 'fa',   'square' : 'la',        'wedge' : 'ti' }

   @property
   def _abjadToLilyStyle(self):
      style = self._abjadLilyStyles.get(self.style)
      if style:
         return style
      else: 
         return self.style
      
   @property
   def _before(self):
      result = [ ]
      if self._client.kind('Chord'):
         result.extend(self._chordFormat)
      else:
         result.extend(_GrobHandler._before.fget(self))
         result.extend(self._noteFormat)
      return result

   @property
   def _chordFormat(self):
      result = [ ]
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            result.append(r'\tweak %s %s' % (
               self._parser.formatAttribute(key),
               self._parser.formatValue(value)))
      if self.style:
         if self.style in self.stylesSupported:
            result.append(r'\tweak %s %s' % (
                  self._parser.formatAttribute('style'),
                  self._parser.formatValue(self._abjadToLilyStyle)))
         else:
            result.append(r"\%s" % self.style)
      return result

   @property
   def _noteFormat(self):
      result = [ ]
      if self.style:
         if self.style in self.stylesSupported:
            result.append(r"\once \override NoteHead #'style = #'%s" \
               % self._abjadToLilyStyle)
         else:
            result.append(r"\%s" % self.style)
      return result
   
   ### PUBLIC ATTRIBUTES ###

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
            raise ValueError('Can not set _NoteHead.pitch = %s' % arg)
      return property(**locals( ))

   @property
   def format(self):
      return self._formatter.lily

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

   stylesSupported = (
      'cross', 'parallelogram', 'concavetriangle', 'slash', 'xcircle', 
      'neomensural', 'harmonic', 'mensural', 'petruccidiamond', 
      'triangle',  'semicircle',  'diamond', 'tiltedtriangle', 
      'square', 'wedge', )

