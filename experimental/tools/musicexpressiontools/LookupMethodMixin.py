# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LookupMethodMixin(AbjadObject):
    r'''Lookup method mixin.

    Definitions for examples:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that should implement the lookup interface.
    '''

    ### PUBLIC METHODS ###

    def look_up_division_set_expression(self, voice):
        r'''Look up division set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = \
            ...     red_segment.timespan.start_offset.look_up_division_set_expression(
            ...     'Voice 1')

        ::

            >>> print format(lookup)
            musicexpressiontools.DivisionSetExpressionLookupExpression(
                offset=musicexpressiontools.OffsetExpression(
                    anchor=musicexpressiontools.TimespanExpression(
                        anchor='red',
                        callbacks=musicexpressiontools.CallbackInventory(
                            []
                            ),
                        ),
                    callbacks=musicexpressiontools.CallbackInventory(
                        []
                        ),
                    ),
                voice_name='Voice 1',
                callbacks=musicexpressiontools.CallbackInventory(
                    []
                    ),
                )

        Returns lookup expression.
        '''
        from experimental.tools import musicexpressiontools
        lookup = \
            musicexpressiontools.DivisionSetExpressionLookupExpression(
            offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_rhythm_set_expression(self, voice):
        r'''Look up rhythm set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = \
            ...     red_segment.timespan.start_offset.look_up_rhythm_set_expression(
            ...     'Voice 1')

        ::

            >>> print format(lookup)
            musicexpressiontools.RhythmSetExpressionLookupExpression(
                offset=musicexpressiontools.OffsetExpression(
                    anchor=musicexpressiontools.TimespanExpression(
                        anchor='red',
                        callbacks=musicexpressiontools.CallbackInventory(
                            []
                            ),
                        ),
                    callbacks=musicexpressiontools.CallbackInventory(
                        []
                        ),
                    ),
                voice_name='Voice 1',
                callbacks=musicexpressiontools.CallbackInventory(
                    []
                    ),
                )

        Returns lookup expression.
        '''
        from experimental.tools import musicexpressiontools
        lookup = musicexpressiontools.RhythmSetExpressionLookupExpression(
            offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_time_signature_set_expression(self, voice):
        r'''Look up time signature set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = \
            ...     red_segment.timespan.start_offset.look_up_time_signature_set_expression(
            ...     'Voice 1')

        ::

            >>> print format(lookup)
            musicexpressiontools.TimeSignatureSetExpressionLookupExpression(
                offset=musicexpressiontools.OffsetExpression(
                    anchor=musicexpressiontools.TimespanExpression(
                        anchor='red',
                        callbacks=musicexpressiontools.CallbackInventory(
                            []
                            ),
                        ),
                    callbacks=musicexpressiontools.CallbackInventory(
                        []
                        ),
                    ),
                voice_name='Voice 1',
                callbacks=musicexpressiontools.CallbackInventory(
                    []
                    ),
                )

        Returns lookup expression.
        '''
        from experimental.tools import musicexpressiontools
        lookup = \
            musicexpressiontools.TimeSignatureSetExpressionLookupExpression(
            offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup