import datetime
import os
import pprint
import time


class Transcript(object):

    def __init__(self):
        self._entries = []
        self._start_time = self.current_time

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def current_time(self):
        return datetime.datetime.fromtimestamp(time.time())

    @property
    def entries(self):
        return self._entries

    @property
    def short_transcript(self):
        return [entry[1] for entry in self.entries]

    @property
    def signature(self):
        result = []
        result.append(len(self.short_transcript))
        indices_already_encountered = set([])
        for i in range(len(self.short_transcript)):
            if i not in indices_already_encountered:
                shared_indices = [i]
                reference_element = self.short_transcript[i]
                for j, current_element in enumerate(self.short_transcript):
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
        assert isinstance(lines, list)
        assert isinstance(clear_terminal, (bool, type(None)))
        entry = []
        entry.append(self.current_time)
        entry.append(lines[:])
        entry.append(clear_terminal)
        self.entries.append(entry)

    def format_entry(self, entry):
        assert len(entry) == 3
        result = []
        result.append(str(entry[0]))
        if entry[2]:
            result.append('clear_terminal=True')
        for line in entry[1]:
            result.append(line)
        return '\n'.join(result)

    def ptc(self):
        tab = '    '
        print tab + 'entry_index = -1'
        for entry in self.short_transcript:
            print ''
            print tab + 'entry_index = entry_index + 1'
            print tab + 'assert transcript[entry_index] == \\'
            for line in pprint.pformat(entry).split('\n'):
                print tab + line

    def write_to_disk(self, output_directory):
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(output_directory, file_name)
        output = file(file_path, 'w')
        for entry in self.entries:
            output.write(self.format_entry(entry))
            output.write('\n\n')
        output.close()
