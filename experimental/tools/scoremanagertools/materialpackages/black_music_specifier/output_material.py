# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools import specifiers


black_music_specifier = specifiers.MusicSpecifier([specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],description='lower register violin pizzicati', custom_identifier='black violin pizzicati'), specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Cello())],description='midrange cello pizzicati', custom_identifier='black cello pizzicati')],name='black music')
