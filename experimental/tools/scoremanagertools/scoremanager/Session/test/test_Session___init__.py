from experimental import *


def test_Session___init___01():
    '''Attributes assigned at initialization time.
    '''

    session = scoremanagertools.scoremanager.Session()

    assert session.initial_user_input is None
    assert session._breadcrumb_stack == []
    assert session.scores_to_show == 'active'
    assert session.pending_user_input is None
