# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class Cluster(Container):
    '''A cluster.

    ::

        >>> cluster = scoretools.Cluster("c'8 <d' g'>8 b'8")
        >>> show(cluster) # doctest: +SKIP

    ..  doctest::

        >>> print format(cluster)
        \makeClusters {
            c'8
            <d' g'>8
            b'8
        }

    ::

        >>> cluster
        Cluster(c'8, <d' g'>8, b'8)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(self, music=None):
        Container.__init__(self, music)
        self.is_simultaneous = False

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of cluster.

        ::

            >>> cluster
            Cluster(c'8, <d' g'>8, b'8)

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, self._summary)

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        result = []
        contributor = ('self_brackets', 'open')
        if self.is_simultaneous:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        contributions = [r'\makeClusters {}'.format(brackets_open[0])]
        result.append([contributor, contributions])
        return tuple(result)

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()
