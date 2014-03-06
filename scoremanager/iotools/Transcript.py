# -*- encoding: utf-8 -*-
import datetime
import os
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class Transcript(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from scoremanager import core
        self._configuration = core.ScoreManagerConfiguration()
        self._entries = []
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._start_time = current_time

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        return self.entries.__getitem__(expr)

    ### PRIVATE METHODS ###

    def _append_entry(self, lines, clear_terminal=None):
        from scoremanager import iotools
        entry = iotools.TranscriptEntry(
            lines,
            terminal_was_cleared=clear_terminal,
            )
        self.entries.append(entry)

    def _write(self, transcripts_directory=None):
        if transcripts_directory is None:
            transcripts_directory = \
                self._configuration.transcripts_directory_path
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(transcripts_directory, file_name)
        output = file(file_path, 'w')
        for entry in self.entries:
            line = entry._format()
            output.write(line)
            output.write('\n\n')
        output.close()

    ### PUBLIC PROPERTIES ###

    @property
    def entries(self):
        return self._entries

    @property
    def last_menu_lines(self):
        return self[-2].lines

    @property
    def last_title(self):
        return self.last_menu_lines[0]

    @property
    def signature(self):
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
                result.append(title)
        return result

    @property
    def user_input_entries(self):
        r'''Gets user input entries in transcript.

        Returns list.
        '''
        result = []
        for entry in self:
            if entry.is_user_input:
                result.append(entry)
        return result
