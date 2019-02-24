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
    if kwargs.get("vocab"):
        vocab_path = kwargs.get("vocab")
        vocab_args = ["-vocab-file", str(vocab_path)]
    else:
        vocab_args = []

    program = CWD / "build" / "cooccur"
    with open(corpus, "r") as infile, open(output_path, "wb") as outfile:
        cmd = [str(program)] + vocab_args
        print(cmd)
        p = subprocess.Popen(cmd, stdin=infile, stdout=outfile)
        p.wait()
    return output_path

def shuffle(coccur_bin: Path, output_path: Path, **kwargs):
    if kwargs.get("memory_limit"):
        memory_arg = kwargs.get("memory_limit")
        memory_args = ['-memory', 3.0]
    else:
        memory_args = []

    program = CWD / "build" / "shuffle"
    with open(coccur_bin, "rb") as infile, open(output_path, "wb") as outfile:
        cmd = [str(program)] + memory_args
        print(cmd)
        p = subprocess.Popen(str(program), stdin=infile, stdout=outfile)
        p.wait()
    return output_path

if __name__ ==  "__main__":
    OUTPUT = CWD / "output"
    corpus = CWD / "text8"
    vocab = OUTPUT / "vocab_py.txt"
    cobin = OUTPUT / "cooccurrences.bin.feat_py"
    shufbin = OUTPUT / "shuf.bin.feat_py"

    o = vocab_count(corpus, vocab)
    c = cooccur(corpus, cobin, vocab=vocab)
    s = shuffle(cobin, shufbin)
    print("result ready at {}".format(s))