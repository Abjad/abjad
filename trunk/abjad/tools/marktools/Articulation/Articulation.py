from abjad.components._Component import _Component
from abjad.tools.marktools.Mark import Mark


class Articulation(Mark):
   '''Abjad model of musical articulation::

      abjad> note = Note("c'4")

   ::

      abjad> marktools.Articulation('staccato')(note)
      Articulation('staccato', '-')(c'4)

   ::

      abjad> f(note)
      c'4 -\staccato

   Articulations implement ``__slots__``.
   '''

   __slots__ = ('_string', '_direction', '_format_slot')

   def __init__(self, *args):
      assert len(args) in range(3)
      Mark.__init__(self)
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

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self.name_string, self.direction_string)

   __deepcopy__ = __copy__

   def __eq__(self, expr):
      assert isinstance(expr, type(self))
      if expr.name_string == self.name_string:
         if self.direction_string == expr.direction_string:
            return True
      return False

   def __str__(self):
      if self.name_string:
         string = self._shortcut_to_word.get(self.name_string)
         if not string:
            string = self.name_string
         return '%s\%s' % (self.direction_string, string)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   ## this causes unnecessary coupling to changeable lilypond codebase and is discouraged
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

   ## this causes unnecessary coupling to changeable lilypond codebase and is discouraged
   _shortcut_to_word = {
         '^':'marcato', '+':'stopped', '-':'tenuto', '|':'staccatissimo', 
         '>':'accent', '.':'staccato', '_':'portato' }

   @property
   def _contents_repr_string(self):
      return '%s, %s' % (repr(self.name_string), repr(self.direction_string))

   ## PUBLIC ATTRIBUTES ##

   @apply
   def direction_string( ):
      def fget(self):
         '''Get direction string of articulation::

            abjad> articulation = marktools.Articulation('staccato')
            abjad> articulation.direction_string
            '-'

         Set direction string of articulation::

            abjad> articulation.direction_string = '^'
            abjad> articulation.direction_string
            '^'
         '''
         return self._direction
      def fset(self, direction_string):
         assert isinstance(direction_string, str)
         self._direction = direction_string
      return property(**locals( ))

   @property
   def format(self):
      '''Read-only LilyPond format string of articulation:

      ::

         abjad> articulation = marktools.Articulation('staccato', 'up')
         abjad> articulation.format
         '^\staccato'
      '''
      return str(self)

   @apply
   def name_string( ):
      def fget(self):
         '''Get name string of articulation::

            abjad> articulation = marktools.Articulation('staccato', 'up')
            abjad> articulation.name_string
            'staccato'

         Set name string of articulation::

            abjad> articulation.name_string = 'marcato'
            abjad> articualtion.name_string
            'marcato'
         '''
         return self._string
      def fset(self, name_string):
         assert isinstance(name_string, str)
         self._string = name_string
      return property(**locals( ))
