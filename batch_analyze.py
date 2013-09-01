import audio_detective, sys, glob, os

def main():
    path = os.getcwd()
    directory = os.path.join(path, sys.argv[1])
    filetypes = ["flac"]
    for filetype in filetypes:
        bitrates = ["128", "192", "256", "320"]
        for bitrate in bitrates:
            os.chdir(os.path.join(directory, filetype, bitrate))
            for track in glob.glob("*." + filetype):
                #print str(audio_detective.get_spectrogram(track, 1024)) + " - " + bitrate + " - " + track
                print bitrate + " - " + audio_detective.get_spectrogram(track, 1024) + " - " + track

main()
