import initializers

class PitchInitializer(object):
   
   def __init__(self): 
      self.initializers = [ ]
      for value in initializers.__dict__.itervalues( ):
         if hasattr(value, 'matchSignature'):
            self.initializers.append(value( ))

   def initialize(self, client, *args):
      for i in self.initializers:
         if i.matchSignature(*args):
            i.initialize(client, *args)
            return True
      print 'Can not initialize Pitch( ).'
      raise ValueError
