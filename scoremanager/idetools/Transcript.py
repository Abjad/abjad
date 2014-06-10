# -*- encoding: utf-8 -*-
import datetime
import os
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class Transcript(AbjadObject):
    r'''Transcript.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_entries',
        '_start_time',
        )

    ### INITIALIZER ###

    def __init__(self):
        from scoremanager import idetools
        self._configuration = idetools.Configuration()
        self._entries = []
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._start_time = current_time

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets transcript entry matching `expr`.

        Returns transcript entry.
        '''
        return self.entries.__getitem__(expr)

    ### PRIVATE METHODS ###

    def _append_entry(self, lines, is_menu=False):
        from scoremanager import idetools
        entry = idetools.TranscriptEntry(lines, is_menu=is_menu)
        self.entries.append(entry)

    def _write(self, transcripts_directory=None):
        if transcripts_directory is None:
            transcripts_directory = \
                self._configuration.transcripts_directory
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(transcripts_directory, file_name)
        with open(file_path, 'w') as file_pointer:
            for entry in self.entries:
                line = entry._format()
                file_pointer.write(line)
                file_pointer.write('\n\n')

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Gets all transcript contents joined together as a single string.

        Returns string.
        '''
        return '\n'.join(self.lines)

    @property
    def entries(self):
        r'''Gets transcript entries.

        Returns list of transcript entries.
        '''
        return self._entries

    @property
    def lines(self):
        r'''Gets all transcript lines.

        Returns list.
        '''
        lines = []
        for entry in self:
            lines.extend(entry.lines)
        return lines

    @property
    def start_time(self):
        r'''Gets transcript start time.

        Returns date / time.
        '''
        return self._start_time

    @property
    def titles(self):
        r'''Gets titles of system display entries in transcript.

        Returns list.
        '''
        result = [_.lines[0] for _ in self if _.is_menu]
        return result