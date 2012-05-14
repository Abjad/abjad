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

    ### PRIVATE METHODS ###

    def _format_slot_2(self):
        result = []
        contributor = ('self_brackets', 'open')
        if self.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        contributions = [r'\makeClusters %s' % brackets_open[0]]
        result.append([contributor, contributions])
        return tuple(result)
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()
