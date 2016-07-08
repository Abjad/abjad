# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import sys
import tempfile


class Play(object):
    r'''IPython replacement callable for `topleveltools.show()`.

    Integrates audio rendering of Abjad MIDI files into IPython notebooks
    using `timidity`.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        '''Render `expr` as audio and display it in the IPython notebook
        as an <audio> tag.
        '''
        from abjad.tools import systemtools
        from abjad.tools import topleveltools
        assert hasattr(expr, '__illustrate__')
        assert systemtools.IOManager.find_executable('lilypond')
        assert systemtools.IOManager.find_executable('timidity')
        has_vorbis = self._check_for_vorbis()
        temp_directory = tempfile.mkdtemp()
        midi_file_path = os.path.join(temp_directory, 'out.midi')
        result = topleveltools.persist(expr).as_midi(midi_file_path)
        midi_file_path, format_time, render_time = result
        if has_vorbis:
            audio_file_path = os.path.join(temp_directory, 'out.ogg')
        else:
            audio_file_path = os.path.join(temp_directory, 'out.aif')
        encoded_audio = self._get_audio_as_base64(
            midi_file_path,
            audio_file_path,
            has_vorbis,
            )
        if encoded_audio is not None:
            self._display_audio_tag(encoded_audio, has_vorbis)
        shutil.rmtree(temp_directory)

    ### PRIVATE METHODS ###

    def _display_audio_tag(self, encoded_audio, has_vorbis):
        from IPython.core.display import display_html
        if has_vorbis:
            mime_type = 'audio/ogg'
        else:
            mime_type = 'audio/aiff'
        audio_tag = '<audio controls type="{}" '
        audio_tag += 'src="data:{};base64,{}">'
        audio_tag = audio_tag.format(mime_type, mime_type, encoded_audio)
        display_html(audio_tag, raw=True)

    def _get_audio_as_base64(
        self,
        midi_file_path,
        audio_file_path,
        has_vorbis,
        ):
        if has_vorbis:
            output_flag = '-Ov'
        else:
            output_flag = '-Oa'
        command = 'timidity {midi_file_path} {output_flag} -o {audio_file_path}'.format(
            midi_file_path=midi_file_path,
            output_flag=output_flag,
            audio_file_path=audio_file_path,
            )
        result = subprocess.call(command, shell=True)
        if result == 0:
            encoded_audio = self._get_base64_from_file(audio_file_path)
            return encoded_audio
        message = 'timidity failed to render MIDI, result: {}'
        message = message.format(result)
        print(message)
        return None

    def _get_base64_from_file(self, file_name):
        '''Read the base64 representation of a file and encode for HTML.
        '''
        import base64
        with open(file_name, 'rb') as file_pointer:
            data = file_pointer.read()
            return base64.b64encode(data).decode('utf-8')

    def _check_for_vorbis(self):
        has_vorbis = False
        output = subprocess.check_output('timidity --help', shell=True)
        if sys.version_info[0] == 3:
            output = output.decode('utf-8')
        for line in output.splitlines():
            for part in line.split():
                if part == '-Ov':
                    has_vorbis = True
                    break
        return has_vorbis
