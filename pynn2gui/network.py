import pyNN
from pyNN import network
from pynn2gui import simulator
# from .populations import Population, PopulationView, Assembly
# from .projections import Projection
# from pyNN.common import Population, PopulationView, Projection, Assembly
from itertools import chain
import xml.etree.ElementTree as et
import json
import os
import re
import copy
import pprint as pp
import xml.dom.minidom as md
from xml.dom.minidom import Text, Element
import numpy as np

# TO DO: modify strings inputs sometimes


class Network(network.Network):
    __doc__ = network.Network.__doc__
    _simulator = simulator

    def __add__(self, other):
        """
        A Network may be added to a Network with the '+' operator, returning a new Network, e.g.::

            n2 = n0 + n1
        """
        if isinstance(other, Network):
            for obj in chain(other.populations, other.views, other.assemblies, other.projections):
                if isinstance(obj, Population):
                    self.populations.add(obj)
                elif isinstance(obj, PopulationView):
                    self.views.add(obj)
                elif isinstance(obj, Assembly):
                    self.assemblies.add(obj)
                elif isinstance(obj, Projection):                   
                    self.projections.add(obj)
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

    def __iadd__(self, other):
        """
        A Network may be added to an existing Network using the '+=' operator, e.g.::

            n0 += n
        """
        if isinstance(other, Network):
            for obj in chain(other.populations, other.views, other.assemblies, other.projections):
                if isinstance(obj, Population):
                    self.populations.add(obj)
                elif isinstance(obj, PopulationView):
                    self.views.add(obj)
                elif isinstance(obj, Assembly):
                    self.assemblies.add(obj)
                elif isinstance(obj, Projection):                   
                    self.projections.add(obj)
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
        # return self.__class__.__add__(self, other)

    def _sorted_geom(self):
        # sorted_list = np.array([[None],[None],[None]], dtype=list)
        exc = []
        inh = []
        stim = []
        for p in self.projections:
            if p.receptor_type == 'inhibitory' and p.pre.label not in inh:
                inh.append(p.pre.label)
        for p in self.populations:
            if 'standard_receptor_type' in p.celltype.__class__.__dict__ and p.label not in inh:
                exc.append(p.label)
            elif p.label not in inh:
                stim.append(p.label)
        exc = sorted(exc)
        inh = sorted(inh)
        stim = sorted(stim)
        # print(exc, inh, stim)
        return exc, inh, stim

    def _header_mxgraph(self,id,header):
        header.set('id','%s' %(id))
        header.set('data_cell','{celltype: empty_no_edge}')
        if id != 0:
            header.set('parent','%s' %(id-1))
        return header
    
    def _data_cell_description(self, p, data):
        desc = ''
        desc += '{'
        for d in data[p]:
            if data[p][d] is "":
                desc += '&quot;%s&quot;:&quot;&quot;,' % d
            elif isinstance(data[p][d],str):
                desc += '&quot;%s&quot;:&quot;%s&quot;,' %(d, data[p][d])
            else:
                desc += '&quot;%s&quot;:%s,' %(d, data[p][d])
        desc = desc[:-1]
        desc += '}'
        return desc

    def _cell_desc(self,id,p,cell,data):
        obj = 'population'
        color = ['red','blue','orange']
        font = ['white', 'white', 'black']
        source = target = int()
        if isinstance(p, Population):
            obj = 'population'
            for test in (0, 1, 2):
                if p.label in self._sorted_geom()[test]:
                    r = test
            cell.set('vertex', str(1))
            cell.set('style','fontColor=%s;fillColor=%s' %(font[r],color[r]))
        elif isinstance(p, Projection):
            obj = 'projection'
            for i, pop in enumerate(self.populations):
                if pop == p.pre:
                    source = i + 2
                if pop == p.post:
                    target = i + 2
            cell.set('edge','%s' %(1)) # maybe on to-do list, wip
            cell.set('source', str(source))
            cell.set('target', str(target))
        cell.set('id','%s' %(id))
        cell.set('value','%s' % data[obj]['name_value'])
        cell.set('data_cell', '%s' %self._data_cell_description(obj, data))
        cell.set('parent','%s' %(1))
        return cell

    def _geom_desc(self,id,p,geom): # to do, wip
        x = [230, 430, 30]
        y = [90, 90, 30]
        height = 30
        width = 80
        gap = 60
        geom.set('as','geometry')
        if isinstance(p, Population):
            sort = self._sorted_geom()
            for r in (0, 1, 2):
                if p.label in sort[r]:
                    r_type = r
            i = sort[r_type].index(p.label)
            geom.set('x',str(x[r_type]))
            geom.set('y',str(y[r_type]+i*(height+gap)))
            geom.set('width', str(width))
            geom.set('height', str(height))
        if isinstance(p, Projection):
            geom.set('relative',str(1))
        return geom

    def _load_data_description(self):
        path = os.path.dirname(pyNN.__file__)
        with open('%s/pynn2gui/gui_parameters.json' % path) as f:
            data = json.load(f)
        return data

    def _matching_search(self, p, parameter_name, value, data):
        obj = 'population'
        if isinstance(p, Population):
            obj = 'population'
        elif isinstance(p, Projection):
            obj = 'projection'
        match = ''
        max_score = 0.
        score = 0.
        for d in data[obj]:
            found = re.search(parameter_name,d)
            if found:
                score = (found.end()-found.start())/len(d)
            else:
                score = 0
            if score > max_score:
                max_score = score
                match = d
        data[obj][match] = value
        return data  

    def _data_update(self,data,p):
        if isinstance(p, Population):
            obj = 'population'
            data[obj]['size'] = p.size
            data[obj]['celltype'] = p.celltype.__class__.__name__
            # data[obj]['label'] = p.label
            data[obj]['name_value'] = p.label
            for parameter_name in p.celltype.default_parameters:
                value = p.get(parameter_name, gather=True, simplify=True)
                self._matching_search(obj, parameter_name, None, data)
        elif isinstance(p, Projection):
            obj = 'projection'
            data[obj]['connectors_type'] = p._connector.__class__.__name__
            data[obj]['receptor_type'] = p.receptor_type
            data[obj]['synapse_type'] = p.synapse_type.__class__.__name__
            data[obj]['name_value'] = p.label.replace('→','_to_')
            for parameter_name in p.synapse_type.default_parameters:
                value = p.get(parameter_name, 'array', gather=True,  with_address=True, multiple_synapses='first')[0][0]
                self._matching_search(obj, parameter_name, value, data)
            for parameter_name, value in p._connector.get_parameters().items():
                self._matching_search(obj, parameter_name, value, data)
        return data

    def xml_struct(self):
        # loading the decription of PyNN objects
        data = self._load_data_description()

        # create the file structure
        model = et.Element('mxGraphModel')  
        root = et.SubElement(model, 'root')
        for id in 0,1:
            header = et.XML("<mxCell />")
            root.append(header)
            self._header_mxgraph(id,header)
        for p in chain(self.populations, self.projections):
            desc = copy.copy(data)
            self._data_update(desc,p)
            id+=1
            cell = et.SubElement(root, 'mxCell')  
            geom = et.XML("<mxGeometry />")
            cell.append(geom)
            self._cell_desc(id,p,cell,desc)
            self._geom_desc(id,p,geom)
        for item in model.findall("mxCell"):
            print('found', et.dump(item))
        xml_tree = et.ElementTree(model)

        # create a new XML file with the results
        # print(model)
        # mydata = str(et.tostring(model))
        # print(mydata)
        # myfile = open("test_gui.xml", "w")  
        # myfile.write(str(mydata))
        # xml_tree.write("test_gui.xml", encoding="utf-8", method='text')
        stringlist = et.tostring(model, 'utf-8', method="html")
        st1 = str(stringlist)
        reparsed = md.parseString(stringlist)
        # st1 = reparsed.toxml()
        st3= reparsed.toprettyxml(indent="   ")
        st2 = st1.replace('&amp;quot;','&quot;')
        st2 = st2[2:-1]
        # st2.replace("<?xml version=\"1.0\" ?>",'')
        print(st3)
        myfile = open("test_gui.xml", "w")  
        myfile.write(st2)


        # self.xmlprettyprint(xml_tree)

net = Network()


