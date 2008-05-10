from .. core.interface import _Interface
from formatter import _NoteHeadFormatter
from .. pitch.pitch import Pitch


class _NoteHead(_Interface):

   def __init__(self, client, pitch = None):
      _Interface.__init__(self, client, 'NoteHead', [ ])
      self._client = client
      self._formatter = _NoteHeadFormatter(self)
      self.pitch = pitch
      self._shape = None

   ### REPR ###

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

   ### MATH AND COMPARISON TESTING ###

   def __cmp__(self, arg):
      return cmp(self.pitch, arg.pitch)

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
            raise ValueError('Can not set _NoteHead.pitch = %s' % arg)
      return property(**locals( ))

   @apply
   def shape( ):
      def fget(self):
         return self._shape
      def fset(self, expr):
         if expr is None:
            self._shape = None
         elif isinstance(expr, str):
            self._shape = expr
         else:
            raise ValueError('can not set notehead shape.')
      return property(**locals( ))

   ### SHAPE NOTE HANDLERS ###

   shapesSupported = (
      'cross', 'parallelogram', 'concavetriangle', 'slash', 'xcircle', 
      'neomensural', 'harmonic', 'mensural', 'petruccidiamond', 
      'triangle',  'semicircle',  'diamond', 'tiltedtriangle', 
      'square', 'wedge', )

   _noteheadShapeToShapeNoteStyle = {
      'triangle' : 'do',         'semicircle' : 're',    'diamond' : 'mi',
      'tiltedtriangle' : 'fa',   'square' : 'la',        'wedge' : 'ti' }

   @property
   def _shapeNoteStyleSetting(self):
      result = [ ]
      if self.shape:
         if self.shape in self.shapesSupported:
            try:
               shape = self._noteheadShapeToShapeNoteStyle[self.shape]
            except KeyError:
               shape = self.shape
            result.append(r"\once \override NoteHead #'style = #'%s" % shape)
         else:
            result.append(r"\%s" % self.shape + \
            ' % user definded notehead variable')
      return result

#   def _shapeNoteStyleVector(self, shape):
#      return '#(%s)' % ' '.join(
#         [self._noteheadShapeToShapeNoteStyle[shape]] * 7)

#   @property
#   def _shapeNoteStyleSetting(self):
#      result = [ ]
#      if self.shape:
#         result.append(r'\once \set shapeNoteStyles = #%s' % 
#            self._shapeNoteStyleVector(self.shape))
#      return result


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
      result.extend(self._shapeNoteStyleSetting)
      return result

   @property
   def format(self):
      return self._formatter.lily
