import os.path
from subprocess import Popen, PIPE


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
