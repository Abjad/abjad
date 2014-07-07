# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ListAutoeditor_edit_item_01():
    r'''Passes silently when list item is a string or number.
    Raises no exceptions.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = [17, 99, 'foo']
    autoeditor = scoremanager.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = '1 2 3 q'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    contents = autoeditor._transcript.contents

    assert 'List (EDIT)' in contents