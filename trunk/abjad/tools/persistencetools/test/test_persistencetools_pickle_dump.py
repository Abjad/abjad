from abjad import *
import os


def test_persistencetools_pickle_dump_01( ):
   '''Pickling should work.
   That is, the code here should raise no exception.'''
   
   t = Note(0, (1, 4))
   file_name = '__test_pickle_01'
   persistencetools.pickle_dump(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)


def test_persistencetools_pickle_dump_02( ):
  
   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   file_name = '__test_pickle_02'
   persistencetools.pickle_dump(t, file_name)
   assert os.stat(file_name)
   os.remove(file_name)
