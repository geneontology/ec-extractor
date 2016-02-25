# EC extractor

Extracts an entry from KEGG and writes a new GO stanza

## Usage

    python3 add-ec-to-go.py ec:2.6.1.86 ec:2.6.1.87

Generates output:

```
[Term]
id: 
name: 2-amino-4-deoxychorismate synthase activity
def: "Catalysis of the reaction: (2S)-2-amino-4-deoxychorismate + L-glutamate = chorismate + L-glutamine [RN:R08956]" [EC:2.6.1.86]
synonym: "ADIC synthase" EXACT [EC:2.6.1.86]
synonym: "2-amino-2-deoxyisochorismate synthase" EXACT [EC:2.6.1.86]
synonym: "SgcD" EXACT [EC:2.6.1.86]
is_a: GO:0008483 ! transaminase activity
```

## Requirements

Python3
BioPython

```
pip3 install biopython
```

## TODO

How should this be used in practice?

As a quick hack, the editor can run the script, hand-add an ID in their ID space, and paste into file

A preferred route would be instead to have a TSV

```
GO:3000000 2.6.1.86
GO:3000001 2.6.1.87
```

This would be the 'source'

A pipeline would generate a module that could be imported (preferred) or generated and inserted.

OBO-Edit is the obstacle to the former
