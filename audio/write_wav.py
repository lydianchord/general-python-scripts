import argparse
import array
import math
import random
import wave


class WaveWriter:
    _FRAMERATE = 44100
    _MIN_VAL = -32768
    _MAX_VAL = 32767
    
    WAVEFORMS = ('white', 'sine', 'square', 'tri', 'saw')
    
    def __init__(self, waveform='sine', seconds=1, amp=0.8, freq=440,
                 duty=50, filename='output.wav'):
        self._FUNC_MAP = {
            'white': self._white_noise,
            'sine': self._sine_wave,
            'square': self._square_wave,
            'tri': self._triangle_wave,
            'saw': self._sawtooth_wave,
        }
        self.config(waveform, seconds, amp, freq, duty, filename)
    
    def _sin_val(self, i):
        return math.sin((2 * math.pi * self._freq * i) / self._FRAMERATE)
    
    def _white_noise(self):
        return [int(self._amp * random.randint(self._MIN_VAL, self._MAX_VAL))
                for i in range(self._num_frames)]
    
    def _sine_wave(self):
        return [int(self._amp * self._sin_val(i) * self._MAX_VAL)
                for i in range(self._num_frames)]
    
    def _square_wave(self):
        limit = self._duty / 100
        wave = []
        for i in range(self._num_frames):
            prop = (i / self._per) % 1
            if prop <= limit:
                wave.append(int(self._amp * self._MAX_VAL))
            else:
                wave.append(int(self._amp * self._MIN_VAL))
        return wave
    
    def _triangle_wave(self):
        half_per = self._per / 2
        wave = []
        for i in range(self._num_frames):
            floored = math.floor((i / half_per) + 0.5)
            val = ((2 / half_per) * (i - half_per * floored) *
                   (-1) ** floored)
            wave.append(int(self._amp * val * self._MAX_VAL))
        return wave
    
    def _sawtooth_wave(self):
        wave = []
        for i in range(self._num_frames):
            prop = i / self._per
            val = 2 * (prop - math.floor(0.5 + prop))
            wave.append(int(self._amp * val * self._MAX_VAL))
        return wave
    
    def config(self, waveform=None, seconds=None, amp=None, freq=None,
               duty=None, filename=None):
        if waveform is not None:
            if waveform not in self._FUNC_MAP:
                waveform = 'sine'
            self._waveform_func = self._FUNC_MAP[waveform]
        if seconds is not None:
            if seconds < 0:
                seconds = 0
            self._num_frames = int(seconds * self._FRAMERATE)
        if amp is not None:
            if amp > 1:
                amp = 1
            elif amp < 0:
                amp = 0
            self._amp = amp
        if freq is not None:
            if freq < 1:
                freq = 1
            self._freq = freq
            self._per = self._FRAMERATE / freq
        if duty is not None:
            if duty > 100:
                duty = 100
            elif duty < 0:
                duty = 0
            self._duty = duty
        if filename is not None:
            self._filename = filename
    
    def write(self, filename=None):
        if not filename:
            filename = self._filename
        if not filename.endswith('.wav'):
            filename = filename + '.wav'
        samples = array.array('h', self._waveform_func())
        with wave.open(filename, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self._FRAMERATE)
            f.setnframes(self._num_frames)
            f.writeframes(samples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-w', '--waveform', choices=WaveWriter.WAVEFORMS)
    parser.add_argument('-s', '--seconds', type=float)
    parser.add_argument('-a', '--amp', type=float)
    parser.add_argument('-f', '--freq', type=float)
    parser.add_argument('-d', '--duty', type=float)
    args = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}
    writer = WaveWriter(**args)
    writer.write()
