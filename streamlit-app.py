# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 02:56:08 2022

@author: monar
"""

import streamlit as st
import cirpy
from cirpy import Molecule
import cv2
import molecules_icon_generator as mig

# import the color mapping of the atoms
new_color = mig.color_map

if __name__ == "__main__":
    st.set_page_config(page_title="Molecule icons")
    st.header('''
    Molecule icons generator!
    ''')

    st.text('''
    Generate icons of molecules from Smiles, Names, Cas-number or standard Inchi.
    ''')
    st.markdown(
        "For more options and information, check out the [GitHub repository](https://github.com/lmonari5/molecule-icon-generator.git) with the python module")

    input_type = st.selectbox("Create your icon by",
                              ['name', 'smiles', 'cas_number', 'stdinchi', 'stdinchikey'],
                              help='Chose the input info of your moleculs')
    def_dict = {'name': 'paracetamol',
                'smiles': "CC(=O)Nc1ccc(cc1)O",
                'cas_number': '103-90-2',
                'stdinchi': 'InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)',
                'stdinchikey': 'RZVAJINKPMORJF-UHFFFAOYSA-N'}

    input_string = st.text_input(input_type + ' :', def_dict[input_type])

    single_bonds = st.checkbox('Draw just single_bonds')
    remove_H = st.checkbox('remove all Hydrogens')
    rdkit_draw = st.checkbox('show rdkit structure')
    bw = st.checkbox('black and white')

    img_format = st.selectbox(
        'Download file format:',
        ('svg', 'png', 'jpeg', 'pdf'))

    col1, col2 = st.columns(2)
    with col1:
        atom_color = st.selectbox(
            'Change the color:',
            list(mig.color_map.keys()))
    with col2:
        new_color[atom_color] = st.color_picker(atom_color, mig.color_map[atom_color])

    # catch error when using the cirpy library
    try:
        if input_type == 'name':
            input_string = cirpy.resolve(input_string, 'smiles')
        mol = Molecule(input_string)
        iupac = mol.iupac_name
        if not iupac:
            iupac = 'not found'
        smiles = mol.smiles
    except Exception as e:
        st.write(f'''
        The cirpy python library is not able to resolve your input {input_type}.
        You can use SMILES to skip the cirpy library.
        ''')
        if input_type != 'smiles':
            st.stop()

    if input_type == 'smiles':  # if the input is a smile, use it directly ignoring the cirpy smiles
        smiles = input_string

    try:
        icon_size = st.slider('Atom size', 0, 500, 100,
                              help='''Atom icons size in pixel. Default: 300''')
        pos_multi = st.slider('Image size multiplier', 0, 800, 160,
                              help='''Multiply the position of the atoms with respect to the 2D structure.
                              A higher multiplier leads to higher resolution. Default: 150''')
        if pos_multi > 300:
            st.write('If the images are too big, they are not rendered. They are still available foe download.')
        if not st.button('run'):
            st.stop()
        mig.icon_print(smiles, name='molecular-icon', rdkit_img=rdkit_draw,
                       single_bonds=single_bonds, remove_H=remove_H,
                       position_multiplier=pos_multi, atom_radius=icon_size, bw=bw,
                       atom_color=new_color)
    except Exception as e:
        st.write('''
        Probably Rdkit failed in building the structure of the molecule.
        ''')
        if input_type != 'smiles':
            st.write(f'Try to use the smiles of the molecule instead of {input_type}')
        st.write(f'''Full error:

        {e}''')
        st.stop()

    im_mol = cv2.imread('molecular-icon.jpeg', cv2.IMREAD_UNCHANGED)
    im_rgba = cv2.cvtColor(im_mol, cv2.COLOR_BGRA2RGBA)
    caption_list = ['Iupac name: ' + iupac]

    if rdkit_draw:
        rdkit_img = cv2.imread("molecular-icon_rdkit.png", cv2.IMREAD_UNCHANGED)
        rdkit_img = cv2.cvtColor(rdkit_img, cv2.COLOR_BGRA2RGBA)
        caption_list.append('Rdkit 2D conformation')
        col1, col2 = st.columns(2)
        col1.image(im_rgba, use_column_width=True, channels='RGBA')
        col2.image(rdkit_img, use_column_width=True, channels='RGBA')
    else:
        st.image(im_rgba, use_column_width=True, channels='RGBA')


    filename = 'molecular-icon.' + img_format
    with open(filename, "rb") as file:
        btn = st.download_button(label="Download icon",
                                 data=file,
                                 file_name=filename,
                                 mime=f"image/{img_format}")

    st.write('''
    Thanks for using the Molecules icons generators!
    ''')
