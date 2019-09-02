import pyNN
from pyNN import network
from . import simulator
from pyNN.common import Population, PopulationView, Projection, Assembly
from itertools import chain
import xml.etree.ElementTree as et
import json
import os
import re
import copy
import pprint as pp
import xml.dom.minidom as md


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
        return self.__class__.__add__(self, other)
    
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
            desc += '%s:%s,' %(d, data[p][d])
        desc = desc[:-1]
        desc += '}'
        return desc

    def _cell_desc(self,id,p,cell,data):
        obj = 'population'
        if isinstance(p, Population):
            obj = 'population'
            cell.set('vertex','%s' %(1))
        elif isinstance(p, Projection):
            obj = 'projection'
            for i, pop in enumerate(self.populations):
                if pop == p.pre:
                    source = i + 2
                elif pop == p.post:
                    target = i + 2
            cell.set('edge','%s' %(1)) # maybe on to-do list, wip
            cell.set('source','%s' %(source))
            cell.set('target','%s' %(target))
        cell.set('id','%s' %(id))
        cell.set('value','%s' % data[obj]['name_value'])
        cell.set('data_cell', '%s' %self._data_cell_description(obj, data))
        cell.set('parent','%s' %(1))
        return cell

    def _geom_desc(self,id,p,geom): # to do, wip
        geom.set('x','420')
        geom.set('y','255')
        geom.set('width','80')
        geom.set('height','30')
        geom.set('as','geometry')
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
            data[obj]['name_value'] = p.label.replace('→','_2_')
            for parameter_name in p.synapse_type.default_parameters:
                value = p.get(parameter_name, 'array', gather=True,  with_address=True, multiple_synapses='first')[0][0]
                self._matching_search(obj, parameter_name, value, data)
            for parameter_name, value in p._connector.get_parameters().items():
                self._matching_search(obj, parameter_name, value, data)
        return data

    # def _xmlprettyprint(self, stringlist):
    #     indent = ''
    #     in_tag = False
    #     for token in stringlist:
    #         if token.startswith('</'):
    #             indent = indent[:-2]
    #             yield indent + token + '\n'
    #             in_tag = True
    #         elif token.startswith('<'):
    #             yield indent + token
    #             indent += '  '
    #             in_tag = True
    #         elif token == '>':
    #             yield '>' + '\n'
    #             in_tag = False
    #         elif in_tag:
    #             yield token
    #         else:
    #             yield indent + token + '\n'

    # def xmlprettyprint(self, element):
    #     return ''.join(self._xmlprettyprint(et.tostringlist(element)))

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
        xml_tree.write("test_gui.xml")
        stringlist = et.tostring(model, 'utf-8')
        reparsed = md.parseString(stringlist)
        st = reparsed.toprettyxml(indent="    ")
        print(st)

        # self.xmlprettyprint(xml_tree)


# if __name__ == '__main__':
#     e = ElementTree.fromstring('<foo><bar>joe'
#                                '<baz name="sue">eve</baz>'
#                                '</bar></foo>')
#     print xmlprettyprint(e)

    # def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Constant', pretty_print=True):
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


