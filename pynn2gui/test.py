from pyNN import pynn2gui as sim

print(sim.network.net.__dict__)

sim.setup(timestep=0.01, min_delay=1.0)

cuba_exp = sim.Population(1, sim.IF_curr_exp(i_offset=1.0, v_thresh=-20.), label="IF_curr_exp_1")
coba_exp = sim.Population(2, sim.IF_curr_exp(i_offset=1.0, v_thresh=-20.), label="IF_curr_exp_2")
# coba_exp_bis = sim.Population(3, sim.IF_curr_exp(i_offset=1.0, v_thresh=-20.), label="IF_curr_exp_3")
# coba_exp_ter = sim.Population(4, sim.IF_curr_exp(i_offset=1.0, v_thresh=-20.), label="IF_curr_exp_4")

prj = sim.Projection(cuba_exp, coba_exp, sim.AllToAllConnector(),sim.StaticSynapse(weight=0.123))

print(sim.network.net.__dict__)


# net = sim.network.Network(cuba_exp + coba_exp) 
# n3 = sim.network.Network(coba_exp_ter)
# n2 = net + prj 
# print("n2.__dict_ for add")
# print(n2.__dict__)
# n2 += coba_exp_bis
# print("n2.__dict__ for iadd")
# print(n2.__dict__)
# n4 = n3 + n2
# print("n4.__dict__ after iadd")
# print(n4.__dict__)
# n3 += net
# print("n3.__dict__ after iadd net")
# print(n3.__dict__)