from abjad import *
from experimental.tools.scoremanagertools import specifiers


black_music_specifier = specifiers.MusicSpecifier([specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],description='lower register violin pizzicati', name='black violin pizzicati'), specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Cello())],description='midrange cello pizzicati', name='black cello pizzicati')],name='black music')