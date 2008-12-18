from abjad import *

def test_cluster_interface_01( ):
   t = Cluster(Note(1, (1, 4)) * 4)
   t.cluster.style = 'ramp'
   t.cluster.padding = 0.1
   assert t.format == "\\makeClusters {\n\t\\once \\override ClusterSpanner #'style = #'ramp\n\t\\once \\override ClusterSpanner #'padding = #0.1\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"
   t.cluster.clear( )
   assert t.format == "\\makeClusters {\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"
   '''
   \makeClusters {
           \once \override ClusterSpanner #'style = #'ramp
           \once \override ClusterSpanner #'padding = #0.1
           cs'4
           cs'4
           cs'4
           cs'4
   }
   '''
