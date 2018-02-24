# Xample

> Test your python script against the sample inputs and outputs for the [Prologin](https://prologin.org) problems.

## Getting Started
### Prerequisite
Check if you have python >= 3.6 installed:

    python --version  # Python 3.6.X
    # python3 --version
    pip install -r requirements.txt 
    # pip3 install -r requirements.txt

If not, download the latest version at https://www.python.org/downloads/

Clone this repository:

    # cd to desired location
    git clone https://github.com/Pyxidatol-C/Xample

### Quick Start
Let's take a simple example: you are trying to solve [this lvl 0 problem](https://prologin.org/train/2017/semifinal/42). 

In `solution.py`, write your solution:

```python
# Prologin
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

    =Passed=
    Passed all tests

Now let us see what will happen when we (deliberately) make a "mistake" in `solution.py`:

```python
# Prologin
# https://prologin.org/train/2017/semifinal/42
input()  # optional
print(54)
```
    
Output:

    Found url: https://prologin.org/train/2017/semifinal/42
    Wrote samples to samples.txt
    
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

You may want to use `test.py` over `xample.py` for several reasons:
- `test.py` works offline (and does not require bs4), while `xample.py` retrieves the samples online;
- `test.py` assumes that the sample inputs / outputs are available and up to date in `samples.txt`, 
   while `xample.py` **overwrites** `samplex.txt` with the retrieved samples;
- `test.py` allows you to add custom test cases - see the next section for the syntax specifications. 


## Samples Syntax
In `samples.txt`, there exist the following tokens:
- input: `Exemple d'entrée`, `Sample input`
- output: `Exemple de sortie`, `Sample output`
- stop: `Commentaire`, `Note`, end of file

For example, if `samples.txt` looks like this:

    Exemple d'entrée
    
    1
    
    Exemple de sortie
    
    2

There are 2 test cases.

In the first one, 
- the input is the part in between the input token `Exemple d'entrée` and the output token `Exemple de sortie`: "1\n"
- the output is between between the output token `Exemple de sortie` and the stop token end of file: "2\n"

Note:
- **empty lines are ignored**
- the tokens are only recognized when they appear **alone** on a line (i.e. "Sample input " with a space is not a token)
- the `\n` character at the end is kept. For this purpose keep an empty line at the end of `samples.txt` 
