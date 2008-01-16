class Initializer(object):

   def __init__(self, initializers):
      exec('import %sinits as initfile' % initializers)
      self.initializers = [ ]
      for value in initfile.__dict__.itervalues( ):
         if hasattr(value, 'matchSignature'):
            self.initializers.append(value( ))

   def initialize(self, client, *args):
      for arg in args:
         initialized = False
         for i in self.initializers:
            if i.matchSignature(arg):
               i.initialize(client, arg)
               initialized = True
         if not initialized:
            print 'Can not initialize %s(%s)' % (client.__class__.__name__, arg)
            raise ValueError
