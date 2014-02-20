# -*- encoding: utf-8 -*-
import datetime
import os
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class IOTranscript(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from scoremanager import core
        self._configuration = core.ScoreManagerConfiguration()
        self._entries = []
        self._start_time = self.current_time

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        return self.entries.__getitem__(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def configuration(self):
        return self._configuration

    @property
    def current_time(self):
        return datetime.datetime.fromtimestamp(time.time())

    @property
    def entries(self):
        return self._entries

    @property
    def last_menu_lines(self):
        return self[-2][1]

    @property
    def last_menu_title(self):
        return self.last_menu_lines[0]

    @property
    def signature(self):
        result = []
        short_transcript = [entry[1] for entry in self.entries]
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

    ### PUBLIC METHODS ###

    def append_lines(self, lines, clear_terminal=None):
        from scoremanager import iotools
        entry = iotools.IOTranscriptEntry(
            lines,
            terminal_was_cleared=clear_terminal,
            )
        self.entries.append(entry)

    def format_entry(self, entry):
        result = []
        result.append(str(entry.current_time))
        if entry.terminal_was_cleared:
            result.append('clear_terminal=True')
        for line in entry.lines:
            result.append(line)
        return '\n'.join(result)

    def write(self, output_directory=None):
        output_directory = output_directory or \
            self.configuration.transcripts_directory_path
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(output_directory, file_name)
        output = file(file_path, 'w')
        for entry in self.entries:
            output.write(self.format_entry(entry))
            output.write('\n\n')
        output.close()
