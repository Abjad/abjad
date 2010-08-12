from abjad.core import _Abjad
from abjad.core import _Immutable
import types


class Articulation(_Abjad, _Immutable):
   '''Any staccato, tenuto, portato or other articulation:

      ::

         abjad> t = Articulation('staccato', 'up')
         abjad> print t.format
         -\staccato
   '''

   def __init__(self, *args):
      assert len(args) in range(3)
      if 2 <= len(args):
         assert isinstance(args[0], (str, type(None)))
         assert isinstance(args[1], (str, type(None)))
         #self.string = args[0]
         #self.direction = args[1]
         string, direction = args
      elif len(args) == 1:
         assert isinstance(args[0], (str, type(None)))
         if args[0]:
            splits = args[0].split('\\')
            assert len(splits) in (1, 2)
            if len(splits) == 1:
               #self.string = args[0]
               #self.direction = None
               string, direction = args[0], None
            elif len(splits) == 2:
               #self.string = splits[1]
               string = splits[1]
               if splits[0]:
                  #self.direction = splits[0]
                  direction = splits[0]
               else:
                  #self.direction = None
                  direction = None
         else:
            #self.string = None
            #self.direction = None
            string, direction = None, None
      else:
         #self.string = None
         #self.direction = None
         string, direction = None, None

      if direction in ('^', 'up'):
         _direction = '^'
      elif direction in ('_', 'down'):
         _direction = '_'
      elif direction in ('-', 'default', None):
         _direction = '-'
      else:
         raise ValueError('can not set articulation direction.')

      object.__setattr__(self, '_string', string)
      object.__setattr__(self, '_direction', _direction)

   ## OVERLOADS ##

   def __eq__(self, expr):
      assert isinstance(expr, Articulation)
      if expr.string == self.string and self.direction == expr.direction:
         return True
      else:
         return False

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, self)

   def __str__(self):
      if self.string:
         string = self._shortcut_to_word.get(self.string)
         if not string:
            string = self.string
         return '%s\%s' % (self.direction, string)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   _articulations_supported = ('accent', 'marcato', 
        'staccatissimo',      'espressivo'
        'staccato',           'tenuto'             'portato'
        'upbow',              'downbow'            'flageolet'
        'thumb',              'lheel'              'rheel'
        'ltoe',               'rtoe'               'open'
        'stopped',            'turn'               'reverseturn'
        'trill',              'prall'              'mordent'
        'prallprall'          'prallmordent',      'upprall',
        'downprall',          'upmordent',         'downmordent',
        'pralldown',          'prallup',           'lineprall',
        'signumcongruentiae', 'shortfermata',      'fermata',
        'longfermata',        'verylongfermata',   'segno',
        'coda',               'varcoda', 
        '^', '+', '-', '|', '>', '.', '_',
        )

   _shortcut_to_word = {
         '^':'marcato', '+':'stopped', '-':'tenuto', '|':'staccatissimo', 
         '>':'accent', '.':'staccato', '_':'portato' }

   ## PUBLIC ATTRIBUTES ##

#   @apply
#   def direction( ):
#      def fget(self):
#         '''Read / write LilyPond direction string.
#
#            *  Default value: ``None``.
#            *  All values: ``'^'``, ``'_'``, ``'-'``, \
#               ``'up'``, ``'down'``, ``'default'``, ``None``.
#
#            ::
#
#               abjad> t = Articulation('staccato')
#
#            ::
#
#               abjad> t.direction = 'up'
#               abjad> print t.format
#               ^\staccato
#
#            ::
#
#               abjad> t.direction = 'down'
#               abjad> print t.format
#               _\staccato
#         '''
#
#         return self._direction
#      def fset(self, expr):
#         assert isinstance(expr, (str, type(None)))
#         if expr in ('^', 'up'):
#            self._direction = '^'
#         elif expr in ('_', 'down'):
#            self._direction = '_'
#         elif expr in ('-', 'default', None):
#            self._direction = '-'
#         else:
#            raise ValueError('can not set articulation direction.')
#      return property(**locals( ))

   @property
   def direction(self):
      '''Read / write LilyPond direction string:

      ::

         abjad> articulation = Articulation('staccato', 'up')

      Defaults to none. Acceptable values are ``'^'``, ``'_'``, ``'-'``, 
      ``'up'``, ``'down'``, ``'default'``, ``None``.
      '''
      return self._direction

   @property
   def format(self):
      '''Read-only LilyPond format string.

         ::

            abjad> t = Articulation('staccato')
            abjad> print t.format
            -\staccato'''
         
      return str(self)

#   @apply
#   def string( ):
#      def fget(self):
#         '''Read / write string representation of accidental.
#
#            * All values: any LilyPond articulation string, ``None``.
#
#            ::
#
#               abjad> t = Articulation('staccato')
#               abjad> t.string = 'marcato'
#               abjad> print t.format
#               -\marcato'''
#
#         return self._string
#      def fset(self, expr):
#         assert isinstance(expr, (str, type(None)))
#         self._string = expr
#      return property(**locals( ))

   @property
   def string(self):
      return self._string
