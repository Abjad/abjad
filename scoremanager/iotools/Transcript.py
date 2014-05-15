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
        from scoremanager import core
        self._configuration = core.ScoreManagerConfiguration()
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

    def _append_entry(self, lines):
        from scoremanager import iotools
        entry = iotools.TranscriptEntry(lines)
        self.entries.append(entry)

    def _write(self, transcripts_directory=None):
        if transcripts_directory is None:
            transcripts_directory = \
                self._configuration.transcripts_directory_path
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(transcripts_directory, file_name)
        with file(file_path, 'w') as file_pointer:
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
        lines = []
        for entry in self:
            lines.extend(entry.lines)
        return '\n'.join(lines)

    @property
    def entries(self):
        r'''Gets transcript entries.

        Returns list of transcript entries.
        '''
        return self._entries

    @property
    def first_lines(self):
        r'''Gets transcript first lines.

        Returns list of strings.
        '''
        result = [_[0] for _ in self]
        result = [_ for _ in result if not _ == '']
        return result

    @property
    def input_entries(self):
        r'''Gets user input entries in transcript.

        Returns list.
        '''
        result = []
        for entry in self:
            if entry.is_input:
                result.append(entry)
        return result

    @property
    def last_menu_lines(self):
        r'''Gets last menu lines.

        Returns lines of -3 entry.
        '''
        return self[-2].lines

    @property
    def last_title(self):
        r'''Gets last title.

        Returns line 0 of last menu lines.
        '''
        return self.last_menu_lines[0]

    @property
    def signature(self):
        r'''Gets transcript signature.

        Returns tuple.
        '''
        result = []
        short_transcript = [entry.lines for entry in self.entries]
        result.append(len(short_transcript))
        indices_already_encountered = set([])
        for i in range(len(short_transcript)):
            if i not in indices_already_encountered:
                shared_indices = [i]
                reference_element = short_transcript[i]
                for j, current_element in enumerate(short_transcript):
                    if current_element == reference_element:
                        if i != j:
                            shared_indices.append(j)
                if 1 < len(shared_indices):
                    result.append(tuple(shared_indices))
                indices_already_encountered.update(shared_indices)
        return tuple(result)

    @property
    def start_time(self):
        r'''Gets transcript start time.

        Returns date / time.
        '''
        return self._start_time

    @property
    def system_display_entries(self):
        r'''Gets system display entries in transcript.

        Returns list.
        '''
        result = []
        for entry in self:
            if entry.is_system_display:
                result.append(entry)
        return result

    @property
    def titles(self):
        r'''Gets titles of system display entries in transcript.

        Returns list.
        '''
        result = []
        for entry in self:
            if entry.is_system_display:
                title = entry.title
                if title:
                    result.append(title)
        return result