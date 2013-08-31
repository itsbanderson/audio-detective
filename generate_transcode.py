import sys, glob, os
from subprocess import call

def generate_transcode(indir, outdir, bitrate):
    call(["mkdir", "-p", os.path.join(outdir, "tmp")])
    tmpdir = os.path.join(outdir, "tmp")

    os.chdir(indir)
    for track in glob.glob("*.flac"):
        outputfile = os.path.join(tmpdir, ".".join(track.split(".")[:-1]) + ".mp3")
        call(["ffmpeg", "-loglevel", "0", "-i", track, "-b", bitrate, "-y", outputfile]) 

    os.chdir(tmpdir)
    for track in glob.glob("*.mp3"):
        outputfile = os.path.join(outdir, ".".join(track.split(".")[:-1]) + ".flac")
        call(["ffmpeg", "-loglevel", "0", "-i", track, outputfile]) 

    call(["rm", "-r", tmpdir])

def main():
    relindir = sys.argv[1]
    reloutdir = sys.argv[2]
    bit = sys.argv[3]
    path = os.getcwd()

    if bit == "all":
        bitrates = ["128", "192", "256", "320"]
        for bitrate in bitrates:
            indir = os.path.join(path, relindir)
            outdir = os.path.join(path, reloutdir, "flac", bitrate)
            generate_transcode(indir, outdir, bitrate)
    else:
        indir = os.path.join(path, relindir)
        outdir = os.path.join(path, reloutdir)
        generate_transcode(indir, outdir, bit)

if __name__ == "__main__":
    main()
