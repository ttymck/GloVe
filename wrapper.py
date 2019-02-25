from dataclasses import dataclass
from pathlib import Path
import subprocess

@dataclass
class GloVeResult:
    vectors: Path
    gradsq: Path

class GloVe:
    build_dir = Path(__file__).parent / "build"
    output_dir = Path(__file__).parent / "output" / "cls"

    def __init__(self, build_path=None, output_path=None):
        if build_path: 
            GloVe.build_dir = build_path
        if output_path:
            GloVe.output_dir = output_path

    @classmethod
    def from_corpus(cls, corpus: Path):
        vocab_path = cls.output_dir / "vocab_count.cls"
        print("running vocab_count")
        if cls.vocab_count(corpus, vocab_path):
            coocur_path = cls.output_dir / "cooccur.cls"
            print("running cooccur")
            if cls.cooccur(corpus, coocur_path, vocab=vocab_path):
                shuf_path = cls.output_dir / "cooccur.shuf.cls"
                print("running shuffle")
                if cls.shuffle(coocur_path, shuf_path):
                    vector_path, gradsq_path = cls.output_dir / "vectors.cls", cls.output_dir / "gradsq.cls"
                    print("running glove (training model)")
                    if cls.train(shuf_path, vocab_path, vector_path, gradsq_path):
                        return GloVeResult(vector_path, gradsq_path)

    @classmethod
    def vocab_count(cls, corpus: Path, output_path: Path):
        program = cls.build_dir / "vocab_count"
        with open(corpus, "r") as infile, open(output_path, "w") as outfile:
            p = subprocess.Popen(str(program), stdin=infile, stdout=outfile)
            p.wait()
        return not p.returncode

    @classmethod
    def cooccur(cls, corpus: Path, output_path: Path, **kwargs):
        if kwargs.get("vocab"):
            vocab_path = kwargs.get("vocab")
            vocab_args = ["-vocab-file", str(vocab_path)]
        else:
            vocab_args = []

        program = cls.build_dir / "cooccur"
        with open(corpus, "r") as infile, open(output_path, "wb") as outfile:
            cmd = [str(program)] + vocab_args
            print(cmd)
            p = subprocess.Popen(cmd, stdin=infile, stdout=outfile)
            p.wait()
        return not p.returncode

    @classmethod
    def shuffle(cls, coccur_binary: Path, output_path: Path, **kwargs):
        if kwargs.get("memory_limit"):
            memory_arg = kwargs.get("memory_limit")
            memory_args = ['-memory', 3.0]
        else:
            memory_args = []

        program = cls.build_dir / "shuffle"
        with open(coccur_binary, "rb") as infile, open(output_path, "wb") as outfile:
            cmd = [str(program)] + memory_args
            print(cmd)
            p = subprocess.Popen(cmd, stdin=infile, stdout=outfile)
            p.wait()
        return not p.returncode

    @classmethod
    def train(cls, input_file: Path, vocab_file: Path, save_file, gradsq_file,
            vector_size=100, threads=16, alpha=0.75, x_max=100.0, eta=0.05,
            binary=2, model=2
            ):
        program = cls.build_dir / "glove"
        cmd = [str(program), 
            "-input-file", f"{input_file}", 
            "-vocab-file", f"{vocab_file}", 
            "-save-file", f"{save_file}",
            "-gradsq-file", f"{gradsq_file}", 
            "-vector-size", f"{vector_size}", 
            "-threads", f"{threads}", 
            "-alpha", f"{alpha}", 
            "-x-max", f"{x_max}", 
            "-eta", f"{eta}", 
            "-binary", f"{binary}", 
            "-model", f"{model}",
        ]
        print(cmd)
        p = subprocess.Popen(cmd)
        p.wait()
        return not p.returncode

if __name__ ==  "__main__":
    cwd = Path(__file__).parent / "build"
    corpus = Path(__file__).parent / "text8"

    result = GloVe.from_corpus(corpus)
    if result:
        print("Success!")
        print("Vectors at: {}; Gradsq at: {}".format(result.vectors, result.gradsq))
