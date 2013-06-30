from abjad.tools.containertools.Container import Container


class Cluster(Container):
    '''.. versionadded:: 1.1

    Abjad model of a tone cluster container:

    ::

        >>> cluster = containertools.Cluster("c'8 <d' g'>8 b'8")

    ::

        >>> cluster
        Cluster(c'8, <d' g'>8, b'8)

    ::

        >>> f(cluster)
        \makeClusters {
            c'8
            <d' g'>8
            b'8
        }

    ::

        >>> show(cluster) # doctest: +SKIP

    Return cluster object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Container.__init__(self, music)
        self.is_parallel = False
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._summary)

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, format_contributions):
        result = []
        contributor = ('self_brackets', 'open')
        if self.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        contributions = [r'\makeClusters %s' % brackets_open[0]]
        result.append([contributor, contributions])
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()
