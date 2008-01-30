class _Characters(object):

   def __init__(self, contents = None):
      self.contents = contents

   def __repr__(self):
      return '"%s"' % self.contents
