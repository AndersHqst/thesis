#
# Script to plot likelihood values for a coin toss
#

from matplotlib.pylab import *

def likelihood(outcomes, p_head):
    p_tail = 1 - p_head
    likelihood = 1.0
    for outcome in outcomes:
        if outcome == 0: #tail
            likelihood *= p_tail
        else:
            likelihood *= p_head
    return likelihood
    
def plotCoinToss(outcomes):
    likelihoods = []
    # plot likelihood for probabilities [0;1]
    for p in xrange(0, 101, 1):
        p = p / 100.
        likelihoods.append(likelihood(outcomes, p))
    xlabel('prob. heads')
    ylabel('likelihood')
    plot(likelihoods)
    show()

toss = [1,1,0,1]
plotCoinToss(toss)


