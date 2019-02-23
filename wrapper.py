from pathlib import Path
import subprocess

CWD = Path(__file__).parent

def vocab_count(corpus: Path, output_path: Path):
    program = CWD / "build" / "vocab_count"
    with open(corpus, "r") as infile, open(output_path, "w") as outfile:
        subprocess.Popen(str(program), stdin=infile, stdout=outfile)
    return output_path

if __name__ ==  "__main__":
    corpus = CWD / "text8"
    outfile = CWD / "vocab_py.txt"

    o = vocab_count(corpus, outfile)
    print("file ready at {}".format(o))