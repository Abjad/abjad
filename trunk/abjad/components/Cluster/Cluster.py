from abjad.components.Container import Container
from abjad.components.Cluster._ClusterFormatter import _ClusterFormatter
#from abjad.interfaces import ClusterInterface


class Cluster(Container):

   def __init__(self, music = None, **kwargs):
      Container.__init__(self, music)
      self.parallel = False
      self._formatter = _ClusterFormatter(self)
      #self._cluster = ClusterInterface(self)
      self._initialize_keyword_values(**kwargs)
   
   ## OVERLOADS ##

   def __repr__(self):
      return 'Cluster(%s)' % self._summary
   
   ## PUBLIC ATTRIBUTES ##

#   @property
#   def cluster(self):
#      return self._cluster
