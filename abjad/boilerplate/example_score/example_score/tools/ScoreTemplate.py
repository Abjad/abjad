# -*- coding: utf-8 -*-
from abjad import Score, Staff, Voice
from abjad.tools import abctools


class ScoreTemplate(abctools.AbjadObject):

    def __call__(self):
        voice = Voice(name='Example Voice')
        staff = Staff([voice], name='Example Staff')
        score = Score([staff], name='Example Score')
        return score
