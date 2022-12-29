
# coding: utf-8
#!python

import numpy
import pyNN.neuroml as sim
from pyNN.random import RandomDistribution

sim.setup()

pop_5 = sim.Population(1, sim.IF_curr_alpha(v_rest=-65, cm=1, tau_m=20, tau_refrac=0, tau_syn_E=5, tau_syn_I=5, i_offset=0, v_reset=-65, v_thresh=-50 ), label='Pop1')
pop_5.initialize(v=-65)
pop_5.record('spikes')
pop_6 = sim.Population(1, sim.SpikeSourcePoisson(rate=100, start=0, duration=10000000000))
prj_7 = sim.Projection(pop_6, pop_5, sim.AllToAllConnector(), sim.StaticSynapse(weight=0.1, delay=0.1), receptor_type='excitatory')

sim.run(10)

pop_5.write_data("test_pop_4.pkl")

sim.end()
