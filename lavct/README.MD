# lavct

Logic Analyzer Video Capture Tool

## Installation and running

```
pip install pygame
```

```
python lavct.py <CSV-FILE>
```

## Usage

- Change pixel clock period: `a` and `d` keys
- Change back porch value: `q` and `e` keys.
- Change colors:
   * `8` -> amber
   * `9` -> green
   * `0` -> white


<p align="center">
  <img width="80%" src="https://github.com/charlysan/x86_stuff/wiki/lavct/prince.gif">
</p>


## Examples and notes

```
python lavct.py prince.csv
```

Folder [captures](./captures/) contains `.csv` example files captured using a JUKO XT PC and Hercules Graphics card.