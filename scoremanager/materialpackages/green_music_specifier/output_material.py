# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import specifiers


green_music_specifier = specifiers.MusicSpecifier([specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],description='upper register violin pizzicati', custom_identifier='green violin pizzicati')],custom_identifier='green music')
