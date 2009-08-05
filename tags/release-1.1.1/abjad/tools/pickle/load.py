import cPickle


def load(file_name):
   f = open(file_name, 'r')
   data = cPickle.load(f)
   f.close( )
   return data
