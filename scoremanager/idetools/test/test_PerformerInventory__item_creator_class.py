# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
inventory = instrumenttools.PerformerInventory
item_creator_class = inventory._make_item_creator_class()


def test_PerformerInventory__item_creator_class_01():

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(session=session)
    item_creator._session._pending_input = 'q'
    assert item_creator._run() is None

    item_creator = item_creator_class(session=session)
    item_creator._session._pending_input = 'b'
    assert item_creator._run() is None

    item_creator = item_creator_class(session=session)
    item_creator._session._pending_input = 'ss'
    assert item_creator._run() is None


def test_PerformerInventory__item_creator_class_02():

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(session=session)
    input_ = 'vn <return>'
    item_creator._session._pending_input = input_
    assert item_creator._run() == instrumenttools.Performer(
        name='violinist',
        instruments=[instrumenttools.Violin()],
        )


def test_PerformerInventory__item_creator_class_03():
    r'''Ranged.
    '''

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va <return> <return>'
    item_creator._session._pending_input = input_
    assert item_creator._run() == [
        instrumenttools.Performer(
            name='violinist',
            instruments=[instrumenttools.Violin()],
            ),
        instrumenttools.Performer(
            name='violist',
            instruments=[instrumenttools.Viola()],
            ),
        ]


def test_PerformerInventory__item_creator_class_04():
    r'''Skipping instruments.
    '''

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va skip skip'
    item_creator._session._pending_input = input_
    assert item_creator._run() == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist'),
        ]


def test_PerformerInventory__item_creator_class_05():
    r'''More instruments.
    '''

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va skip more xyl'
    item_creator._session._pending_input = input_
    assert item_creator._run() == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(
            name='violist',
            instruments=[instrumenttools.Xylophone()]
            ),
        ]


def test_PerformerInventory__item_creator_class_06():
    r'''Auxiliary percussion.
    '''

    session = scoremanager.idetools.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    caxixi = instrumenttools.UntunedPercussion(
        instrument_name='caxixi',
        short_instrument_name='caxixi',
        )
    input_ = 'vn more untuned cax'
    item_creator._session._pending_input = input_
    item_creator._run()
    assert item_creator.target == [
        instrumenttools.Performer(
            name='violinist',
            instruments=[caxixi],
            ),
        ]