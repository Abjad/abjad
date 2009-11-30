from abjad import *


def test_pickle_dump_01( ):
   '''Pickling should work.
   That is, the code here should raise no exception.'''
   
   t = Note(0, (1, 4))
   file_name = '__test_pickle_01'
   pickle.dump(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)


def test_pickle_dump_02( ):
  
   t = Staff(construct.scale(4))
   file_name = '__test_pickle_02'
   pickle.dump(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)
