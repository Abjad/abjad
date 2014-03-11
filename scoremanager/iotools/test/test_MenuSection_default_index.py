# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MenuSection_default_index_01():

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test')
    section.title = 'section'
    section.append('apple')
    section.append('banana')
    section.append('cherry')

    assert section.default_index is None
    assert pytest.raises(ValueError, 'section.default_index = -1')
    assert pytest.raises(ValueError, 'section.default_index = 99')

    section.default_index = 2
    assert section.default_index == 2
