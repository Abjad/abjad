# -*- encoding: utf-8 -*-
from experimental import *


def test_ReiteratedArticulationHandler___format___01():

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        )

    assert testtools.compare(
        format(handler),
        r'''
        handlertools.ReiteratedArticulationHandler(
            articulation_list=['.', '^'],
            minimum_duration=durationtools.Duration(1, 16),
            maximum_duration=durationtools.Duration(1, 8)
            )
        '''
        )
