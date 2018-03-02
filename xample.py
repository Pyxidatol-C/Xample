import re
import sys
import json
import glob2
import os.path
import json.decoder
import urllib.request
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple
from subprocess import Popen, PIPE, TimeoutExpired


def run_file(py_file: str, ins: str = "") -> str:
    """Run python script with optional input to stdin and return output from stdout.

    :param py_file: The path to the python script.
    :raise FileNotFoundError: When path 'py_file' cannot be resolved.
    :param ins: The input fed to stdin as a string.
                Defaults to empty string (no input).
    :return: The output from stdout as a string.
    """
    # Create subprocess
    process = Popen(
        ["python3", py_file],
        stdin=PIPE,
        stdout=PIPE
    )
    try:
        outs, _ = process.communicate(ins.encode(), timeout=10)
    except TimeoutExpired as e:
        process.kill()
        raise e
    else:
        return outs.decode()


def process_samples(raw_text: str) -> List[Dict[str, str]]:
    """Convert the raw sample text into a list of {'in': in, 'out', out}.

    :param raw_text: The raw sample text to be processed.
    :return: The sample inputs/outputs as a list of tuples of the the form (in, out).
    """
    samples = []
    taking_input = False
    taking_output = False
    in_ = ""  # Note: it is assumed that there are no empty inputs
    out = ""  # or empty outputs
    for line in raw_text.split('\n'):
        if line == "Exemple d'entrée" or line == "Sample input":
            taking_input = True
            taking_output = False
            if out:
                samples.append({"in": in_, "out": out})
                in_, out = "", ""
            continue
        if line == "Exemple de sortie" or line == "Sample output":
            taking_input = False
            taking_output = True
            continue
        if line == "Commentaire" or line == "Note":
            taking_input = False
            taking_output = False
            samples.append({'in': in_, 'out': out})
            in_, out = "", ""

        if line:
            if taking_input:
                in_ += line + "\n"
            if taking_output:
                out += line + "\n"
    if taking_output:
        samples.append({'in': in_, 'out': out})
    return samples


def check_sample(in_: str, expected_out: str, py_file: str) -> Tuple[bool, str]:
    """Run individual test.

    :param in_: The input fed to stdin.
    :param expected_out: The expected output.
    :param py_file: the path to the python script
    :return: The output of the program and a boolean indicating
             if it is the same as the expected output as a tuple.
    """
    out = run_file(py_file, in_)
    return out == expected_out, out


def check_samples(py_file: str):
    """Run check_sample over all the examples and display nice error messages."""
    samples = get_samples(py_file)
    for sample in samples:
        in_, expected_out = sample['in'], sample['out']
        out = ""
        try:
            passed, out = check_sample(in_, expected_out, py_file)
            if not passed:
                raise ValueError
        except Exception as e:
            print("❌ Failed")
            print("#Input")
            print(in_.strip('\n'))
            print("#Expected Output")
            print(expected_out.strip('\n'))
            print("#Output")
            print(out.strip('\n'))
            print("#Error")
            print(e)
        else:
            print("✅ Passed")
    if not samples:
        print("⚠️ No tests found.")
    print()


def fetch_samples(url: str) -> str:
    """Fetch the Input/output samples section from the url to the Prologin problem.

    :param url: The URL to the prologin problem.
                A string of the format "http[s]://prologin.org/train/<YEAR>/<qualification|semifinal>/<EXERCISE_NAME>"
    :return: The text in the Input/output samples section from the problem's page.
    """
    return BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser").find(id="samples").text


def get_samples(py_file: str) -> List[Dict[str, str]]:
    """Get samples from samples.json using the url in the script (calling load_samples before ensures that it exists).

    :param py_file: The path to the python script.
    :return: The samples in samples.json matched by the url on the first line of the script.
    """
    with open(py_file) as f:
        url = re.search(r"https?://prologin.org/train/20\d{2}/(qualification|semifinal)/[a-z_A-Z\d]*", f.readline())[0]
    with open("samples.json") as f2:
        return json.load(f2)[url]


def load_samples(py_file: str) -> bool:
    """Read the samples from the url specified in first one of the solution file and write it to samples.json.

    :param py_file: The path to the solution python script.
    :return: True if the samples are successfully loaded from the specified url; False otherwise.
    """
    print("#" * 80)
    print(py_file)
    with open(py_file) as f:
        code = f.readlines()
    if code and re.search(r"https?://prologin.org/train/20\d{2}/(qualification|semifinal)/[a-z_A-Z\d]*", code[0]):
        url = re.search(r"https?://prologin.org/train/20\d{2}/(qualification|semifinal)/[a-z_A-Z\d]*", code[0])[0]
        print(f"✅ Found url: {url}")
        try:
            with open("samples.json") as f:
                local_samples = json.load(f)
                if type(local_samples) != dict:
                    raise json.decoder.JSONDecodeError
        except (FileNotFoundError, json.decoder.JSONDecodeError):  # file doesn't exist yet or invalid json
            local_samples = {}
            print("⚠️ Cannot read samples.json; the file is reinitialized.")

        if url in local_samples:
            print(f"⚠️ Reading examples from samples.json; delete entry in samples.json to reload.")
            print("--\n")
            return True
        local_samples[url] = process_samples(fetch_samples(url))
        with open("samples.json", "w") as f:
            json.dump(local_samples, f, indent=2)
        print(f"✅ Wrote samples to samples.json")
        print(f"✅ Saved url: {url}")
    else:
        print("❌️ Failed to locate url on first line of script.")
        print('--\n')
        return False
    print("--\n")
    return True


def test(py_file: str):
    if load_samples(py_file):
        check_samples(py_file)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '**/'
    path += "/" if os.path.isdir(path) and not path.endswith("/") else ""
    path += "*.py" if path.endswith("/") else ""
    files: List[str] = sorted(glob2.glob(path))
    if not files:
        print(f"⚠️ {path} does not match any file.")
    for file in files:
        test(file)
