"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

def process_section(regex, mddata, default=''):
    var = re.split(regex, mddata)
    if len(var) == 3:
        return var[0] + var[1], var[2] #
    else:
        return default, mddata

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    # xmldata = mddata
    
    # Splitting and processing sections
    entete, mddata = process_section(r'(DU \d+ \w* \d{4})', mddata)
    expose, mddata = process_section(r'(Sur le rapport)', mddata)
    motivation, mddata = process_section(r'(Examen d.*moyens?)', mddata)
    moyens, mddata = process_section(r'(PAR CES MOTIFS.*la Cour :|EN CONSÉQUENCE.*la Cour :)', mddata, None)
    dispositif = mddata

    # Setting dispositif section
    dispositif = mddata

    # Creating xml data
    xmldata = [f'<Entête>{entete}</Entête>', f'<Exposé_du_litige>{expose}</Exposé_du_litige>',
            f'<Motivation>{motivation}</Motivation>', f'<Moyens>{moyens}</Moyens>',
            f'<Dispositif>{dispositif}</Dispositif>']

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.extend(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 