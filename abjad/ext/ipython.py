# -*- coding: utf-8 -*-
'''
Abjad-IPython Extension
-----------------------

Integrates audio and visual rendering of Abjad scores in IPython notebooks.

This extension requires `fluidsynth` be in your $PATH. If you do not have
`fluidsynth` installed, it is likely available in your platform's package
manager:

OS X
    $ brew install fluidsynth --with-libsndfile
    $ port install fluidsynth

Linux
    $ apt-get install fluidsynth

'''
import os
import shutil
import tempfile
from IPython.core.display import display_html


class Play(object):
    r'''Integrates audio rendering of Abjad MIDI files into IPython notebooks
    using `fluidsynth`.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_bank',
        '_sound_font',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._midi_bank = 'gs'
        self._sound_font = None

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
            print('fluidsynth is not available.')
        if not systemtools.IOManager.find_executable('ffmpeg'):
            print('ffmpeg is not available.')
        assert '__illustrate__' in dir(expr)
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
        rendered_successfully = self._display_ogg(
            self.midi_bank,
            midi_file_path,
            ogg_file_path,
            sound_font,
            )
        if rendered_successfully:
            self._display_mp3(mp3_file_path, ogg_file_path)
        shutil.rmtree(temp_directory)

    ### PRIVATE METHODS ###

    def _display_mp3(self, mp3_file_path, ogg_file_path):
        from abjad.tools import systemtools
        ffmpeg_command = 'ffmpeg -i {} {}'.format(ogg_file_path, mp3_file_path)
        print(ffmpeg_command)
        result = systemtools.IOManager.spawn_subprocess(ffmpeg_command)
        if result == 0:
            encoded_audio = self._get_base64_from_file(mp3_file_path)
            audio_tag = '<audio controls type="audio/mpeg" '
            audio_tag += 'src="data:audio/mpeg;base64,{}">'
            audio_tag = audio_tag.format(encoded_audio)
            display_html(audio_tag, raw=True)
            return True
        message = 'ffmpeg failed to render OGG as MP3, result: {}'
        message = message.format(result)
        print(message)
        return False

    def _display_ogg(
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
        print(fluidsynth_command)
        result = systemtools.IOManager.spawn_subprocess(fluidsynth_command)
        if result == 0:
            encoded_audio = self._get_base64_from_file(ogg_file_path)
            audio_tag = '<audio controls type="audio/ogg" '
            audio_tag += 'src="data:audio/ogg;base64,{}">'
            audio_tag = audio_tag.format(encoded_audio)
            display_html(audio_tag, raw=True)
            return True
        message = 'fluidsynth failed to render MIDI as OGG, result: {}'
        message = message.format(result)
        print(message)
        return False

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
        return self._midi_bank

    @property
    def sound_font(self):
        return self._sound_font


class Show(object):

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''A replacement for Ajbad's show function for IPython Notebook.
        '''
        from abjad.tools import systemtools
        from abjad.tools import topleveltools
        from IPython.core.display import display_png
        assert '__illustrate__' in dir(expr)
        temporary_directory = tempfile.mkdtemp()
        temporary_file_path = os.path.join(
            temporary_directory,
            'output.png',
            )
        result = topleveltools.persist(expr).as_png(temporary_file_path)
        pngs = []
        for file_path in result[0]:
            command = 'convert {file_path} -trim {file_path}'.format(
                file_path=file_path,
                )
            systemtools.IOManager.spawn_subprocess(command)
            with open(file_path, 'rb') as file_pointer:
                file_contents = file_pointer.read()
                pngs.append(file_contents)
        shutil.rmtree(temporary_directory)
        for png in pngs:
            display_png(png, raw=True)


def load_ipython_extension(ipython):
    import abjad
    from abjad.tools import topleveltools
    play = Play()
    show = Show()
    abjad.play = play
    abjad.show = show
    topleveltools.play = play
    topleveltools.show = show
    names = {
        'load_sound_font': play.load_sound_font,
        'play': play,
        'show': show,
        }
    ipython.push(names)