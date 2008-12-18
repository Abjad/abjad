from abjad import *


def test_cluster_01( ):
   '''Cluster can be empty.'''
   t = Cluster([ ])
   assert t.brackets == 'curly'
   assert len(t) == 0
   assert t.format == '\\makeClusters {\n}'
   

def test_cluster_02( ):
   t = Cluster(Note(1, (1, 4)) * 4)
   assert isinstance(t, Cluster)
   assert t.brackets == 'curly'
   assert len(t) == 4
   assert t.format == "\\makeClusters {\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"
