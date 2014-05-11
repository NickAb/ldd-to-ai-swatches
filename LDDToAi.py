#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import swatch as AiSwatch
import xml.etree.ElementTree as ET

def colorMetaWithMatID(matid):
	colorsMeta = {
		1 : ('White', 'White', 'Solid Colours'),
		5 : ('Brick-Yellow', 'Tan', 'Solid Colours'),
		18 : ('Nougat', 'Flesh', 'Solid Colours'),
		21 : ('Bright Red', 'Red', 'Solid Colours'),
		23 : ('Bright Blue', 'Blue', 'Solid Colours'),
		24 : ('Bright Yellow', 'Yellow', 'Solid Colours'),
		26 : ('Black', 'Black', 'Solid Colours'),
		28 : ('Dark Green', 'Green', 'Solid Colours'),
		37 : ('Bright Green', 'Bright Green', 'Solid Colours'),
		38 : ('Dark Orange', 'Dark Orange', 'Solid Colours'),
		102 : ('Medium Blue', 'Medium Blue', 'Solid Colours'),
		106 : ('Bright Orange', 'Orange', 'Solid Colours'),
		119 : ('Bright Yellowish-Green', 'Lime', 'Solid Colours'),
		124 : ('Bright Reddish Violet', 'Magenta', 'Solid Colours'),
		135 : ('Sand Blue', 'Sand Blue', 'Solid Colours'),
		138 : ('Sand Yellow', 'Dark Tan', 'Solid Colours'),
		140 : ('Earth Blue', 'Dark Blue', 'Solid Colours'),
		141 : ('Earth Green', 'Dark Green', 'Solid Colours'),
		151 : ('Sand Green', 'Sand Green', 'Solid Colours'),
		154 : ('Dark Red', 'Dark Red', 'Solid Colours'),
		191 : ('Flame Yellowish Orange', 'Bright Light Orange', 'Solid Colours'),
		192 : ('Reddish Brown', 'Reddish Brown', 'Solid Colours'),
		194 : ('Medium Stone Grey', 'Light Grey', 'Solid Colours'),
		199 : ('Dark Stone Grey', 'Dark Grey', 'Solid Colours'),
		208 : ('Light Stone Grey', ' Very Light Grey', 'Solid Colours'),
		212 : ('Light Royal Blue', 'Light Blue', 'Solid Colours'),
		221 : ('Bright Purple', 'Bright Pink', 'Solid Colours'),
		222 : ('Light Purple', 'Light Pink', 'Solid Colours'),
		226 : ('Cool Yellow', 'Blonde', 'Solid Colours'),
		268 : ('Medium Lilac', 'Dark Purple', 'Solid Colours'),
		283 : ('Light Nougat', 'Light Flesh', 'Solid Colours'),
		308 : ('Dark Brown', 'Dark Brown', 'Solid Colours'),
		312 : ('Medium Nougat', 'Medium Dark Flesh', 'Solid Colours'),
		330 : ('Olive Green', 'Olive Green', 'Solid Colours'),
		331 : ('Medium-Yellowish green', 'Dark Lime; Medium Lime', 'Solid Colours'),
		40 : ('Tr. (clear)', '', 'Tr. Colours'),
		41 : ('Tr. Red', '', 'Tr. Colours'),
		42 : ('Tr. Light Blue', '', 'Tr. Colours'),
		43 : ('Tr. Blue', '', 'Tr. Colours'),
		44 : ('Tr. Yellow', '', 'Tr. Colours'),
		47 : ('Tr. Fluorescent Reddish-Orange (Tr. Dark Orange)', '', 'Tr. Colours'),
		48 : ('Tr. Green', '', 'Tr. Colours'),
		49 : ('Tr. Fluorescent Green (Tr. Neon Green)', '', 'Tr. Colours'),
		111 : ('Tr. Brown (Smoke)', '', 'Tr. Colours'),
		113 : ('Tr. Medium Reddish-Violet', '', 'Tr. Colours'),
		126 : ('Tr. Bright Bluish-Violet', '', 'Tr. Colours'),
		143 : ('Tr. Fluorescent Blue', '', 'Tr. Colours'),
		182 : ('Tr. Bright Orange', '', 'Tr. Colours'),
		311 : ('Tr. Bright Green', '', 'Tr. Colours'),
		131 : ('Silver', 'Pearl Light Grey', 'Special Colours'),
		148 : ('Metallic Dark Grey', 'Pearl Dark Grey', 'Special Colours'),
		294 : ('Phosphorescent Green', 'Glow In Dark Trans Green', 'Special Colours'),
		297 : ('Warm Gold', 'Pearl Gold', 'Special Colours'),
		145 : ('Metallic Sand Blue', '', 'Phased out colours'),
		2 : ('Grey', '', 'Phased out colours'),
		27 : ('Dark Grey', '', 'Phased out colours'),
		153 : ('Sand Red', '', 'Phased out colours'),
		136 : ('Sand Violet', '', 'Phased out colours'),
		107 : ('Bright Bluish Green', '', 'Phased out colours'),
		25 : ('Earth Orange', '', 'Phased out colours'),
		104 : ('Bright Violet', '', 'Phased out colours'),
	}
	unknownMetaData = ('Unknown', '', 'NA')
	colorMetaData = colorsMeta.get(int(matid), unknownMetaData)
	colorName = '%s: %s' % (matid, colorMetaData[0])
	
	if (colorMetaData[0] != colorMetaData[1] and colorMetaData[1]):
		colorName = '%s (%s)' % (colorName, colorMetaData[1])
		
	colorName = colorName[:29] + (colorName[29:] and '..')
		
	return {'name': colorName, 'group': colorMetaData[2]}

def formatGlobalColorSwatchRGB(matid, red, green, blue):
	colorMeta = colorMetaWithMatID(matid)

	data = {'mode' : u'RGB', 'values' : [float(red)/255., float(green)/255., float(blue)/255.]}
	swatch = {'data' : data, 'name' : unicode(colorMeta['name']), 'type' : u'Global'}
	
	return {'swatch' : swatch, 'group' : colorMeta['group']}

def xmlFileToSwatches(dataset):
	tree = ET.parse(dataset)
	root = tree.getroot()

	swatchesList = []
	swatchesGroups = {}

	for mat in root.findall('Material'):
		swatchInfo = formatGlobalColorSwatchRGB(mat.get('MatID'), mat.get('Red'), mat.get('Green'), mat.get('Blue'))
		
		groupKey = swatchInfo['group']
		swatch = swatchInfo['swatch']
		
		if groupKey not in swatchesGroups:
			swatchesGroups[groupKey] = []
			
		swatchesGroups[groupKey].append(swatch)
		
	for groupKey in swatchesGroups:
		if groupKey != 'NA':
			groupDic = {'name' : unicode(groupKey), 'swatches' : swatchesGroups[groupKey], 'type': u'Color Group'}		
			swatchesList.append(groupDic)

	return swatchesList	

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

dataset = safe_list_get(sys.argv, 1, 'Materials.xml')

filename = safe_list_get(sys.argv, 2, 'LDDColors.ase')

print dataset
print filename


swatchesList = xmlFileToSwatches(dataset)

AiSwatch.write(swatchesList, filename)
