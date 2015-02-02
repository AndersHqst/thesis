from utils.dataset_helpers import *
from matplotlib.pylab import plot, hist, ylabel, xlabel, savefig, close, title, figtext
from preprocessing.discretization import *
from scipy.stats import tvar
import os
def plot_bacteria_hist(dataset, folder, mid_quantile=False):
    """
    Saves a histogram of abundances binned
    :return:
    """

    # Get the transposed abundances matrix
    abundances = abundance_matrix(dataset).T

    # Get header names to priint on the plots
    headers = dataset[0][2:]

    for index, bacteria_column  in enumerate(abundances):

        abundances = [float(x) for x in bacteria_column]

        if mid_quantile:
            abundances.sort()
            abundances = abundances[int(len(abundances)*0.25): -int(len(abundances)*0.25)]

        xlabel('relative abundance bin')
        ylabel('#occurrences')

        bacteria_name = headers[index]
        title(bacteria_name)
        bins, intervals, patches = hist(abundances, color='#0066FF')

        # Write discretized values
        threshold = 0.5
        discretized_abundances = discrete_abundances(abundances, threshold=threshold)
        _0 = '0: ' + str(len([x for x in discretized_abundances if x == 0]))
        _1 = '1: ' + str(len([x for x in discretized_abundances if x == 1]))

        relatve_threshold = discrete_relative_threshold(abundances, threshold)
        threshold_text = 'Threshold: %f' % relatve_threshold
        figtext(0.7, 0.90, threshold_text, fontsize=10)
        figtext(0.7, 0.85, _0, fontsize=10)
        figtext(0.7, 0.80, _1, fontsize=10)

        # Draw threshold line
        a, b = [relatve_threshold, relatve_threshold], [0, max(bins)]
        plot(a, b, c='r')

        # Write max and avg
        max_abundance = 'max: %f' % max(abundances)
        avg_abundance = 'avg: %f' % (sum(abundances) / float(len(abundances)))
        figtext(0.7, 0.75, max_abundance, fontsize=10)
        figtext(0.7, 0.70, avg_abundance, fontsize=10)

        # write variance
        variance = 'var: %f' % tvar(abundances)
        figtext(0.7, 0.65, variance, fontsize=10)

        # Save fig to folder
        folder_path = os.path.join(dir, '../../experiments/' + folder)
        if not (os.path.exists(folder_path)):
            os.makedirs(folder_path)
        savefig(folder_path + '-' + bacteria_name.replace('/','-').replace('|', '-'))

        close()
