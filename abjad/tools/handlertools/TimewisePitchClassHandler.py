# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.handlertools.Handler import Handler


class TimewisePitchClassHandler(Handler):
    r'''Timewise pitch-class handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_pitch_class_server',
        )

    ### INITIALIZER ###

    def __init__(self, pitch_class_server=None):
        self._pitch_class_server = pitch_class_server

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        classes = (scoretools.Note, scoretools.Chord)
        for leaf in \
            scoretools.iterate_components_forward_in_expr(expr, classes):
            if isinstance(leaf, scoretools.Note):
                pitch_class = \
                    self.pitch_class_server.get_next_n_nodes_at_level(1, -1)
                leaf.written_pitch = pitch_class
            elif isinstance(leaf, scoretools.Chord):
                pitch_classes = \
                    self.pitch_class_server.get_next_n_nodes_at_level(
                        len(leaf), -1)
                leaf.clear()
                leaf.extend(pitch_classes)
            else:
                raise ValueError

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_class_server(self):
        r'''Gets pitch-class server of handler.

        Returns pitch-class server or none.
        '''
        return self._pitch_class_server