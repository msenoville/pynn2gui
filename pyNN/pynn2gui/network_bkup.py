from pyNN import network
from . import simulator
from pyNN.common import Population, PopulationView, Projection, Assembly
from itertools import chain

net = network.Network()

class Network(network.Network):
    __doc__ = network.Network.__doc__
    _simulator = simulator

    def __add__(self, other):
        """
        A Network may be added to a Network with the '+' operator, returning a new Network, e.g.::

            n2 = n0 + n1
        """
        ntwk = Network()
        # if isinstance(other, Network):
        #     ntwk.populations.append(self.populations.add(other.populations))
        #     ntwk.views.append(self.views.add(other.views))
        #     ntwk.assemblies.append(self.assemblies.add(other.assemblies))
        #     ntwk.projections.append(self.projections.add(other.projections))
        # elif isinstance(other, Population):
        #     ntwk.populations.append(self.populations.add(other))
        # elif isinstance(other, PopulationView):
        #     ntwk.views.append(self.views.add(other))
        #     ntwk.populations.append(self.populations.add(other.parent))
        # elif isinstance(other, Assembly):
        #     ntwk.assemblies.append(self.assemblies.add(other)
        #     ntwk.populations.append(self.populations.update(other.populations))
        # elif isinstance(other, Projection):
        #     ntwk.projections.append(self.projections.add(other))
        # else:
        #     raise TypeError("can only add a Population, a PopulationView, an Assembly, a Projection, or another Network to a Network")
        if isinstance(other, Network):
            # for obj in chain(other.populations, other.views, other.assemblies, other.projections):
            #     if isinstance(obj, Population):
            #         self.populations.add(obj)
            #     elif isinstance(obj, PopulationView):
            #         self.view.add(obj)
            #     elif isinstance(obj, Assembly):
            #         self.assemblies.add(obj)
            #     elif isinstance(obj, Projection):                   
            #         self.projections.add(obj)
            self.populations.add(other.populations)
            self.views.add(other.views)
            self.assemblies.add(other.assemblies)
            self.projections.add(other.projections)
        elif isinstance(other, Population):
            self.populations.add(other)
        elif isinstance(other, PopulationView):
            self.views.add(other)
            self.populations.add(other.parent)
        elif isinstance(other, Assembly):
            self.assemblies.add(other)
            self.populations.update(other.populations)
        elif isinstance(other, Projection):
            self.projections.add(other)
        else:
            raise TypeError("can only add a Population, a PopulationView, an Assembly, a Projection, or another Network to a Network")
        return self
        # ntwk = Network()

    def __iadd__(self, other):
        """
        A Network may be added to an existing Network using the '+=' operator, e.g.::

            n0 += n
        """

        # if isinstance(other, Network):
        #     # for obj in chain(other.populations, other.views, other.assemblies, other.projections):
        #     #     if isinstance(obj, Population):
        #     #         self.populations.add(obj)
        #     #     elif isinstance(obj, PopulationView):
        #     #         self.view.add(obj)
        #     #     elif isinstance(obj, Assembly):
        #     #         self.assemblies.add(obj)
        #     #     elif isinstance(obj, Projection):                   
        #     #         self.projections.add(obj)
        #     self.populations.add(other.populations)
        #     self.views.add(other.views)
        #     self.assemblies.add(other.assemblies)
        #     self.projections.add(other.projections)
        # elif isinstance(other, Population):
        #     self.populations.add(other)
        # elif isinstance(other, PopulationView):
        #     self.views.add(other)
        #     self.populations.add(other.parent)
        # elif isinstance(other, Assembly):
        #     self.assemblies.add(other)
        #     self.populations.update(other.populations)
        # elif isinstance(other, Projection):
        #     self.projections.add(other)
        # else:
        #     raise TypeError("can only add a Population, a PopulationView, an Assembly, a Projection, or another Network to a Network")
        return self.__class__.__add__(self, other)

