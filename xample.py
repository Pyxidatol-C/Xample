import sys
import os.path
import urllib.request
from bs4 import BeautifulSoup
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
        ["python3", path],
        stdin=PIPE,
        stdout=PIPE
    )
    outs, _ = process.communicate(ins.encode())
    return outs.decode()


def get_samples() -> List[Tuple[str, str]]:
    """Get the sample inputs/outputs from samples.txt.

    :return: The sample inputs/outputs as a list of tuples of the the form (in, out).
    """
    samples = []
    with open("samples.txt") as f:
        taking_input = False
        taking_output = False
        in_ = ""  # Note: it is assumed that there are no empty inputs
        out = ""  # or empty outputs
        for line in f.readlines():
            if line == "Exemple d'entrée\n" or line == "Sample input\n":
                taking_input = True
                taking_output = False
                if out:
                    samples.append((in_, out))
                    in_, out = "", ""
                continue
            if line == "Exemple de sortie\n" or line == "Sample output\n":
                taking_input = False
                taking_output = True
                continue
            if line == "Commentaire\n" or line == "Note\n":
                taking_input = False
                taking_output = False
                samples.append((in_, out))
                in_, out = "", ""

            if line != '\n':
                if taking_input:
                    in_ += line
                if taking_output:
                    out += line
    if taking_output:
        samples.append((in_, out))
    return samples


def check_sample(in_: str, expected_out: str, file: str) -> Tuple[bool, str]:
    """Runs individual test

    :param in_: The input fed to stdin.
    :param expected_out: The expected output.
    :param file: the path to the python script
    :return: The output of the program and a boolean indicating
             if it is the same as the expected output as a tuple.
    """
    out = run_file(file, in_)
    return out == expected_out, out


def check_samples(file: str = "solution.py"):
    """Run check_sample over all the examples and display nice error messages"""
    err = False
    for in_, expected_out in get_samples():
        try:
            passed, out = check_sample(in_, expected_out, file)
            if not passed:
                raise ValueError
        except Exception as e:
            print("!!!!!!!!Failed!!!!!!!!\n"
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
    if not err and get_samples():
        print("Passed all tests.")


def fetch_samples(url: str) -> str:
    """Fetch the Input/output samples section from the url to the Prologin problem.

    :param url: The URL to the prologin problem.
                A string of the format "http[s]://prologin.org/train/<YEAR>/<qualification|semifinal>/<EXERCISE_NAME>"
    :return: The text in the Input/output samples section from the problem's page.
    """
    return BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser").find(id="samples").text


def load_samples(file: str = "solution.py"):
    """Read the samples from the url specified in the solution file and write it to samples.txt."""
    with open(file) as f:
        code = f.readlines()
    if code:
        url = code[0][2:-1]  # 2: to ignore the start of comment ('# ') and :-1 to strip '\n' at the end
        print(f"Found url: {url}")
        try:
            with open("samples.txt") as f:
                local_samples = f.readlines()
        except FileNotFoundError:
            # file doesn't exist yet
            local_samples = None
        
        if local_samples:
            url_loaded = local_samples[0].strip('\n')
            if url_loaded == url:
                print(f"To reload examples, remove the url on the first line in samples.txt.\n")
                return

        samples = fetch_samples(url)
        with open("samples.txt", "w") as f:
            f.write(url + '\n')
            f.write(samples)
        print(f"Wrote samples to samples.txt")
        print(f"Saved url: {url}\n")


def test(file: str = "solution.py"):
    load_samples(file)
    check_samples(file)


if __name__ == '__main__':
    try:
        test(sys.argv[1])
    except IndexError:
        raise FileNotFoundError("Solution filename must be passed as a command line argument")
