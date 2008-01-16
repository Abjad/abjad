class Comments(list):
   
   def __init__(self):
      self.before = [ ]
      self.after = [ ]
      self.right = [ ]

   def __repr__(self):
      if len(self):
         return 'Comments(%s)' % ', '.join(self)
      else:
         return 'Comments( )'

   @property
   def _before(self):
      result = [ ]
      result.extend(['% ' + x for x in self.before])
      result.extend(['% ' + x for x in self])
      return result

   @property
   def _after(self):
      result = [ ]
      result.extend(['% ' + x for x in self.after])
      return result

   @property
   def _right(self):
      result = [ ]
      result.extend(['% ' + x for x in self.right])
      return result
