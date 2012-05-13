from abjad.tools.containertools.Container import Container


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

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Container.__init__(self, music)
        self.is_parallel = False
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._summary)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def format(self):
        from abjad.tools.containertools._format_cluster import _format_cluster
        self._update_marks_of_entire_score_tree_if_necessary()
        return _format_cluster(self)
