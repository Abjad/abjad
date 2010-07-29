from abjad import *
import os


def test_persistencetools_dump_pickle_01( ):
   '''Pickling should work.
   That is, the code here should raise no exception.'''
   
   t = Note(0, (1, 4))
   file_name = '__test_pickle_01'
   persistencetools.dump_pickle(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)


def test_persistencetools_dump_pickle_02( ):
  
   t = Staff(macros.scale(4))
   file_name = '__test_pickle_02'
   persistencetools.dump_pickle(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)
