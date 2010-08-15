class LilyPondContextProxy(object):
   '''.. versionadded:: 1.1.2

   LilyPond context proxy..
   '''

   def __init__(self):
      pass

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__
