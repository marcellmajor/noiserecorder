import pyaudio
import wave
import io
import numpy as np
from array import array
from datetime import datetime

# gnuplot -e "filename='volume_log_24-10-19_00-40-30.txt';" -p volumegraph.gnuplot

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 4 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test2.wav' # name of .wav file

period_seconds = 60 * 5
period_max = 0

min_volume = 115
max_volume = 0
file_counter = 0

def record_wavfile( volmax, filecount ):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%y-%m-%d_%H-%M")
    # save the audio frames as .wav file
    wav_output_filename = "sample" + str(filecount) + "_" + formatted_time + "_" + str(volmax) + ".wav"
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

seconds_elapsed = 0
logfile_name = "volume_log_" + datetime.now().strftime("%y-%m-%d_%H-%M-%S") + ".txt"
logfile = open( logfile_name, "w" )
logfile.write( "{}, {}\n".format( "Datetime", "Maxvolume" ) )
logfile.close()

while(True):
    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("                    recording                ", end='\r')
    frames = []

    record_file = False
    recorded_volume = 0
    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        if( vol > min_volume ):
            recorded_volume = vol
            file_counter += 1
            record_file = True
        if( vol > max_volume ):
            max_volume = vol
        if( period_max < vol):
            period_max = vol

        print( "{} - {}     ".format(str(vol),str(max_volume)), end='\r' )
        frames.append(data)

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    seconds_elapsed += record_secs
    if( ( seconds_elapsed % period_seconds ) == 0 ):
        logfile = open( logfile_name, "a" )
        logfile.write( "{}, {}\n".format( datetime.now().strftime("%y-%m-%d_%H-%M-%S"), period_max ) )
        logfile.close()
        period_max = 0

    print("                    finished recording    ", end='\r')
    
    if( record_file ):
        record_wavfile( recorded_volume, file_counter )
        # pass


