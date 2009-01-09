class Function(object):
   '''Wrapper for names of Scheme functions known to LilyPond.'''

   def __init__(self, name = ''):
      self.name = name
   
   @property
   def format(self):
      return self.name
