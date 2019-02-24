from pathlib import Path
import subprocess

CWD = Path(__file__).parent

def vocab_count(corpus: Path, output_path: Path):
    program = CWD / "build" / "vocab_count"
    with open(corpus, "r") as infile, open(output_path, "w") as outfile:
        p = subprocess.Popen(str(program), stdin=infile, stdout=outfile)
        p.wait()
    return output_path

def cooccur(corpus: Path, output_path: Path, **kwargs):
    if kwargs:
        print("kwargs!")

    program = CWD / "build" / "cooccur"
    with open(corpus, "r") as infile, open(output_path, "w") as outfile:
        p = subprocess.Popen(str(program), stdin=infile, stdout=outfile)
        p.wait()

if __name__ ==  "__main__":
    corpus = CWD / "text8"
    vocab = CWD / "vocab_py.txt"
    cobin = CWD / "cooccurrences.bin.feat_py"

    o = vocab_count(corpus, vocab)
    c = cooccur(corpus, cobin)
    print("file ready at {}".format(o))