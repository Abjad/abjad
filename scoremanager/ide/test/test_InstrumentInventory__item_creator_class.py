# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.ide.Session()
inventory = instrumenttools.InstrumentInventory()
item_creator_class = inventory._make_item_creator_class()


def test_InstrumentInventory__item_creator_class_01():

    item_creator = item_creator_class(session=session)
    input_ = 'violin'
    item_creator._run(input_=input_)
    assert item_creator.target == instrumenttools.Violin()


def test_InstrumentInventory__item_creator_class_02():

    item_creator = item_creator_class(session=session)
    input_ = 'untuned vibraslap'
    item_creator._run(input_=input_)
    vibraslap = instrumenttools.UntunedPercussion(
        instrument_name='vibraslap',
        short_instrument_name='vibraslap',
        )
    assert item_creator.target == vibraslap


def test_InstrumentInventory__item_creator_class_03():

    item_creator = item_creator_class(is_ranged=True, session=session)
    input_ = 'violin, viola'
    item_creator._run(input_=input_)
    instruments = [instrumenttools.Violin(), instrumenttools.Viola()]
    assert item_creator.target == instruments


def test_InstrumentInventory__item_creator_class_04():

    item_creator = item_creator_class(is_ranged=True, session=session)
    input_ = 'violin, viola, untuned vibraslap'
    item_creator._run(input_=input_)
    instruments = [
        instrumenttools.Violin(),
        instrumenttools.Viola(),
        instrumenttools.UntunedPercussion(
            instrument_name='vibraslap',
            short_instrument_name='vibraslap',
            ),
        ]
    assert item_creator.target == instruments