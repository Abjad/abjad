from abjad.tools.containertools.Container import Container
from abjad.tools.containertools.Cluster._ClusterFormatter import _ClusterFormatter


class Cluster(Container):
    '''.. versionadded:: 1.1

    Abjad model of a tone cluster container::

        abjad> cluster = containertools.Cluster("c'8 d'8 b'8")

    ::

        abjad> cluster
        Cluster(c'8, d'8, b'8)

    ::

        abjad> f(cluster)
        \makeClusters {
            c'8
            d'8
            b'8
        }

    Return cluster object.
    '''

    def __init__(self, music = None, **kwargs):
        Container.__init__(self, music)
        self.is_parallel = False
        self._formatter = _ClusterFormatter(self)
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._summary)
