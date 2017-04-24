# -*- coding: utf-8 -*-
import abjad


class ScoreTemplate(abjad.abctools.AbjadObject):
    r'''Score template.
    '''

    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''
        voice = abjad.Voice(name='Example Voice')
        staff = abjad.Staff([voice], name='Example Staff')
        score = abjad.Score([staff], name='Example Score')
        return score
