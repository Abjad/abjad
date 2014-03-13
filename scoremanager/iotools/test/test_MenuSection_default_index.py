# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MenuSection_default_index_01():

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test', title='section')
    section.append('apple')
    section.append('banana')
    section.append('cherry')

    assert section.default_index is None


def test_MenuSection_default_index_02():

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(
        name='test', 
        title='section',
        default_index=2,
        )
    section.append('apple')
    section.append('banana')
    section.append('cherry')

    assert section.default_index == 2
