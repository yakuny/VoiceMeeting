import argparse
import queue
import threading
import wave
import numpy as np

import pyaudio
from pynput import keyboard
from data_process import DataProcess

# ===========================================
#        Parse the argument
# ===========================================

parser = argparse.ArgumentParser()
# setup pyaudio record configuration
parser.add_argument('--CHUNK', default=1024, type=int)
parser.add_argument('--SAMPLE_WIDTH', default=2, type=int)
parser.add_argument('--CHANNELS', default=1, type=int)
parser.add_argument('--RATE', default=16000, type=int)
parser.add_argument('--RECORD_SECONDS', default=1, type=int)
parser.add_argument('--FILENAME', default='output.wav', type=str)
args = parser.parse_args()

data_queue = queue.Queue()


class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press)
        self.start_flag = False
        self.end_flag = False

    def on_press(self, key):
        # start recording
        if key == keyboard.Key.space:
            self.start_flag = True
            print('Start recording.')

        # stop recording
        elif key == keyboard.Key.esc:
            print('Stop recording')
            self.end_flag = True
            return False

        return True


class AudioRecorder(threading.Thread):
    def __init__(self, listener):
        super().__init__()
        global data_queue
        self.p = pyaudio.PyAudio()
        self.listener = listener
        self.wf = wave.open(args.FILENAME, 'wb')
        self.wf.setnchannels(args.CHANNELS)
        self.wf.setsampwidth(args.SAMPLE_WIDTH)
        self.wf.setframerate(args.RATE)

    def run(self):
        print("Press 'Space Bar' to start recording.")
        print("Press 'Esc' to end recording.")
        self.start_record()

    def start_record(self):
        stream = self.p.open(format=self.p.get_format_from_width(args.SAMPLE_WIDTH),
                             channels=args.CHANNELS,
                             rate=args.RATE,
                             input=True,
                             frames_per_buffer=args.CHUNK,
                             start=False)
        while not self.listener.start_flag:
            pass
        stream.start_stream()
        frames = []
        while stream.is_active():
            string_audio_data = stream.read(args.CHUNK)
            frames.append(string_audio_data)
            audio_data = np.fromstring(string_audio_data, dtype=np.int16).astype('float32')
            data_queue.put(audio_data)
            if self.listener.end_flag:
                stream.stop_stream()
                self.wf.writeframes(b''.join(frames))
                self.wf.close()
                print('You should have a wav file in the current directory')

        stream.close()
        self.p.terminate()


if __name__ == '__main__':
    keyboard_listener = MyListener()
    keyboard_listener.start()

    recorder = AudioRecorder(keyboard_listener)
    recorder.start()

    data_process = DataProcess(data_queue, args, keyboard_listener)
    data_process.start()

    recorder.join()
    print('End.')