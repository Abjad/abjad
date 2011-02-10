from abjad import *


def test_Cluster___init___01( ):
   '''Cluster can be empty.'''
   t = chordtools.Cluster([ ])
   assert not t.is_parallel
   assert len(t) == 0
   assert t.format == '\\makeClusters {\n}'
   

def test_Cluster___init___02( ):
   t = chordtools.Cluster(Note(1, (1, 4)) * 4)
   assert isinstance(t, chordtools.Cluster)
   assert not t.is_parallel
   assert len(t) == 4
   assert t.format == "\\makeClusters {\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"
