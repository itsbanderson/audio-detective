import sys, glob, os
from subprocess import call

def gen(indir, intype, outdir, outtype):
    os.chdir(os.path.join(os.getcwd(), indir))
    for track in glob.glob("*." + intype):
        outputfile = os.path.join(os.getcwd(), outdir, ".".join(track.split(".")[:-1]) + "." + outtype)
        call(["ffmpeg", "-loglevel", "0", "-i", track, "-y", outputfile]) 

if __name__ == "__main__":
    inputdir = sys.argv[1]
    inputtype = sys.argv[2]
    outputdir = sys.argv[3]
    outputtype = sys.argv[4]
    gen(inputdir, inputtype, outputdir, outputtype)
