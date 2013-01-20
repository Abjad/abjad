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

            >>> request = red_segment.timespan.start_offset.look_up_division_setting('Voice 1')

        ::

            >>> z(request)
            settingtools.DivisionSettingLookup(
                voice_name='Voice 1',
                offset=settingtools.OffsetExpression(
                    anchor=settingtools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return command request.        
        '''
        from experimental.tools import settingtools
        return settingtools.DivisionSettingLookup(voice, offset=self)

    def look_up_rhythm_setting(self, voice):
        r'''PayloadCallbackMixin voice ``1`` rhythm command 
        active at start of segment ``'red'``::

            >>> request = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')

        ::

            >>> z(request)
            settingtools.RhythmSettingLookup(
                voice_name='Voice 1',
                offset=settingtools.OffsetExpression(
                    anchor=settingtools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return command request.        
        '''
        from experimental.tools import settingtools
        return settingtools.RhythmSettingLookup(voice, offset=self)

    def look_up_time_signature_setting(self, voice):
        r'''PayloadCallbackMixin voice ``1`` time signature command
        active at start of segment ``'red'``::

            >>> request = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')

        ::

            >>> z(request)
            settingtools.TimeSignatureSettingLookup(
                voice_name='Voice 1',
                offset=settingtools.OffsetExpression(
                    anchor=settingtools.TimespanExpression(
                        anchor='red'
                        )
                    )
                )

        Return command request.
        '''
        from experimental.tools import settingtools
        return settingtools.TimeSignatureSettingLookup(voice, offset=self)
