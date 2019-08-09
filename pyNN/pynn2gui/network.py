import pyNN
from pyNN import network
from . import simulator
from pyNN.common import Population, PopulationView, Projection, Assembly
from itertools import chain
import xml.etree.ElementTree as et
import json
import os
import re

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
                    self.view.add(obj)
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
        return self.__class__.__add__(self, other)
    
    def _header_mxgraph(self,id,header):
        header.set('id','%s' %(id))
        header.set('data_cell','{celltype: empty_no_edge}')
        if id != 0:
            header.set('parent','%s' %(id-1))
        return header
    
    def _cell_desc(self,id,cell,data):
        cell.set('id','%s' %(id))
        cell.set('value','%s' %())
        cell.set('data_cell', '%s' % _data_cell_description(data))
        cell.set('vertex','%s' %(1))
        cell.set('parent','%s' %(1))
        return cell

    def _geom_desc(self,id,geom):
        return

    def _data_cell_description(self, data):
        desc = ''
        desc += '{'
        desc += 'name_value:%s' % 
        desc += 'celltype:%s' % 
        desc = ',%s:%s' %()
        dec += '}'
        return desc


    def _load_data_description(self):
        path = os.path.dirname(pyNN.__file__)
        with open('%s/pynn2gui/gui_parameters.json' % path) as f:
            data = json.load(f)
        return data

    def _data_update(self,data,pop):
        data[]
        for parameter_name in population.celltype.default_parameters:
            match = ''
            max_score = 0.
            score = 0.
            for d in data['population']:
                found = re.search(parameter_name,d)
                if found:
                    score = (found.end()-found.start())/len(d)
                else:
                    score = 0
                if score > max_score:
                    max_score = score
                    match = d
            data['population'][match] = pop.get(parameter_name, gather=True, simplify=True)
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
        for i, p in enumerate(self.populations):
            desc = copy(data)
            self._data_update(desc,p)
            id+=1
            cell = et.SubElement(root, 'mxCell')  
            geom = et.XML("<mxGeometry />")
            cell.append(geom)
            self._cell_desc(id,cell,desc)
            self._geom_desc(id,geom)
        # item2 = et.SubElement(items, 'item')  
        # item1.set('name','item1') 
        # item1.set('test','test1') 
        # elem.set('nametest','itemtest')  
        # item1.text = 'item1abc'  
        # item2.text = 'item2abc'
        
        # for id, p in enumerate(self.populations):
        #     # print(i)
        #     # print(p)
        #     # print(p.celltype.__class__.__name__)
        #     # print(p.celltype.default_parameters)
        #     for parameter_name in p.celltype.default_parameters:
        #         match = ''
        #         max_score = 0.
        #         score = 0.
        #         for d in data['population']:
        #             found = re.search(parameter_name,d)
        #             if found:
        #                 score = (found.end()-found.start())/len(d)
        #             else:
        #                 score = 0
        #             if score > max_score:
        #                 max_score = score
        #                 match = d
        #         # print(match,parameter_name)
        #         data['population'][match] = p.get(parameter_name, gather=True, simplify=True)
        #     print(data)

        # create a new XML file with the results
        print(model)
        mydata = et.tostring(model)
        print(mydata)
        # myfile = open("items2.xml", "w")  
        # myfile.write(mydata)  

    # def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Constant', pretty_print=True):
        

    #     imported_ns_def_ = GenerateDSNamespaceDefs_.get('Constant')
    #     if imported_ns_def_ is not None:
    #         namespacedef_ = imported_ns_def_
    #     if pretty_print:
    #         eol_ = '\n'
    #     else:
    #         eol_ = ''
    #     if self.original_tagname_ is not None:
    #         name_ = self.original_tagname_
    #     showIndent(outfile, level, pretty_print)
    #     outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
    #     already_processed = set()
    #     self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Constant')
    #     if self.hasContent_():
    #         outfile.write('>%s' % (eol_, ))
    #         self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Constant', pretty_print=pretty_print)
    #         outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
    #     else:
    #         outfile.write('/>%s' % (eol_, ))

net = Network()


