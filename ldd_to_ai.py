#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
import argparse

import swatch as ai_swatch_helper

from colors_meta_helper import color_meta_by_material_id


def color_meta_by_material_id(material_id):
    colors_metadata = {
        1: ('White', 'White', 'Solid Colours'),
        5: ('Brick-Yellow', 'Tan', 'Solid Colours'),
        18: ('Nougat', 'Flesh', 'Solid Colours'),
        21: ('Bright Red', 'Red', 'Solid Colours'),
        23: ('Bright Blue', 'Blue', 'Solid Colours'),
        24: ('Bright Yellow', 'Yellow', 'Solid Colours'),
        26: ('Black', 'Black', 'Solid Colours'),
        28: ('Dark Green', 'Green', 'Solid Colours'),
        37: ('Bright Green', 'Bright Green', 'Solid Colours'),
        38: ('Dark Orange', 'Dark Orange', 'Solid Colours'),
        102: ('Medium Blue', 'Medium Blue', 'Solid Colours'),
        106: ('Bright Orange', 'Orange', 'Solid Colours'),
        119: ('Bright Yellowish-Green', 'Lime', 'Solid Colours'),
        124: ('Bright Reddish Violet', 'Magenta', 'Solid Colours'),
        135: ('Sand Blue', 'Sand Blue', 'Solid Colours'),
        138: ('Sand Yellow', 'Dark Tan', 'Solid Colours'),
        140: ('Earth Blue', 'Dark Blue', 'Solid Colours'),
        141: ('Earth Green', 'Dark Green', 'Solid Colours'),
        151: ('Sand Green', 'Sand Green', 'Solid Colours'),
        154: ('Dark Red', 'Dark Red', 'Solid Colours'),
        191: ('Flame Yellowish Orange', 'Bright Light Orange', 'Solid Colours'),
        192: ('Reddish Brown', 'Reddish Brown', 'Solid Colours'),
        194: ('Medium Stone Grey', 'Light Grey', 'Solid Colours'),
        199: ('Dark Stone Grey', 'Dark Grey', 'Solid Colours'),
        208: ('Light Stone Grey', ' Very Light Grey', 'Solid Colours'),
        212: ('Light Royal Blue', 'Light Blue', 'Solid Colours'),
        221: ('Bright Purple', 'Bright Pink', 'Solid Colours'),
        222: ('Light Purple', 'Light Pink', 'Solid Colours'),
        226: ('Cool Yellow', 'Blonde', 'Solid Colours'),
        268: ('Medium Lilac', 'Dark Purple', 'Solid Colours'),
        283: ('Light Nougat', 'Light Flesh', 'Solid Colours'),
        308: ('Dark Brown', 'Dark Brown', 'Solid Colours'),
        312: ('Medium Nougat', 'Medium Dark Flesh', 'Solid Colours'),
        330: ('Olive Green', 'Olive Green', 'Solid Colours'),
        331: ('Medium-Yellowish green', 'Dark Lime; Medium Lime', 'Solid Colours'),
        40: ('Tr. (clear)', '', 'Tr. Colours'),
        41: ('Tr. Red', '', 'Tr. Colours'),
        42: ('Tr. Light Blue', '', 'Tr. Colours'),
        43: ('Tr. Blue', '', 'Tr. Colours'),
        44: ('Tr. Yellow', '', 'Tr. Colours'),
        47: ('Tr. Fluorescent Reddish-Orange (Tr. Dark Orange)', '', 'Tr. Colours'),
        48: ('Tr. Green', '', 'Tr. Colours'),
        49: ('Tr. Fluorescent Green (Tr. Neon Green)', '', 'Tr. Colours'),
        111: ('Tr. Brown (Smoke)', '', 'Tr. Colours'),
        113: ('Tr. Medium Reddish-Violet', '', 'Tr. Colours'),
        126: ('Tr. Bright Bluish-Violet', '', 'Tr. Colours'),
        143: ('Tr. Fluorescent Blue', '', 'Tr. Colours'),
        182: ('Tr. Bright Orange', '', 'Tr. Colours'),
        311: ('Tr. Bright Green', '', 'Tr. Colours'),
        131: ('Silver', 'Pearl Light Grey', 'Special Colours'),
        148: ('Metallic Dark Grey', 'Pearl Dark Grey', 'Special Colours'),
        294: ('Phosphorescent Green', 'Glow In Dark Trans Green', 'Special Colours'),
        297: ('Warm Gold', 'Pearl Gold', 'Special Colours'),
        145: ('Metallic Sand Blue', '', 'Phased out colours'),
        2: ('Grey', '', 'Phased out colours'),
        27: ('Dark Grey', '', 'Phased out colours'),
        153: ('Sand Red', '', 'Phased out colours'),
        136: ('Sand Violet', '', 'Phased out colours'),
        107: ('Bright Bluish Green', '', 'Phased out colours'),
        25: ('Earth Orange', '', 'Phased out colours'),
        104: ('Bright Violet', '', 'Phased out colours'),
    }
    unknown_metadata = ('Unknown', '', 'NA')
    color_metadata = colors_metadata.get(int(material_id), unknown_metadata)
    color_name = '%s: %s' % (material_id, color_metadata[0])

    if color_metadata[0] != color_metadata[1] and color_metadata[1]:
        color_name = '%s (%s)' % (color_name, color_metadata[1])

    color_name = color_name[:29] + (color_name[29:] and '..')

    return {'name': color_name, 'group': color_metadata[2]}

def format_global_color_swatch_rgb(material_id, red, green, blue):
    color_metadata = color_meta_by_material_id(material_id)

    data = {'mode': u'RGB', 'values': [float(red) / 255., float(green) / 255., float(blue) / 255.]}
    swatch = {'data': data, 'name': unicode(color_metadata['name']), 'type': u'Global'}

    return {'swatch': swatch, 'group': color_metadata['group']}


def xml_file_to_swatches(data_set):
    tree = ElementTree.parse(data_set)
    root = tree.getroot()

    swatches_list = []
    swatches_groups = {}

    for mat in root.findall('Material'):
        swatch_data = format_global_color_swatch_rgb(mat.get('MatID'), mat.get('Red'), mat.get('Green'),
                                                     mat.get('Blue'))

        group_key = swatch_data['group']
        swatch = swatch_data['swatch']

        if group_key not in swatches_groups:
            swatches_groups[group_key] = []

        swatches_groups[group_key].append(swatch)

    for group_key in swatches_groups:
        if group_key != 'NA':
            group_dic = {'name': unicode(group_key), 'swatches': swatches_groups[group_key], 'type': u'Color Group'}
            swatches_list.append(group_dic)

    return swatches_list


def main(input_xml, output_ase):
    swatches_list = xml_file_to_swatches(input_xml)
    ai_swatch_helper.write(swatches_list, output_ase)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert Lego Digital Designer colors (materials.xml) into Adobe swatch file (.ase).')
    parser.add_argument('-i', '--materialspath', help='File path to LEGO Digital Designer Materials.xml',
                        default='Materials.xml', dest='input', metavar='INPUTFILE')
    parser.add_argument('-o', '--swatch',
                        help='File path to output Adobe swatches file (must including file name and extension)',
                        default='LDDColors.ase', dest='output', metavar='OUTPUTFILE')
    args = parser.parse_args()
    main(args.input, args.output)
