# Xample

> Test your python script against the sample inputs and outputs for the [Prologin](https://prologin.org) problems.

## Getting Started
### Prerequisites
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

In `exo_42.py` (you can choose any filename), write your solution:

```python
# https://prologin.org/train/2017/semifinal/42
input()  # optional
print(42)
```

Then

    cd PATH/TO/CURRENT/DIRECTORY
    python xample.py exo_42.py
    # python3 xample.py exo_42.py

`xample.py` and `exo_42.py` can be in different directories, and you can point to either using absolute or relative paths.

The output (it might take a while to load the samples from the url):
    

    exo_42.py
    ✅ Found url: https://prologin.org/train/2017/semifinal/42
    ⚠️ Cannot read samples.json; the file is reinitialized.
    ✅ Wrote samples to samples.json
    ✅ Saved url: https://prologin.org/train/2017/semifinal/42
    --

    ✅ Passed

Now let us see what will happen when we (deliberately) make a "mistake":

```python
# https://prologin.org/train/2017/semifinal/42
input()  # optional
print(6 * 9)
```
    
Output:
    
    exo_42.py
    ✅ Found url: https://prologin.org/train/2017/semifinal/42
    ⚠️ Reading examples from samples.json; delete entry in samples.json to reload.
    --

    ❌ Failed
    #Input
    QUEL EST LE PRODUIT DE SIX PAR NEUF
    #Expected Output
    42
    #Output
    54
    #Error
 
### Offline Usage
If `samples.json` was already populated, `xample.py` will automatically use the data there instead of redownloading, which allows offline use.

## Samples Syntax
`samples.json`:

    {
        "https://prologin.org/train/2017/semifinal/42": [
            {
                "in": "QUEL EST LE PRODUIT DE SIX PAR NEUF\n",
                "out": "42\n"
            }
        ]
    }

Note:
- the `\n` character at the end is kept (used as the input terminator)
