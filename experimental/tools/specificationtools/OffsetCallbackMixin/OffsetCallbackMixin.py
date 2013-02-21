from abjad.tools import durationtools
from experimental.tools.specificationtools.CallbackMixin import CallbackMixin


class OffsetCallbackMixin(CallbackMixin):
    '''Offset callback mixin.

    Score for examples:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> set_expression = red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])

    ::

        >>> offset = red_segment.timespan.stop_offset

    ::

        >>> z(offset)
        specificationtools.OffsetExpression(
            anchor=specificationtools.TimespanExpression(
                anchor='red'
                ),
            edge=Right
            )

    Add to classes that should implement offset callbacks.
    '''

    ### PRIVATE METHODS ###

    def _apply_callbacks(self, offset):
        assert isinstance(offset, durationtools.Offset), repr(offset)
        evaluation_context = {
            'self': self,
            'Duration': durationtools.Duration,
            'Multiplier': durationtools.Multiplier,
            'Offset': durationtools.Offset,
            }
        for callback in self.callbacks:
            callback = callback.replace('offset', repr(offset))
            offset = eval(callback, evaluation_context)
        return offset

    def _scale(self, offset, multiplier):
        assert 0 <= multiplier
        offset *= multiplier
        return offset

    def _translate(self, offset, translation):
        offset += translation
        return offset

    ### PUBLIC METHODS ###

    def scale(self, multiplier):
        '''Scale offset expression by `multiplier`.

        ::

            >>> result = offset.scale(Multiplier(4, 5))

        ::

            >>> z(result)
            specificationtools.OffsetExpression(
                anchor=specificationtools.TimespanExpression(
                    anchor='red'
                    ),
                edge=Right,
                callbacks=specificationtools.CallbackInventory([
                    'self._scale(offset, Multiplier(4, 5))'
                    ])
                )

        Return offset expression copy with callback.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        callback = 'self._scale(offset, {!r})'
        callback = callback.format(multiplier)
        return self._copy_and_append_callback(callback)

    def translate(self, translation):
        '''Translate offset expression by `translation`.

        ::

            >>> result = offset.translate(Duration(9, 2))

        ::

            >>> z(result)
            specificationtools.OffsetExpression(
                anchor=specificationtools.TimespanExpression(
                    anchor='red'
                    ),
                edge=Right,
                callbacks=specificationtools.CallbackInventory([
                    'self._translate(offset, Duration(9, 2))'
                    ])
                )

        Return offset expression copy with callback.
        '''
        translation = durationtools.Duration(translation)
        callback = 'self._translate(offset, {!r})'
        callback = callback.format(translation)
        return self._copy_and_append_callback(callback)
