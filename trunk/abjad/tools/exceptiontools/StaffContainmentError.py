# -*- encoding: utf-8 -*-
class StaffContainmentError(Exception):
    r'''Staves must not contain staff groups, scores or other staves.
    '''
    pass
