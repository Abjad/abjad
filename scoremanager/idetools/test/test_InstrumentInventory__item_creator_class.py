# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
session = scoremanager.idetools.Session()
inventory = instrumenttools.InstrumentInventory()
item_creator_class = inventory._make_item_creator_class()


def test_InstrumentInventory__item_creator_class_01():

    item_creator = item_creator_class(session=session)
    input_ = 'violin'
    item_creator._session._pending_input = input_
    item_creator._run()
    assert item_creator.target == instrumenttools.Violin()


def test_InstrumentInventory__item_creator_class_02():

    item_creator = item_creator_class(session=session)
    input_ = 'Untuned vibraslap'
    item_creator._session._pending_input = input_
    item_creator._run()
    vibraslap = instrumenttools.UntunedPercussion(
        instrument_name='vibraslap',
        short_instrument_name='vibraslap',
        )
    assert item_creator.target == vibraslap


def test_InstrumentInventory__item_creator_class_03():

    item_creator = item_creator_class(is_ranged=True, session=session)
    input_ = 'violin, viola'
    item_creator._session._pending_input = input_
    item_creator._run()
    instruments = [instrumenttools.Violin(), instrumenttools.Viola()]
    assert item_creator.target == instruments


def test_InstrumentInventory__item_creator_class_04():

    item_creator = item_creator_class(is_ranged=True, session=session)
    input_ = 'violin, viola, untuned vibraslap'
    item_creator._session._pending_input = input_
    item_creator._run()
    instruments = [
        instrumenttools.Violin(),
        instrumenttools.Viola(),
        instrumenttools.UntunedPercussion(
            instrument_name='vibraslap',
            short_instrument_name='vibraslap',
            ),
        ]
    assert item_creator.target == instruments


def test_InstrumentInventory__item_creator_class_05():
    r'''Back doesn't cause anything to blow up.
    '''

    input_ = 'red~example~score m instrumentation da hornist i add b q'

    material_package = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'instrumentation',
        )

    with systemtools.FilesystemState(keep=[material_package]):
        ide._run(input_=input_)