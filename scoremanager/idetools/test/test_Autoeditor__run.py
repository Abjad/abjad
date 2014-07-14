# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools
import scoremanager


def test_Autoeditor__run_01():
    r'''Edits clef name.
    '''

    target = Clef('alto')
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm tenor done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Clef('tenor')


def test_Autoeditor__run_02():
    r'''Creates default tempo.
    '''

    target = Tempo()
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target is target


def test_Autoeditor__run_03():
    r'''Edits tempo duration with pair.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration (1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)


def test_Autoeditor__run_04():
    r'''Edits tempo duration with duration object.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration Duration(1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)


def test_Autoeditor__run_05():
    r'''Edits markup contents.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Markup(),
        )
    input_ = 'arg foo~text done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    markup = markuptools.Markup('foo text')
    assert autoeditor.target == markup


def test_Autoeditor__run_06():
    r'''Edits markup contents and direction.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Markup(),
        )
    input_ = '''arg '"foo~text~here"' dir up done'''
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Markup('"foo text here"', direction=Up)


def test_Autoeditor__run_07():
    r'''Edits markup contents and direction.
    '''

    target = Markup('foo bar')
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'arg entirely~new~text direction up done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Markup('entirely new text', direction=Up)


def test_Autoeditor__run_08():
    r'''Edits mapping component source and target.
    '''

    target = pitchtools.OctaveTranspositionMappingComponent()
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'source [A0, C8] target -18 q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
    assert autoeditor.target == component


def test_Autoeditor__run_09():
    r'''Edits pitch range.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = pitchtools.PitchRange()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = '1 [F#3, C5) q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == pitchtools.PitchRange('[F#3, C5)')

    session = scoremanager.idetools.Session(is_test=True)
    target = pitchtools.PitchRange()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = '1 (A0, C8] q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == pitchtools.PitchRange('(A0, C8]')


def test_Autoeditor__run_10():
    r'''Edits hairpin handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.NoteAndChordHairpinHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "('p', '<', 'f') Duration(1, 8) done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.NoteAndChordHairpinHandler(
        hairpin_token=('p', '<', 'f'),
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_11():
    r'''Edits hairpins handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.NoteAndChordHairpinsHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "[('p', '<', 'f')] Duration(1, 8) done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.NoteAndChordHairpinsHandler(
        hairpin_tokens=[('p', '<', 'f')],
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_12():
    r'''Edits patterned articulations handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = handlertools.PatternedArticulationsHandler()
    session._autoadvance_depth = 1
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "[['.', '^'], ['.']] (1, 16) (1, 8) cs'' c''' done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.PatternedArticulationsHandler(
        articulation_lists=[['.', '^'], ['.']],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_13():
    r'''Edits reiterated articulation handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    session._is_autostarting = True
    target = handlertools.ReiteratedArticulationHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['.', '^'] (1, 16) (1, 8) cs'' c''' done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_14():
    r'''Edits reiterated articulation handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    session._is_autostarting = True
    target = handlertools.ReiteratedArticulationHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['.', '^'] None None None None done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_15():
    r'''Edits reiterated dynamic handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.ReiteratedDynamicHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target
        )
    input_ = 'f Duration(1, 8) q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_16():
    r'''Edits terraced dynamics handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.TerracedDynamicsHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['p', 'f', 'f'] Duration(1, 8) q"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.TerracedDynamicsHandler(
        dynamics=['p', 'f', 'f'],
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler


def test_Autoeditor__run_17():
    r'''Edits talea rhythm-maker.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = rhythmmakertools.TaleaRhythmMaker()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 't c (-1, 2, -3, 4) d 16 done sd/ (6,) (2, 3)/ done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        split_divisions_by_counts=(6,),
        extra_counts_per_division=(2, 3),
        )

    assert autoeditor.target == maker


def test_Autoeditor__run_18():
    r'''Adds instruments to performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Piccolo(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer


def test_Autoeditor__run_19():
    r'''Removes instruments from performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo rm piccolo done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer


def test_Autoeditor__run_20():
    r'''Moves instruments in performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo mv 1 2 done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Piccolo(),
        instrumenttools.Flute(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer


def test_Autoeditor__run_21():
    r'''Lone bang doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da ! q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '!'." in contents


def test_Autoeditor__run_22():
    r'''Double bang doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da !! q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '!!'." in contents


def test_Autoeditor__run_23():
    r'''Lone question mark doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da ? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '?'." in contents


def test_Autoeditor__run_24():
    r'''Double question mark doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '??'." in contents


def test_Autoeditor__run_25():
    r'''Bang-suffixed done doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da done! q'
    ide._run(input_=input_)