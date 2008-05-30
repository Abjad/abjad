
class _Articulation(object):

   def __init__(self, string = None, direction = None):
      self.string = string
      self.direction = direction

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
        'coda',               'varcoda',)

   _shortcutToWord = {
         '^':'marcato', '+':'stopped', '-':'tenuto', '|':'staccatissimo', 
         '>':'accent', '.':'staccato', '_':'portato' }


   ### OVERRIDES ###

   def __eq__(self, expr):
      assert isinstance(expr, _Articulation)
      if expr.string == self.string and self.direction == expr.direction:
         return True
      else:
         return False

   ### REPR ###

   def __repr__(self):
      return '_Articulation(%s)' % self

   def __str__(self):
      if self.string:
         string = self._shortcutToWord.get(self.string)
         if not string:
            string = self.string
         return '%s\%s' % (self.direction, string)
      else:
         return ''

   ### MANAGED ATTRIBUTES ###

   @apply
   def string( ):
      def fget(self):
         return self._string
      def fset(self, expr):
         if expr is None:
            self._string = None #''
         elif isinstance(expr, str):
            self._string = expr
         else:
            raise ValueError('can not set articulation string.')
      return property(**locals( ))

   @apply
   def direction( ):
      def fget(self):
         return self._direction
      def fset(self, expr):
         if expr is None:
            self._direction = '-'
         elif isinstance(expr, str):
            if expr in ('^', 'up'):
               self._direction = '^'
            elif expr in ('_', 'down'):
               self._direction = '_'
            elif expr in ('-', 'center'):
               self._direction = '-'
            else:
               raise ValueError('can not set articulation direction.')
         else:
            raise ValueError('can not set articulation direction.')
      return property(**locals( ))


   ### FORMATTING ###

   @property
   def lily(self):
      return str(self)
      


