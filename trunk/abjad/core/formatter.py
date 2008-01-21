class _Formatter(object):

   def __init__(self, client):
      self._client = client
      self.number = False
      self.variable = None
      self.before = [ ]
      self.after = [ ]
      self.opening = [ ]
      self.closing = [ ]
      self.left = [ ]
      self.right = [ ]
   
   def __repr__(self):
      return '%s( )' % self.__class__.__name__
