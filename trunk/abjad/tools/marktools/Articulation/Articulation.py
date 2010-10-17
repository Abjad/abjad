from abjad.components._Component import _Component
#from abjad.core import _StrictComparator
#from abjad.core import _Immutable
from abjad.tools.contexttools.ContextMark import ContextMark


#class Articulation(_StrictComparator, _Immutable):
class Articulation(Mark):
   '''Abjad model of music articulation:

   ::

      abjad> t = notetools.Articulation('staccato', 'up')
      Articulation('^\staccato')
   '''

   __slots__ = ('_string', '_direction', '_format_slot')

#   def __new__(klass, *args):
#
#      self = object.__new__(klass)
#
#      assert len(args) in range(3)
#      if 2 <= len(args):
#         assert isinstance(args[0], (str, type(None)))
#         assert isinstance(args[1], (str, type(None)))
#         string, direction = args
#      elif len(args) == 1:
#         assert isinstance(args[0], (str, type(None)))
#         if args[0]:
#            splits = args[0].split('\\')
#            assert len(splits) in (1, 2)
#            if len(splits) == 1:
#               string, direction = args[0], None
#            elif len(splits) == 2:
#               string = splits[1]
#               if splits[0]:
#                  direction = splits[0]
#               else:
#                  direction = None
#         else:
#            string, direction = None, None
#      else:
#         string, direction = None, None
#
#      if direction in ('^', 'up'):
#         direction = '^'
#      elif direction in ('_', 'down'):
#         direction = '_'
#      elif direction in ('-', 'default', None):
#         direction = '-'
#      else:
#         raise ValueError('can not set articulation direction.')
#
#      object.__setattr__(self, '_string', string)
#      object.__setattr__(self, '_direction', direction)
#
#      return self
#
#   def __getnewargs__(self):
#      return (self.string, self.direction)

   def __init__(self, *args):
      assert len(args) in range(3)
      Mark.__init__(self, target_context = _Component)
      if 2 <= len(args):
         assert isinstance(args[0], (str, type(None)))
         assert isinstance(args[1], (str, type(None)))
         string, direction = args
      elif len(args) == 1:
         assert isinstance(args[0], (str, type(None)))
         if args[0]:
            splits = args[0].split('\\')
            assert len(splits) in (1, 2)
            if len(splits) == 1:
               string, direction = args[0], None
            elif len(splits) == 2:
               string = splits[1]
               if splits[0]:
                  direction = splits[0]
               else:
                  direction = None
         else:
            string, direction = None, None
      else:
         string, direction = None, None

      if direction in ('^', 'up'):
         direction = '^'
      elif direction in ('_', 'down'):
         direction = '_'
      elif direction in ('-', 'default', None):
         direction = '-'
      else:
         raise ValueError('can not set articulation direction.')

      object.__setattr__(self, '_string', string)
      object.__setattr__(self, '_direction', direction)
      self._format_slot = 'right'
      self._contents_repr_string = '%s, %s' % (repr(self.string), repr(self.direction))

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self.string, self.direction)

   __deepcopy__ = __copy__

   def __eq__(self, expr):
      assert isinstance(expr, type(self))
      if expr.string == self.string:
         if self.direction == expr.direction:
            return True
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

   @property
   def direction(self):
      '''Direction string of articulation:

      ::

         abjad> articulation = notetools.Articulation('staccato', 'up')
         abjad> articulation.direction
         '^'
      '''
      return self._direction

   @property
   def format(self):
      '''LilyPond format string of articulation:

      ::

         abjad> articulation = notetools.Articulation('staccato', 'up')
         abjad> articulation.format
         '^\staccato'
      '''
      return str(self)

   @property
   def string(self):
      '''Name string of articulation:

      ::

         abjad> articulation = notetools.Articulation('staccato', 'up')
         abjad> articulation.string
         'staccato'
      '''
      return self._string
