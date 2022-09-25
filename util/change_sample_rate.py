import librosa
import soundfile
import os
import time
import sys
import shutil

def pre_process_audio(audio_path):
    path_audio_processed = './ready_for_slice/'
    if not os.path.exists(path_audio_processed):
        try:
            os.mkdir(path_audio_processed)
        except OSError:
            print('Creation of directory %s failed' %path_audio_processed)
        else:
            print('Successfully created the directory %s' %path_audio_processed)

    start_sub = time.time()
    n = 0
    print('Downsampling wav files...')
    for file in os.listdir(audio_path):
        if(file.endswith('.wav')):
            try:
                nameSolo_1 = file.rsplit('.', 1)[0]
                data, samplerate = librosa.load(audio_path + file, sr=22050) # Downsample 44.1kHz to 24kHz
                soundfile.write(path_audio_processed + nameSolo_1 + '.wav', data, samplerate, subtype='PCM_16')
                n = n+1
                print('File ', n , ' completed:', nameSolo_1)
            except EOFError as error:
                next

    print('Downsampling complete')
    print('---------------------------------------------------------------------')

#    s = 0
#    print('Changing bit pro sample...')
#    for file in os.listdir(path_audio_processed):
#        if(file.endswith('.wav')):
#            try:
#                nameSolo_2 = file.rsplit('.', 1)[0]
#                #nameSolo_2 = nameSolo_2.replace('')
#                data, samplerate = soundfile.read(path_audio_processed + file)
#                soundfile.write(path_audio_processed + nameSolo_2 + '.wav', data, samplerate, subtype='PCM_16')
#                s = s + 1
#                print('File ' , s , ' completed')
#            except EOFError as error:
#                next

#    print('Bit pro sample changed')
#    print('---------------------------------------------------------------------')

    #shutil.rmtree('./audio', ignore_errors=True)

    end_sub = time.time()

    print('The script took ', end_sub-start_sub, ' seconds to run')



#Source:
#https://stackoverflow.com/questions/30619740/python-downsampling-wav-audio-file
#https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
