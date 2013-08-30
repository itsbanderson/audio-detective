import sys, glob, os
from subprocess import call

def generate_transcode(indir, outdir, bitrate):
    os.chdir(os.path.join(os.getcwd(), indir))
    outpath = os.path.join(os.getcwd(), outdir)
    call(["mkdir", os.path.join(outpath, "tmp")])

    tmpdir = os.path.join(outpath, "tmp")
    for track in glob.glob("*.flac"):
        outputfile = os.path.join(tmpdir, ".".join(track.split(".")[:-1]) + ".mp3")
        call(["ffmpeg", "-loglevel", "0", "-i", track, "-b", bitrate, "-y", outputfile]) 

    os.chdir(tmpdir)
    for track in glob.glob("*.mp3"):
        outputfile = os.path.join(outpath, ".".join(track.split(".")[:-1]) + ".flac")
        call(["ffmpeg", "-loglevel", "0", "-i", track, outputfile]) 

    call(["rm", "-r", tmpdir])

if __name__ == "__main__":
    indir = sys.argv[1]
    outdir = sys.argv[2]
    bitrate = sys.argv[3]
    gen(indir, outdir, bitrate)
