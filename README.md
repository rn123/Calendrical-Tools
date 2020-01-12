# Calendrical Tools

Calendrical Tools is a Python package for computing different calendars using the code from Reingold & Dershowitz, Calendrical Computations. 

Candybar is a tool for computing calendars and displaying then in a rectangular format. The goal is to produce output similar to Appendix C of Reingold & Dershowitz.

![candybar](output/cal_2020.png)

## Installation

```
pip install git+https://github.com/rn123/Calendrical-Tools#egg=Calendrical-Tools
```

## Usage

```python
from calendrical_tools import candybar

cal = candybar.TextCandyBar(2020)
cal.prcandybar()
```

## License
Includes a version of pycalcal

[MIT](https://choosealicense.com/licenses/mit/)
