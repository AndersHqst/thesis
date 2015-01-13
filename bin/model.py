class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.u0 = 0
        self.U = {}
        self.C = []
        self.heurestics = {}
        self.BIC_scrores = {}
        self.G = None
        self.T_c = []
        self.total_weight = None