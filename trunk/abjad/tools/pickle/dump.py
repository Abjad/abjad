import cPickle


def dump(data, file_name):
   f = open(file_name, 'w')
   cPickle.dump(data, f)
   f.close( )
