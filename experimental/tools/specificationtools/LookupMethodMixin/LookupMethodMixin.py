from abjad.tools.abctools.AbjadObject import AbjadObject


class LookupMethodMixin(AbjadObject):
    '''Lookup method mixin.

    Definitions for examples:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that should implement the lookup interface.
    '''

    ### PUBLIC METHODS ###

    def look_up_division_set_expression(self, voice):
        r'''Look up division set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 1')

        ::

            >>> z(lookup)
            specificationtools.DivisionSetExpressionLookupExpression(
                offset=specificationtools.OffsetExpression(
                    anchor=specificationtools.TimespanExpression(
                        anchor='red'
                        )
                    ),
                voice_name='Voice 1'
                )

        Return lookup expression.
        '''
        from experimental.tools import specificationtools
        lookup = specificationtools.DivisionSetExpressionLookupExpression(offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_rhythm_set_expression(self, voice):
        r'''Look up rhythm set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')

        ::

            >>> z(lookup)
            specificationtools.RhythmSetExpressionLookupExpression(
                offset=specificationtools.OffsetExpression(
                    anchor=specificationtools.TimespanExpression(
                        anchor='red'
                        )
                    ),
                voice_name='Voice 1'
                )

        Return lookup expression.
        '''
        from experimental.tools import specificationtools
        lookup = specificationtools.RhythmSetExpressionLookupExpression(offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_time_signature_set_expression(self, voice):
        r'''Look up time signature set expression active at
        start of segment ``'red'`` in voice ``1``:

        ::

            >>> lookup = red_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')

        ::

            >>> z(lookup)
            specificationtools.TimeSignatureSetExpressionLookupExpression(
                offset=specificationtools.OffsetExpression(
                    anchor=specificationtools.TimespanExpression(
                        anchor='red'
                        )
                    ),
                voice_name='Voice 1'
                )

        Return lookup expression.
        '''
        from experimental.tools import specificationtools
        lookup = specificationtools.TimeSignatureSetExpressionLookupExpression(offset=self, voice_name=voice)
        lookup._score_specification = self.score_specification
        return lookup
