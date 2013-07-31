# -*- encoding: utf-8 -*-
class SpannerPopulationError(Exception):
    r'''Spanner contents incorrect.

    Spanner may be missing component it is assumed to have.

    Spanner may have a component it is assumed not to have.
    '''
    pass
