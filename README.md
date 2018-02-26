# Xample

> Test your python script against the sample inputs and outputs for the [Prologin](https://prologin.org) problems.

## Getting Started
### Prerequisite
Check if you have python >= 3.6 installed:

    python --version  # Python 3.6.X
    # python3 --version

If not, download the latest version at https://www.python.org/downloads/

Clone this repository:

    # cd to desired location
    git clone https://github.com/Pyxidatol-C/Xample

Install the dependencies:

    pip install -r requirements.txt 
    # pip3 install -r requirements.txt

### Quick Start
Let's take a simple example: you are trying to solve [this lvl 0 problem](https://prologin.org/train/2017/semifinal/42). 

In `solution.py`, write your solution:

```python
# https://prologin.org/train/2017/semifinal/42
input()  # optional
print(42)
```

Then

    cd PATH/TO/CURRENT/DIRECTORY
    python xample.py
    # python3 xample.py

The output (it might take a while to load the samples from the url):
    
    Found url: https://prologin.org/train/2017/semifinal/42
    Wrote samples to samples.txt
    Saved url: https://prologin.org/train/2017/semifinal/42

    =Passed=
    Passed all tests

Now let us see what will happen when we (deliberately) make a "mistake" in `solution.py`:

```python
# https://prologin.org/train/2017/semifinal/42
input()  # optional
print(6 * 9)
```
    
Output:

    Found url: https://prologin.org/train/2017/semifinal/42
    To reload, remove the url on the first line in samples.txt.
    
    !!!!!!!!Failed!!!!!!!!
    #Input
    QUEL EST LE PRODUIT DE SIX PAR NEUF
    
    #Expected Output
    42
    
    #Output
    54
 
### Offline Usage
Alternatively, you can go on the problem page and manually copy the sample inputs / outputs to `samples.txt`.

Then, 
 
    python test.py
    # python3 test.py

Output:
    
    =Passed=
    Passed all tests.
    
Note that `test.py`'s features are fully included in `xample.py`. 
The core functions are all kept separately in `test.py` for the ease of implementation during the regional event.  

## Samples Syntax
In `samples.txt`, there exist the following tokens:
- input: `Exemple d'entrée`, `Sample input`
- output: `Exemple de sortie`, `Sample output`
- stop: `Commentaire`, `Note`, end of file

For example, if `samples.txt` looks like this:

    https://prologin.org/train/2017/semifinal/42

    Exemple d'entrée
    
    1
    
    Exemple de sortie
    
    2

The first line of the file serves as the header, which allows `xample.py` to recognize if the samples are already saved.

The following lines describe a test case:

- the input is the part in between the input token `Exemple d'entrée` and the output token `Exemple de sortie`: "1\n"
- the expected output is between between the output token `Exemple de sortie` and the stop token end of file: "2\n"

Note:
- **empty lines are ignored**
- the tokens are only recognized when they appear **alone** on a line (i.e. "Sample input " with a space is not a token)
- the `\n` character at the end is kept. For this purpose keep an empty line at the end of `samples.txt` 
