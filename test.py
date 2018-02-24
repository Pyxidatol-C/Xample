import os.path
from subprocess import Popen, PIPE
from typing import List, Tuple


def run_file(py_file: str, ins: str = "") -> str:
    """Run python script with optional input to stdin and return output from stdout.

    :param py_file: The name of the python script.
                    Relative path will be tried first;
                    if that fails absolute path will be used;
                    if that fails too a FileNotFoundError is raised.
    :raise FileNotFoundError: When path 'py_file' cannot be resolved.
    :param ins: The input fed to stdin as a string.
                Defaults to empty string (no input).
    :return: The output from stdout as a string.
    """
    # Resolve file path
    if os.path.isfile(py_file):
        path = py_file  # as absolute path
    else:
        rel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), py_file)
        if os.path.isfile(rel_path):
            path = rel_path
        else:
            raise FileNotFoundError

    # Create subprocess
    process = Popen(
        ["python", path],
        stdin=PIPE,
        stdout=PIPE
    )
    outs, _ = process.communicate(ins.encode())
    return outs.decode()[:-1]  # strip \n at the end


def get_samples() -> List[Tuple[str, str]]:
    """Get the sample inputs/outputs from samples.txt.

    :return: The sample inputs/outputs as a list of tuples of the the form (in, out).
    """


def check_sample(in_: str, expected_out: str) -> Tuple[bool, str]:
    """Run solution.py and check its output.

    :param in_: The input fed to stdin.
    :param expected_out: The expected output.
    :return: The output of the program and a boolean indicating
             if it is the same as the expected output as a tuple.
    """
    out = run_file("solution.py", in_)
    return out == expected_out, out


def check_samples():
    """Run solution.py and check against the inputs/outputs in samples.txt"""
    err = False
    for in_, expected_out in get_samples():
        try:
            passed, out = check_sample(in_, expected_out)
            if not passed:
                raise ValueError
        except Exception as e:
            print("!Failed!\n"
                  "#Input\n"
                  f"{in_}\n"
                  "#Expected Output\n"
                  f"{expected_out}\n"
                  "#Output\n"
                  f"{out}\n"
                  f"{e}")
            err = True
            print(e)
        else:
            print("=Passed=")
    if not err:
        print("===Passed all tests===")
