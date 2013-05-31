from abjad import *
from experimental.tools.scoremanagertools import specifiers


green_music_specifier = specifiers.MusicSpecifier([specifiers.MusicContributionSpecifier([specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],description='upper register violin pizzicati', name='green violin pizzicati')],name='green music')