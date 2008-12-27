from abjad import *


def test_cluster_interface_01( ):
   '''
   Clusters handle grob overrides.
   '''

   t = Cluster(Note(1, (1, 4)) * 4)
   t.cluster.style = 'ramp'
   t.cluster.padding = 0.1

   r'''
   \makeClusters {
      \override ClusterSpanner #'style = #'ramp
      \override ClusterSpanner #'padding = #0.1
      cs'4
      cs'4
      cs'4
      cs'4
      \revert ClusterSpanner #'style
      \revert ClusterSpanner #'padding
   }
   '''

   assert t.format == "\\makeClusters {\n\t\\override ClusterSpanner #'style = #'ramp\n\t\\override ClusterSpanner #'padding = #0.1\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n\t\\revert ClusterSpanner #'style\n\t\\revert ClusterSpanner #'padding\n}"

   t.cluster.clear( )

   r'''
   \makeClusters {
      cs'4
      cs'4
      cs'4
      cs'4
   }
   '''

   assert t.format == "\\makeClusters {\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"
