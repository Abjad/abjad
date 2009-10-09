class DiatonicInterval(object):

   def __init__(self, quality, interval):
      if quality in self._acceptable_qualities:
         self._quality = quality
      else:
         raise ValueError(
            'quality must be in %s' % self._acceptable_qualities)
      if isinstance(interval, int):
         if int == 0:
            raise ValueError
         self._interval = interval
      else:
         raise ValueError('interval must be integer.')

   ## OVERLOADS ##

   def __repr__(self):
      direction_string = self._direction_string
      if direction_string:
         return '%s(%s %s %s)' % (self.__class__.__name__, 
            self._direction_string, self._quality, self._interval_string)
      else:
         return '%s(%s %s)' % (self.__class__.__name__,
            self._quality, self._interval_string)
      
   ## PRIVATE ATTRIBUTES ##

   _acceptable_qualities = ('perfect', 'major', 'minor',
      'diminished', 'augmented')

   @property
   def _direction_string(self):
      if abs(self._interval) == 1:
         return None
      elif 1 < self._interval:
         return 'ascending'
      else:
         return 'descending'

   @property
   def _interval_string(self):
      interval_to_string = {1: 'unison', 2: 'second', 3: 'third', 
         4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'octave',
         9: 'ninth', 10: 'tenth', 11: 'eleventh', 12: 'twelth',
         13: 'thirteenth', 14: 'fourteenth', 15: 'fifteenth'}
      return interval_to_string[abs(self._interval)]

   ## PUBLIC ATTRIBUTES ##

   @property
   def semitones(self):
      result = 0
      interval_to_semitones = {
         1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10, 8: 12,
         9: 13, 10: 15, 11: 17, 12: 19, 13: 20, 14: 22, 15: 24}
      result += interval_to_semitones[abs(self._interval)]
      quality_to_semitones = {
         'perfect': 0, 'major': 1, 'minor': 0, 'augmented': 1,
         'diminished': -1}
      result += quality_to_semitones[self._quality]
      if self._interval < 0:
         result *= -1
      return result
