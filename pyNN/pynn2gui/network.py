from pyNN import network
from . import simulator
from pyNN.common import Population, PopulationView, Projection, Assembly
from itertools import chain
import xml.etree.ElementTree as et
import json

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
        header.set('data_cell','_fonction_to_do')
        if id != 0:
            header.set('parent','%s' %(id-1))
        return header
    
    def _cell_desc(self,id,header):
        return

    def _geom_desc(self,id,header):
        return

    def xml_struct(self):
        # create the file structure
        model = et.Element('mxGraphModel')  
        root = et.SubElement(model, 'root')
        for id in 0,1:
            header = et.XML("<mxCell />")
            root.append(header)
            self._header_mxgraph(id,header)
        for i, p in enumerate(self.populations):
            id+=1
            cell = et.SubElement(root, 'mxCell')  
            geom = et.XML("<mxGeometry />")
            cell.append(geom)
            self._cell_desc(id,header)
            self._geom_desc(id,header)
        # item2 = et.SubElement(items, 'item')  
        # item1.set('name','item1') 
        # item1.set('test','test1') 
        # elem.set('nametest','itemtest')  
        # item1.text = 'item1abc'  
        # item2.text = 'item2abc'

        with open('gui_parameters.json') as f:
            data = json.load(f)
        
        for id, p in enumerate(self.populations):
            print(i)
            print(p)
            print(p.celltype.__class__.__name__)
            print(p.celltype.default_parameters)
            for parameter_name in p.celltype.default_parameters:
                print(p.get(parameter_name, gather=True, simplify=True))



        # create a new XML file with the results
        print(model)
        mydata = et.tostring(model)
        print(mydata)
        # myfile = open("items2.xml", "w")  
        # myfile.write(mydata)  

    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Constant', pretty_print=True):
        

        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Constant')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Constant')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Constant', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))

net = Network()


