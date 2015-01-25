
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
        self.confidence = 0
        self.lift = 0

    def __str__(self):
        return '(conf:%.3f, lift:%.3f) %s -> %s' % (self.confidence, self.lift, to_index_list(self.X), to_index_list(self.Y))



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

    # Since we iterate several itemsets,
    # we may visit the same subsets X,Y several times
    # so we track visited nodes to avoid dublicates
    association_rules_set = set()

    # List of all possible rules
    # that come from all subsets of the
    # itemsets
    rules = []

    for itemset in itemsets:

        singletons = singletons_of_itemset(itemset)

        for k in range(len(singletons)):
            choose_X = k + 1
            for comb in combinations(singletons, choose_X):

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

                        Y = union_of_itemsets(Y_comb)

                        if not (X, Y) in association_rules_set:
                            association_rules_set.add((X, Y))
                            XY = X | Y
                            prob_XY = 0
                            prob_Y = 0
                            if use_observed_frequency:
                                prob_XY = model.fr(XY)
                                prob_Y = model.fr(Y)
                            else:
                                prob_XY = model.query(XY)
                                prob_Y = model.query(Y)

                            if prob_X > float_precision and prob_Y > float_precision:

                                conf = prob_XY / prob_X
                                lift = conf / prob_Y

                                rule = AssociationRule()
                                rule.X = X
                                rule.Y = Y
                                rule.confidence = conf
                                rule.lift = lift
                                rules.append(rule)


    # Return sorted list, regading the rules as
    # either association or disassociation rules
    # Association rules, descending prob, lift > 1 for true rules
    association_rules = filter(lambda rule: rule.lift > 1, rules)
    association_rules.sort(lambda ar1, ar2: ar1.confidence < ar2.confidence and 1 or -1)

    # Disassociation rules, ascending prob, lift < 1 for true rules
    disassociation_rules = filter(lambda rule: rule.lift < 1, rules)
    disassociation_rules.sort(lambda ar1, ar2: ar1.confidence < ar2.confidence and -1 or 1)

    return association_rules, disassociation_rules


#
# Debug code
#
# D= [15, 4, 6, 0, 0, 2, 4, 6, 4, 2, 0, 2, 4, 4, 6, 2, 2, 4, 0, 7, 4, 4, 4, 5, 0, 10, 0, 2, 0, 0, 6, 6, 13, 0, 0, 4, 0, 0, 7, 6, 6, 6, 3, 0, 2, 0, 0, 2, 2, 15, 0, 4, 10, 0, 0, 12, 4, 6, 0, 6, 6, 2, 6, 6, 6, 4, 14, 0, 5, 4, 4, 4, 6, 2, 1, 0, 0, 0, 0, 0, 2, 7, 2, 6, 0, 2, 0, 4, 6, 0, 3, 0, 0, 2, 2, 0, 0, 12, 4, 4, 6, 14, 2, 4, 6, 4, 0, 2, 0, 0, 2, 4, 2, 2, 4, 4, 0, 4, 2, 2, 2, 4, 4, 2, 2, 0, 2, 1, 0, 2, 5, 7, 4, 0, 0, 6, 2, 2, 2, 0, 0, 4, 2, 10, 2, 0, 4, 0, 4, 4, 0, 6, 0, 0, 0, 6, 3, 2, 2, 0, 2, 6, 0, 0, 0, 6, 0, 4, 2, 6, 2, 2, 0, 3, 2, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 4, 0, 4, 4, 4, 4, 2, 0, 0, 4, 1, 2, 6, 2, 4, 6, 4, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 0, 10, 0, 0, 4, 0, 0, 0, 0, 6, 4, 0, 0, 6, 4, 0, 6, 12, 0, 4, 0, 2, 0, 0, 4, 2, 6, 4, 4, 12, 4, 2, 2, 4, 4, 4, 0, 0, 2, 2, 2, 6, 4, 0, 0, 4, 4, 0, 0, 4, 8, 4, 6, 6, 0, 2, 4, 4, 0, 6, 6, 4, 0, 4, 6, 0, 0, 0, 2, 4, 0, 4, 0, 4, 0, 4, 6, 4, 0, 2, 2, 0, 4, 0, 0, 6, 8, 2, 2, 0, 0, 4, 6, 6, 2, 2, 0, 0, 2, 6, 0, 0, 2, 0, 0, 0, 0, 4, 4, 0, 9, 6, 4, 4, 6, 0, 0, 0, 6, 4, 2, 4, 2, 7, 0, 0, 6, 4, 6, 4, 4, 4, 0, 0, 0, 0, 4, 6, 6, 0, 8, 6, 4, 4, 15, 6, 6, 0, 4, 4, 4, 6, 4, 4, 2, 2, 0, 6, 6, 2, 11, 6, 0, 4, 6, 6, 4, 0, 6, 13, 0, 6, 6, 0, 10, 9, 6, 7, 0, 12, 6, 6, 6, 5, 0, 2, 2, 7, 0, 5, 0, 1, 2, 9, 2, 4, 0, 0, 6, 0, 0, 0, 0, 6, 6, 2, 2, 0, 0, 2, 2, 0, 4, 0, 0, 4, 4, 4, 0, 4, 0, 6, 4, 0, 2, 2, 2, 2, 0, 6, 2, 14, 4, 0, 0, 4, 2, 6, 0, 6, 2, 0, 6, 0, 4, 4, 0, 0, 12, 4, 6, 0, 6, 6, 6, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 6, 4, 0, 4, 6, 4, 0, 6, 4, 4, 2, 2, 0, 4, 0, 0, 0, 0, 4, 6, 4, 2, 0, 0, 6, 0, 4, 2, 0, 4, 0, 0, 4, 0, 6, 4, 4, 0, 6, 0, 4, 6, 6, 6, 4, 0, 2, 4, 0, 0, 6, 6, 4, 0, 4, 4, 0, 2, 6, 6, 0, 2, 6, 6, 6, 4, 6, 0, 6, 0, 6, 6, 6, 4, 6, 4, 6, 9, 6, 6, 2, 2, 4, 6, 6, 0, 0, 4, 6, 4, 0, 0, 4, 0, 4, 4, 0, 2, 2, 15, 4, 0, 4, 2, 0, 0, 4, 2, 2, 0, 0, 4]
# model = Model(D, s=0.0)
# model.mtv()
# association_rules, disassociation_rules = association_rules(model, model.C)
# print 'Association rules'
# for ar in association_rules:
#     print ar
#
# print '\nDisassociation rules'
# for ar in disassociation_rules:
#     print ar

print 'done'