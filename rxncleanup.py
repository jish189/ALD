import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# this script cleans up the raw csv export from catalyst-hub.org from
# the catahub.py script


def cleanup(csvfile):

    # load csv file of raw export from catlyst-hub.org

    df = pd.read_csv(csvfile)

    # drop the duplicate energies, keeping the reaction with lowest energy
    df = df.drop_duplicates(subset=['chemicalComposition', 'Equation'])
    df = df.sort_values(by=['Equation', 'chemicalComposition', 'reactionEnergy'])

    