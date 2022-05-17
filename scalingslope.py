# import stuff

from rdkit import Chem
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import asc

# define the two surfaces of study
SURFACE1 = 'Ag12'
SURFACE2 = 'Cu12'

# load in the binding energies of elements df
df_be = pd.read_csv('dft_binding_energies.csv')

# save the pure metal ones to a separate df
df_be_pure = df_be.loc[df_be['chemicalComposition'].str.contains('12', case=False)]

# pure metal surface names
dfarray = df_be_pure.to_numpy()
elementnames = dfarray[:,0]


def slopefrommol(m):
    # returns the scaling slope given a mol molecule object
    return

def naive_scaling(elements, multiplicity=1, saturation=1):
    # elements: dictionary of heteroatoms and their count in the molecule
    # multiplicity: number of atoms bound to surface
    # saturation: degree of saturation of the atom bound to surface. Number of bonds the atom can form to surface. Things that increase this is
    # number of double bonds and bonds to hydrogen.

    if atom == 'C':
        valency = 4
    elif atom == 'N':
        valency = 3
    elif atom == 'O':
        valency = 2
    elif atom == 'S':
        valency = 2
    
    slope = saturation * multiplicity / valency
    

    return slope

def countelements(m):
    elements = {'C': 0, 'N': 0, 'O': 0, 'S': 0}
    # also keep track of the total saturation of the heteroatom, via 
    for atom in m.GetAtoms():
        if atom.GetAtomicNum() == 6:
            elements['C'] += 1
        elif atom.GetAtomicNum() == 7:
            elements['N'] += 1
        elif atom.GetAtomicNum() == 8:
            elements['O'] += 1
        elif atom.GetAtomicNum() == 16:
            elements['S'] += 1
    return elements

def scalingslope(m):
    # keeps track of the naive scaling slope of a molecule
    slope = {'C': 0, 'N': 0, 'O': 0, 'S': 0}
    for atom in m.GetAtoms():
        if atom.GetAtomicNum() == 6:
            slope['C'] += (1 - atom.GetDegree()/4)
        elif atom.GetAtomicNum() == 7:
            slope['N'] += (1 - atom.GetDegree()/3)
        elif atom.GetAtomicNum() == 8:
            slope['O'] += (1 - atom.GetDegree()/2)
        elif atom.GetAtomicNum() == 16:
            slope['S'] += (1 - atom.GetDegree()/2)
    return slope
        



if __name__ == '__main__':
    # import csv as pd
    df = pd.read_csv('cleanedmolecules2.csv') # contains ~4000 molecules that contain N, O, S.

    #  convert all molecules in df2 to molecule object of rdkit
    df['Mol'] = df['SMILES'].apply(Chem.MolFromSmiles)
    df['heterocount'] = df['Mol'].apply(countelements)
    df['naivescaling'] = df['Mol'].apply(scalingslope)

    df = pd.concat([df, df['naivescaling'].apply(pd.Series)], axis=1)
    #df.to_csv('test.csv')

    # generate binding energy plots, for all surfaces and for pure metal surfaces
    
    plt.scatter(df_be['nbind'], df_be['obind'])
    plt.scatter(df_be_pure['nbind'], df_be_pure['obind'])
    #plt.xlim([-1,7])
    #plt.ylim([-5,4])
    plt.ylabel('oxygen binding energy (ev)')
    plt.xlabel('nitrogen binding energy (ev)')

    

    # generate labels for pure surfaces
    x = df_be_pure['nbind'].to_numpy()
    y = df_be_pure['obind'].to_numpy()
    for i, txt in enumerate(elementnames):
        plt.annotate(txt, (x[i], y[i]))

    plt.savefig("test.png")
    
    # calculate the best scaling slope molecules for N, S, and O

    # for O we sort by 'O' column for best scaling slopes
    dfsorto = df.sort_values(by=['O'], ascending=False, ignore_index=True)[0:50]
    dfsorto.to_csv('oxygencandidates.csv')

    # for S we sort by 'S' column for best scaling slopes
    dfsorts = df.sort_values(by=['S'], ascending=False, ignore_index=True)[0:50]
    dfsorts.to_csv('sulfurcandidates.csv')

    # for N we sort by 'N' column for best scaling slopes
    dfsortn = df.sort_values(by=['N'], ascending=False, ignore_index=True)[0:50]
    dfsortn.to_csv('nitrogencandidates.csv')

    # plot best oxygen candidates x = scaling slope, y = melting point,// z = molar mass
    #print(dfsorto['Melting Point: Melting Point [C]'].str.split().str[0].astype(float))
    '''
    dfsorto['melt'] = dfsorto['Melting Point: Melting Point [C]'].str.split().str[0].astype(float)
    plt.scatter(dfsorto['O'], dfsorto['melt'])
    plt.xlim([0,4.5])
    plt.title('oxygen-based inhibitors')
    plt.xlabel('scaling slope')
    plt.ylabel('melting point [C]')
    plt.savefig("test.png")
    '''

    '''
    # generate Hacac vs o-phosphoric acid scaling relation vs pure metals
    plt.scatter(df_be_pure['obind'], df_be_pure['obind'])
    plt.scatter(df_be_pure['obind'], 3*df_be_pure['obind'])
    plt.xlabel('Oxygen binding energy')
    plt.ylabel('Molecule adsorption energy')
    plt.title('Hacac vs o-phosphoric acid')
    plt.savefig("test.png")
    '''
