from abjad.tools.abctools.AbjadObject import AbjadObject


class LookupMethodMixin(AbjadObject):
    '''Lookup method mixin.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that should implement the lookup interface.
    '''
    
    ### PUBLIC METHODS ###

    def look_up_division_setting(self, voice):
        r'''Look up voice ``1`` division command
        active at start of segment ``'red'``::

            >>> lookup = red_segment.timespan.start_offset.look_up_division_setting('Voice 1')

        ::

            >>> z(lookup)
            expressiontools.SetDivisionLookupExpression(
                voice_name='Voice 1',
                offset=expressiontools.OffsetExpression(
                    anchor=expressiontools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return lookup expression.        
        '''
        from experimental.tools import expressiontools
        lookup = expressiontools.SetDivisionLookupExpression(voice, offset=self)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_rhythm_setting(self, voice):
        r'''StartPositionedPayloadCallbackMixin voice ``1`` rhythm command 
        active at start of segment ``'red'``::

            >>> lookup = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')

        ::

            >>> z(lookup)
            expressiontools.SetRhythmLookupExpression(
                voice_name='Voice 1',
                offset=expressiontools.OffsetExpression(
                    anchor=expressiontools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return lookup expression.        
        '''
        from experimental.tools import expressiontools
        lookup = expressiontools.SetRhythmLookupExpression(voice, offset=self)
        lookup._score_specification = self.score_specification
        return lookup

    def look_up_time_signature_setting(self, voice):
        r'''StartPositionedPayloadCallbackMixin voice ``1`` time signature command
        active at start of segment ``'red'``::

            >>> lookup = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')

        ::

            >>> z(lookup)
            expressiontools.SetTimeSignatureLookupExpression(
                voice_name='Voice 1',
                offset=expressiontools.OffsetExpression(
                    anchor=expressiontools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return lookup expression.
        '''
        from experimental.tools import expressiontools
        lookup = expressiontools.SetTimeSignatureLookupExpression(voice, offset=self)
        lookup._score_specification = self.score_specification
        return lookup
