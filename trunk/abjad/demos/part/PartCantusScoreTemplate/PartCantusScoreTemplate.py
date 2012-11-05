# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.scoretemplatetools import ScoreTemplate


class PartCantusScoreTemplate(ScoreTemplate):

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):
       
        # make bell voice and staff
        bell_voice = voicetools.Voice(name='Bell Voice')
        bell_staff = stafftools.Staff([bell_voice], name='Bell Staff')
        contexttools.ClefMark('treble')(bell_staff)
        contexttools.InstrumentMark('Campana in La', 'Camp.')(bell_staff)
        contexttools.TempoMark((1, 4), (112, 120))(bell_staff)
        contexttools.TimeSignatureMark((6, 4))(bell_staff)

        # make first violin voice and staff
        first_violin_voice = voicetools.Voice(name='First Violin Voice')
        first_violin_staff = stafftools.Staff([first_violin_voice], name='First Violin Staff')
        contexttools.ClefMark('treble')(first_violin_staff)
        instrumenttools.Violin(
            instrument_name_markup='Violin I', 
            short_instrument_name_markup='Vln. I'
            )(first_violin_staff)
        # contexttools.TempoMark((1, 4), (112, 120))(first_violin_staff)
        # contexttools.TimeSignatureMark((6, 4))(first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = voicetools.Voice(name='Second Violin Voice')
        second_violin_staff = stafftools.Staff([second_violin_voice], name='Second Violin Staff')
        contexttools.ClefMark('treble')(second_violin_staff)
        instrumenttools.Violin(
            instrument_name_markup='Violin II', 
            short_instrument_name_markup='Vln. II'
            )(second_violin_staff)
        # contexttools.TempoMark((1, 4), (112, 120))(second_violin_staff)
        # contexttools.TimeSignatureMark((6, 4))(second_violin_staff)

        # make viola voice and staff
        viola_voice = voicetools.Voice(name='Viola Voice')
        viola_staff = stafftools.Staff([viola_voice], name='Viola Staff')
        contexttools.ClefMark('alto')(viola_staff)
        instrumenttools.Viola()(viola_staff)
        # contexttools.TempoMark((1, 4), (112, 120))(viola_staff)
        # contexttools.TimeSignatureMark((6, 4))(viola_staff)

        # make cello voice and staff
        cello_voice = voicetools.Voice(name='Cello Voice')
        cello_staff = stafftools.Staff([cello_voice], name='Cello Staff')
        contexttools.ClefMark('bass')(cello_staff)
        instrumenttools.Cello()(cello_staff)
        # contexttools.TempoMark((1, 4), (112, 120))(cello_staff)
        # contexttools.TimeSignatureMark((6, 4))(cello_staff)

        # make bass voice and staff
        bass_voice = voicetools.Voice(name='Bass Voice')
        bass_staff = stafftools.Staff([bass_voice], name='Bass Staff')
        contexttools.ClefMark('bass')(bass_staff)
        instrumenttools.Contrabass()(bass_staff)
        # contexttools.TempoMark((1, 4), (112, 120))(bass_staff)
        # contexttools.TimeSignatureMark((6, 4))(bass_staff)

        # make strings staff group
        strings_staff_group = scoretools.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            bass_staff,
            ],
            name='Strings Staff Group',
            )

        # make score
        score = scoretools.Score([
            bell_staff,
            strings_staff_group,
            ],
            name='Pärt Cantus Score'
            )

        # return Pärt Cantus score
        return score

