# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
inventory = instrumenttools.PerformerInventory
item_creator_class = inventory._make_item_creator_class()


def test_PerformerInventory__item_creator_class_01():

    session = scoremanager.core.Session()
    item_creator = item_creator_class(session=session)
    input_ = 'q'
    assert item_creator._run(input_=input_) is None

    item_creator = item_creator_class(session=session)
    input_ = 'b'
    assert item_creator._run(input_=input_) is None

    item_creator = item_creator_class(session=session)
    input_ = 'h'
    assert item_creator._run(input_=input_) is None


def test_PerformerInventory__item_creator_class_02():

    session = scoremanager.core.Session()
    item_creator = item_creator_class(session=session)
    input_ = 'vn <return>'
    assert item_creator._run(input_=input_) == \
        instrumenttools.Performer(
            name='violinist',
            instruments=[instrumenttools.Violin()],
            )


def test_PerformerInventory__item_creator_class_03():
    r'''Ranged.
    '''

    session = scoremanager.core.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va <return> <return>'
    assert item_creator._run(input_=input_) == [
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

    session = scoremanager.core.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va skip skip'
    assert item_creator._run(input_=input_) == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist'),
        ]


def test_PerformerInventory__item_creator_class_05():
    r'''More instruments.
    '''

    session = scoremanager.core.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    input_ = 'vn, va skip more xyl'
    assert item_creator._run(input_=input_) == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(
            name='violist',
            instruments=[instrumenttools.Xylophone()]
            ),
        ]


def test_PerformerInventory__item_creator_class_06():
    r'''Auxiliary percussion.
    '''

    session = scoremanager.core.Session()
    item_creator = item_creator_class(
        is_ranged=True,
        session=session,
        )
    caxixi = instrumenttools.UntunedPercussion(
        instrument_name='caxixi',
        short_instrument_name='caxixi',
        )
    input_ = 'vn more untuned cax'
    item_creator._run(input_=input_)
    assert item_creator.target == [
        instrumenttools.Performer(
            name='violinist',
            instruments=[caxixi],
            ),
        ]