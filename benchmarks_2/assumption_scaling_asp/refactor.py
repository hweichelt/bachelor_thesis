from pathlib import Path
import os

for assumption_dir in [f for f in os.listdir(".") if os.path.isdir(f)]:
    for muc_dir in [f for f in os.listdir(assumption_dir) if os.path.isdir(Path(assumption_dir).joinpath(f))]:
        with open(Path(assumption_dir).joinpath(muc_dir).joinpath("encoding.lp"), "r") as f:
            out = f.read().replace(":-", "unsat :-")
        with open(Path(assumption_dir).joinpath(muc_dir).joinpath("encoding.lp"), "w") as f:
            f.write(out + f"\n\n#const n_assumptions={int(assumption_dir.replace('_assumptions', ''))}.")
