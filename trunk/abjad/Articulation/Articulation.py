from abjad.core import _Abjad
import types


class Articulation(_Abjad):
   '''Any staccato, tenuto, portato, etc.

      ::

         abjad> t = Articulation('staccato')
         abjad> print t.format
         -\staccato'''

   def __init__(self, string = None, direction = None):
      '''Init ``string`` and ``direction`` both to ``None``.'''

      self.string = string
      self.direction = direction

   ## OVERLOADS ##

   def __eq__(self, expr):
      assert isinstance(expr, Articulation)
      if expr.string == self.string and self.direction == expr.direction:
         return True
      else:
         return False

   def __repr__(self):
      return 'Articulation(%s)' % self

   def __str__(self):
      if self.string:
         string = self._shortcutToWord.get(self.string)
         if not string:
            string = self.string
         return '%s\%s' % (self.direction, string)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   _articulationsSupported = ('accent', 'marcato', 
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

   _shortcutToWord = {
         '^':'marcato', '+':'stopped', '-':'tenuto', '|':'staccatissimo', 
         '>':'accent', '.':'staccato', '_':'portato' }

   ## PUBLIC ATTRIBUTES ##

   @apply
   def direction( ):
      def fget(self):
         '''Read / write *LilyPond* direction string.

            *  Default value: ``None``.
            *  All values: ``'^'``, ``'_'``, ``'-'``, \
               ``'up'``, ``'down'``, ``'default'``, ``None``.

            ::

               abjad> t = Articulation('staccato')

            ::

               abjad> t.direction = 'up'
               abjad> print t.format
               ^\staccato

            ::

               abjad> t.direction = 'down'
               abjad> print t.format
               _\staccato'''

         return self._direction
      def fset(self, expr):
         assert isinstance(expr, (str, types.NoneType))
         if expr in ('^', 'up'):
            self._direction = '^'
         elif expr in ('_', 'down'):
            self._direction = '_'
         elif expr in ('-', 'default', None):
            self._direction = '-'
         else:
            raise ValueError('can not set articulation direction.')
      return property(**locals( ))

   @property
   def format(self):
      '''Read-only *LilyPond* format string.

         ::

            abjad> t = Articulation('staccato')
            abjad> print t.format
            -\staccato'''
         
      return str(self)

   @apply
   def string( ):
      def fget(self):
         '''Read / write string representation of accidental.

            * All values: any *LilyPond* articulation string, ``None``.

            ::

               abjad> t = Articulation('staccato')
               abjad> t.string = 'marcato'
               abjad> print t.format
               -\marcato'''

         return self._string
      def fset(self, expr):
         assert isinstance(expr, (str, types.NoneType))
         self._string = expr
      return property(**locals( ))
