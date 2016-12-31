LDD to Ai Swatches
==================

LDD to Ai Swatches is a python script that converts Materials.xml form Lego Digital Designer into Adobe Illustrator swatchs file (.ase).
Convert Lego Digital Designer colors (materials.xml) into Adobe swatch file
(.ase).

optional arguments:
```
  -h, --help            show this help message and exit
  -i INPUTFILE, --materialspath INPUTFILE
                        File path to LEGO Digital Designer Materials.xml
  -o OUTPUTFILE, --swatch OUTPUTFILE
                        File path to output Adobe swatches file (must
                        including file name and extension)
```

Materials.xml can be found inside db.lif shipped with LEGO Digital Designer

Prerequisites
------------
__swatch__ (parser for adobe swatch exchange files) https://github.com/nsfmc/swatch

Usage
-----
```bash
python ldd_to_ai.py
python ldd_to_ai.py -i INPUTFILE -o OUTPUTFILE
```
