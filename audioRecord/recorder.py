import wave
from pyaudio import PyAudio, paInt16

framerate = 16000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 10

'''save the data to the wavfile'''
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()

def record():
    pa = PyAudio()
    stream = pa.open(format = paInt16, channels=channels, rate=framerate, input=True, frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    count = 0
    while count < TIME * 8:
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file('01.wav', my_buf)
    stream.close()

chunk = 2014
def play():
    wf = wave.open(r'01.wav', 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), 
                    rate=wf.getframerate(), output=True)
    while True:
        data = wf.readframes(chunk)
        if data == '': break
        stream.write(data)
    stream.close()
    p.terminate()

if __name__ == '__main__':
    record()
    print('Over!')
    play()
