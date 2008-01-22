import cPickle


def dump_pickle(data, file_name):
   f = open(file_name, 'w')
   cPickle.dump(data, f)
   f.close()
      

def load_pickle(file_name):
   f = open(file_name, 'r')
   data = cPickle.load(f)
   f.close()
   return data
