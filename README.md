LDD to Ai Swatches
==================

LDD to Ai Swatches is a python script that converts Materials.xml form Lego Digital Designer into Adobe Illustrator swatchs file (.ase).

Prerequsites
------------
__swatch__ (parser for adobe swatch exchange files) https://github.com/nsfmc/swatch

Usage
-----
```bash
python LDDToAi.py materialsxmlpath swatchespath
```

`materialsxmlpath` - path for `Materials.xml` file from extracted LDD `db.lif` (default `Materials.xml`)

`swatchespath` - deires file name for swatches file (default `LDDColors.ase`)