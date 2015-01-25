
from itertools import combinations
from itemsets import singletons_of_itemset, union_of_itemsets, to_index_list
from model import Model
from settings import float_precision

class AssociationRule(object):
    def __init__(self):
        super(AssociationRule, self).__init__()

        # The rule is X -> Y, ie given an X, probability of Y
        self.X = 0
        self.Y = 0
        self.conditional_probability = 0

    def __str__(self):
        return '(%.3f) %s -> %s' % (self.conditional_probability, to_index_list(self.X), to_index_list(self.Y))



def association_rules(model, itemsets, use_observed_frequency=False):
    """
    Mines all association rules for a set of itemsets
    subject to the provided model and its dataset.
    Empty itemsets are ignored
    :param model: Model object
    :param itemsets: Itemsets to mine ruels for
     :param use_observed_frequency: If set to True, association rules will
     be based on the actual frequencies of the itemsets in D. Default is
     to use the estimate frequency of the model
    :return:
    """

    association_rules_set = set()
    association_rules = []

    # If X is very likely and Y is very unlikely
    co_exclusions = []

    # Association rule has X -> Y
    # and probability
    for itemset in itemsets:

        singletons = singletons_of_itemset(itemset)

        for k in range(len(singletons)):
            choose_X = k + 1
            for comb in combinations(singletons, choose_X):

                # comb is a unique subset of the itemset the X in X -> Y we need association rules
                # for all possible Y, ie items in itemset that are not in X

                X = union_of_itemsets(comb)

                prob_X = 0
                if use_observed_frequency:
                    prob_X = model.fr(X)
                else:
                    prob_X = model.query(X)

                Ys = set(singletons) - set(comb)

                for i in range(len(Ys)):
                    choose_Y = i + 1
                    for Y_comb in combinations(Ys, choose_Y):
                        # query X and XY, ie chance of Y given X, is
                        # the chance of X times X and Y
                        Y = union_of_itemsets(Y_comb)

                        # Since we iterate several itemsets,
                        # We may be visiting the same subset several times
                        if not (X, Y) in association_rules_set:
                            association_rules_set.add((X, Y))
                            XY = X | Y
                            prob_XY = 0
                            if use_observed_frequency:
                                prob_XY = model.fr(XY)
                            else:
                                prob_XY = model.query(XY)

                            if prob_X > float_precision:

                                cond_prob = prob_XY / prob_X

                                rule = AssociationRule()
                                rule.X = X
                                rule.Y = Y
                                rule.conditional_probability = cond_prob
                                # tuple of tuple with X,Y and rule
                                association_rules.append(rule)


    # sort by descending probability
    association_rules.sort(lambda ar1, ar2: ar1.conditional_probability < ar2.conditional_probability and 1 or -1)

    return association_rules


# D= [15, 4, 6, 0, 0, 2, 4, 6, 4, 2, 0, 2, 4, 4, 6, 2, 2, 4, 0, 7, 4, 4, 4, 5, 0, 10, 0, 2, 0, 0, 6, 6, 13, 0, 0, 4, 0, 0, 7, 6, 6, 6, 3, 0, 2, 0, 0, 2, 2, 15, 0, 4, 10, 0, 0, 12, 4, 6, 0, 6, 6, 2, 6, 6, 6, 4, 14, 0, 5, 4, 4, 4, 6, 2, 1, 0, 0, 0, 0, 0, 2, 7, 2, 6, 0, 2, 0, 4, 6, 0, 3, 0, 0, 2, 2, 0, 0, 12, 4, 4, 6, 14, 2, 4, 6, 4, 0, 2, 0, 0, 2, 4, 2, 2, 4, 4, 0, 4, 2, 2, 2, 4, 4, 2, 2, 0, 2, 1, 0, 2, 5, 7, 4, 0, 0, 6, 2, 2, 2, 0, 0, 4, 2, 10, 2, 0, 4, 0, 4, 4, 0, 6, 0, 0, 0, 6, 3, 2, 2, 0, 2, 6, 0, 0, 0, 6, 0, 4, 2, 6, 2, 2, 0, 3, 2, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 4, 0, 4, 4, 4, 4, 2, 0, 0, 4, 1, 2, 6, 2, 4, 6, 4, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 0, 10, 0, 0, 4, 0, 0, 0, 0, 6, 4, 0, 0, 6, 4, 0, 6, 12, 0, 4, 0, 2, 0, 0, 4, 2, 6, 4, 4, 12, 4, 2, 2, 4, 4, 4, 0, 0, 2, 2, 2, 6, 4, 0, 0, 4, 4, 0, 0, 4, 8, 4, 6, 6, 0, 2, 4, 4, 0, 6, 6, 4, 0, 4, 6, 0, 0, 0, 2, 4, 0, 4, 0, 4, 0, 4, 6, 4, 0, 2, 2, 0, 4, 0, 0, 6, 8, 2, 2, 0, 0, 4, 6, 6, 2, 2, 0, 0, 2, 6, 0, 0, 2, 0, 0, 0, 0, 4, 4, 0, 9, 6, 4, 4, 6, 0, 0, 0, 6, 4, 2, 4, 2, 7, 0, 0, 6, 4, 6, 4, 4, 4, 0, 0, 0, 0, 4, 6, 6, 0, 8, 6, 4, 4, 15, 6, 6, 0, 4, 4, 4, 6, 4, 4, 2, 2, 0, 6, 6, 2, 11, 6, 0, 4, 6, 6, 4, 0, 6, 13, 0, 6, 6, 0, 10, 9, 6, 7, 0, 12, 6, 6, 6, 5, 0, 2, 2, 7, 0, 5, 0, 1, 2, 9, 2, 4, 0, 0, 6, 0, 0, 0, 0, 6, 6, 2, 2, 0, 0, 2, 2, 0, 4, 0, 0, 4, 4, 4, 0, 4, 0, 6, 4, 0, 2, 2, 2, 2, 0, 6, 2, 14, 4, 0, 0, 4, 2, 6, 0, 6, 2, 0, 6, 0, 4, 4, 0, 0, 12, 4, 6, 0, 6, 6, 6, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 6, 4, 0, 4, 6, 4, 0, 6, 4, 4, 2, 2, 0, 4, 0, 0, 0, 0, 4, 6, 4, 2, 0, 0, 6, 0, 4, 2, 0, 4, 0, 0, 4, 0, 6, 4, 4, 0, 6, 0, 4, 6, 6, 6, 4, 0, 2, 4, 0, 0, 6, 6, 4, 0, 4, 4, 0, 2, 6, 6, 0, 2, 6, 6, 6, 4, 6, 0, 6, 0, 6, 6, 6, 4, 6, 4, 6, 9, 6, 6, 2, 2, 4, 6, 6, 0, 0, 4, 6, 4, 0, 0, 4, 0, 4, 4, 0, 2, 2, 15, 4, 0, 4, 2, 0, 0, 4, 2, 2, 0, 0, 4]
# model = Model(D, s=0.0)
# model.mtv()
# for ar in association_rules(model, model.C):
#     print ar