# -*- coding: utf-8 -*-
import os
import shutil
import tempfile


class Play(object):
    r'''IPython replacement callable for `topleveltools.show()`.

    Integrates audio rendering of Abjad MIDI files into IPython notebooks
    using `fluidsynth`.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_bank',
        '_sound_font',
        )

    ### INITIALIZER ###

    def __init__(self):
        from abjad.tools import ipythontools
        configuration = ipythontools.IPythonConfiguration()
        self._midi_bank = configuration['midi_bank'] or 'gs'
        self._sound_font = configuration['sound_font']

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        '''Render `expr` as Vorbis audio and display it in the IPython notebook
        as an <audio> tag.

        This function requires `fluidsynth` and `ffmpeg` to convert MIDI into
        an audio recording.
        '''
        from abjad.tools import systemtools
        from abjad.tools import topleveltools
        if not systemtools.IOManager.find_executable('fluidsynth'):
            message = 'WARNING: fluidsynth is not available; '
            message += 'cannot render MIDI file to MP3.'
            print(message)
            return
        if not systemtools.IOManager.find_executable('ffmpeg'):
            message = 'WARNING: ffmpeg is not available; '
            message += 'cannot render MIDI file to MP3.'
            print(message)
            return
        assert hasattr(expr, '__illustrate__')
        sound_font = self.sound_font
        if not sound_font:
            message = 'sound_font is not specified, please call '
            message += "'load_sound_font(sound_font, midi_bank)' "
            message += 'to select a sound font.'
            print(message)
        sound_font = sound_font or ''
        temp_directory = tempfile.mkdtemp()
        midi_file_path = os.path.join(temp_directory, 'out.mid')
        result = topleveltools.persist(expr).as_midi(midi_file_path)
        midi_file_path, format_time, render_time = result
        ogg_file_path = os.path.join(temp_directory, 'out.ogg')
        mp3_file_path = os.path.join(temp_directory, 'out.mp3')
        encoded_audio = self._get_ogg_as_base64(
            self.midi_bank,
            midi_file_path,
            ogg_file_path,
            sound_font,
            )
        if encoded_audio is not None:
            encoded_audio = self._get_mp3_as_base64(
                mp3_file_path,
                ogg_file_path,
                )
            if encoded_audio is not None:
                self._display_mp3_audio_tag(encoded_audio)
        shutil.rmtree(temp_directory)

    ### PRIVATE METHODS ###

    def _display_mp3_audio_tag(self, encoded_audio):
        from IPython.core.display import display_html
        audio_tag = '<audio controls type="audio/mpeg" '
        audio_tag += 'src="data:audio/mpeg;base64,{}">'
        audio_tag = audio_tag.format(encoded_audio)
        display_html(audio_tag, raw=True)

    def _display_ogg_audio_tag(self, encoded_audio):
        from IPython.core.display import display_html
        audio_tag = '<audio controls type="audio/ogg" '
        audio_tag += 'src="data:audio/ogg;base64,{}">'
        audio_tag = audio_tag.format(encoded_audio)
        display_html(audio_tag, raw=True)

    def _get_base64_from_file(self, file_name):
        '''Read the base64 representation of a file and encode for HTML.
        '''
        import base64
        import sys
        with open(file_name, 'rb') as file_pointer:
            data = file_pointer.read()
            if sys.version_info[0] == 2:
                return base64.b64encode(data).decode('utf-8')
            return base64.b64encode(data)

    def _get_mp3_as_base64(
        self,
        mp3_file_path,
        ogg_file_path,
        ):
        from abjad.tools import systemtools
        ffmpeg_command = 'ffmpeg -i {} {}'.format(ogg_file_path, mp3_file_path)
        # print(ffmpeg_command)
        result = systemtools.IOManager.spawn_subprocess(ffmpeg_command)
        if result == 0:
            encoded_audio = self._get_base64_from_file(mp3_file_path)
            return encoded_audio
        message = 'ffmpeg failed to render OGG as MP3, result: {}'
        message = message.format(result)
        print(message)
        return None

    def _get_ogg_as_base64(
        self,
        midi_bank,
        midi_file_path,
        ogg_file_path,
        sound_font,
        ):
        from abjad.tools import systemtools
        fluidsynth_command = (
            'fluidsynth',
            '-T oga',
            '-nli',
            '-r 44100',
            '-o synth.midi-bank-select={}'.format(midi_bank),
            '-F',
            ogg_file_path,
            sound_font,
            midi_file_path,
            )
        fluidsynth_command = ' '.join(fluidsynth_command)
        # print(fluidsynth_command)
        result = systemtools.IOManager.spawn_subprocess(fluidsynth_command)
        if result == 0:
            encoded_audio = self._get_base64_from_file(ogg_file_path)
            return encoded_audio
        message = 'fluidsynth failed to render MIDI as OGG, result: {}'
        message = message.format(result)
        # print(message)
        return None

    ### PUBLIC METHODS ###

    def load_sound_font(self, new_sound_font, new_midi_bank):
        '''Save location of argument sound_font and its type.

        Type can be either 'gs', 'gm', 'xg', or 'mma'.
        '''
        new_sound_font = os.path.expanduser(new_sound_font)
        if os.path.isfile(new_sound_font):
            self._sound_font = new_sound_font
        else:
            message = 'The specified sound_font {} (relative to {}) '
            message += 'is either inaccessible or does not exist.'
            message = message.format(new_sound_font, os.getcwd())
            print(message)
        valid_midi_banks = ('gs', 'gm', 'xg', 'mma')
        if new_midi_bank in valid_midi_banks:
            self._midi_bank = new_midi_bank
        else:
            message = 'The MIDI bank must be either be one of {!s}'
            message = message.format(valid_midi_banks)
            print(message)

    ### PUBLIC PROPERTIES ###

    @property
    def midi_bank(self):
        r'''Gets midi bank name.

        Returns string.
        '''
        return self._midi_bank

    @property
    def sound_font(self):
        r'''Gets sound font path.

        Returns string.
        '''
        return self._sound_font