class Initializer(object):

   def __init__(self, initializers):
      exec('import %inits.py' % initializers)
      self.initializers = [ ]
      for value in chordinits.__dict__.itervalues( ):
         if hasattr(value, 'matchSignature'):
            self.initializers.append(value( ))

   def initialize(self, client, *args):
      for arg in args:
         for i in self.initializers:
            if i.matchSignature(arg):
               i.initialize(client, arg)
               break
         print 'Can not initialize %s(%s)' % (client.__class__.__name__, arg)
         raise ValueError
