# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_MenuSection_default_index_01():

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section',
        )

    assert section.default_index is None


def test_MenuSection_default_index_02():

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        default_index=2,
        menu_entries=commands,
        name='test',
        title='section',
        )

    assert section.default_index == 2