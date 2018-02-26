from bs4 import BeautifulSoup
from test import check_samples
import urllib.request


def fetch_samples(url: str) -> str:
    """Fetch the Input/output samples section from the url to the Prologin problem.

    :param url: The URL to the prologin problem.
                A string of the format "http[s]://prologin.org/train/<YEAR>/<qualification|semifinal>/<EXERCISE_NAME>"
    :return: The text in the Input/output samples section from the problem's page.
    """
    return BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser").find(id="samples").text


def load_samples():
    """Read the samples from the url specified in solution.py and write it to samples.txt."""
    with open("solution.py") as f:
        code = f.readlines()
    if code:
        url = code[0][2:-1]  # 2: to ignore the start of comment ('# ') and :-1 to strip '\n' at the end
        print(f"Found url: {url}")
        with open("samples.txt") as f:
            local_samples = f.readlines()
        if local_samples:
            url_loaded = local_samples[0].strip('\n')
            if url_loaded == url:
                print(f"To reload, remove the url on the first line in samples.txt.\n")
                return

        samples = fetch_samples(url)
        with open("samples.txt", "w") as f:
            f.write(url + '\n')
            f.write(samples)
        print(f"Wrote samples to samples.txt")
        print(f"Saved url: {url}\n")


if __name__ == '__main__':
    load_samples()
    check_samples()
