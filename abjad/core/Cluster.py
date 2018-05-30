from .Container import Container


class Cluster(Container):
    """
    Cluster.

    ..  container:: example

        >>> cluster = abjad.Cluster("c'8 <d' g'>8 b'8")
        >>> abjad.show(cluster) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(cluster)
            \makeClusters {
                c'8
                <d' g'>8
                b'8
            }

        >>> cluster
        Cluster("c'8 <d' g'>8 b'8")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = ()

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

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()
