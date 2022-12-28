"""
Standard cells for nest

:copyright: Copyright 2006-2016 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.

"""

from pyNN.standardmodels import cells, build_translations
from .. import simulator


class IF_curr_alpha(cells.IF_curr_alpha):

    __doc__ = cells.IF_curr_alpha.__doc__

    translations = build_translations(
        ('v_rest',     'v_rest'),
        ('v_reset',    'v_reset'),
        ('cm',         'cm'), 
        ('tau_m',      'tau_m'),
        ('tau_refrac', 'tau_refrac'),
        ('tau_syn_E',  'tau_syn_E'),
        ('tau_syn_I',  'tau_syn_I'),
        ('v_thresh',   'v_thresh'),
        ('i_offset',   'i_offset'), 
    )
    gui_name = 'IF_curr_alpha'
    standard_receptor_type = True
    

class IF_curr_exp(cells.IF_curr_exp):
    
    __doc__ = cells.IF_curr_exp.__doc__    
    
    translations = build_translations(
        ('v_rest',     'v_rest'),
        ('v_reset',    'v_reset'),
        ('cm',         'cm'), 
        ('tau_m',      'tau_m'),
        ('tau_refrac', 'tau_refrac'),
        ('tau_syn_E',  'tau_syn_E'),
        ('tau_syn_I',  'tau_syn_I'),
        ('v_thresh',   'v_thresh'),
        ('i_offset',   'i_offset'), 
    )
    gui_name = 'IF_curr_exp'
    standard_receptor_type = True
    

class IF_cond_alpha(cells.IF_cond_alpha):

    __doc__ = cells.IF_cond_alpha.__doc__    

    translations = build_translations(
        ('v_rest',     'v_rest'),
        ('v_reset',    'v_reset'),
        ('cm',         'cm'), 
        ('tau_m',      'tau_m'),
        ('tau_refrac', 'tau_refrac'),
        ('tau_syn_E',  'tau_syn_E'),
        ('tau_syn_I',  'tau_syn_I'),
        ('v_thresh',   'v_thresh'),
        ('i_offset',   'i_offset'), 
        ('e_rev_E',    'e_rev_E'),
        ('e_rev_I',    'e_rev_I'),
    )
    gui_name = 'IF_cond_alpha'
    standard_receptor_type = True
        

class IF_cond_exp(cells.IF_cond_exp):

    __doc__ = cells.IF_cond_exp.__doc__    
    
    translations = build_translations(
        ('v_rest',     'v_rest'),
        ('v_reset',    'v_reset'),
        ('cm',         'cm'), 
        ('tau_m',      'tau_m'),
        ('tau_refrac', 'tau_refrac'),
        ('tau_syn_E',  'tau_syn_E'),
        ('tau_syn_I',  'tau_syn_I'),
        ('v_thresh',   'v_thresh'),
        ('i_offset',   'i_offset'),
        ('e_rev_E',    'e_rev_E'),
        ('e_rev_I',    'e_rev_I'),
    )
    gui_name = 'IF_cond_exp'
    standard_receptor_type = True


class HH_cond_exp(cells.HH_cond_exp):
    
    __doc__ = cells.HH_cond_exp.__doc__    
    
    translations = build_translations(
        ('gbar_Na',    'gbar_Na'),
        ('gbar_K',     'gbar_K'),
        ('g_leak',     'g_leak'),
        ('cm',         'cm'),
        ('v_offset',   'v_offset'),
        ('e_rev_Na',   'e_rev_Na'),
        ('e_rev_K',    'e_rev_K'), 
        ('e_rev_leak', 'e_rev_leak'),
        ('e_rev_E',    'e_rev_E'),
        ('e_rev_I',    'e_rev_I'),
        ('tau_syn_E',  'tau_syn_E'),
        ('tau_syn_I',  'tau_syn_I'),
        ('i_offset',   'i_offset'), 
    )
    gui_name = 'HH_cond_exp'
    standard_receptor_type = True
    
   
class EIF_cond_alpha_isfa_ista(cells.EIF_cond_alpha_isfa_ista):

    __doc__ = cells.EIF_cond_alpha_isfa_ista.__doc__ 

    translations = build_translations(
        ('cm',         'cm'),
        ('tau_refrac', 'tau_refrac'), 
        ('v_spike',    'v_spike'),
        ('v_reset',    'v_reset'),
        ('v_rest',     'v_rest'),
        ('tau_m',      'tau_m'),
        ('i_offset',   'i_offset'),
        ('a',          'a'),
        ('b',          'b'),
        ('delta_T',    'delta_T'),
        ('tau_w',      'tau_w'),
        ('v_thresh',   'v_thresh'),
        ('e_rev_E',    'e_rev_E'),
        ('tau_syn_E',  'tau_syn_E'),
        ('e_rev_I',    'e_rev_I'),
        ('tau_syn_I',  'tau_syn_I'),
    )
    gui_name = 'EIF_cond_alpha_isfa_ista'
    standard_receptor_type = True


class SpikeSourcePoisson(cells.SpikeSourcePoisson):

    __doc__ = cells.SpikeSourcePoisson.__doc__ 

    translations = build_translations(
        ('rate',     'rate'),
        ('start',    'start'),
        ('duration', 'duration'),
    )
    gui_name = 'SpikeSourcePoisson'


def unsupported(parameter_name, valid_value):
    def error_if_invalid(**parameters):
        if parameters[parameter_name].base_value != valid_value:
            raise NotImplementedError("The `{}` parameter is not supported in the GUI App".format(parameter_name))
        return valid_value
    return error_if_invalid


class SpikeSourceArray(cells.SpikeSourceArray):

    __doc__ = cells.SpikeSourceArray.__doc__

    translations = build_translations(
        ('spike_times', 'spike_times'),
    )
    gui_name = 'SpikeSourceArray'


class EIF_cond_exp_isfa_ista(cells.EIF_cond_exp_isfa_ista):
    
    __doc__ = cells.EIF_cond_exp_isfa_ista.__doc__

    translations = build_translations(
        ('cm',         'cm'),  
        ('tau_refrac', 'tau_refrac'), 
        ('v_spike',    'v_spike'),
        ('v_reset',    'v_reset'),
        ('v_rest',     'v_rest'),
        ('tau_m',      'tau_m'),
        ('i_offset',   'i_offset'),
        ('a',          'a'),
        ('b',          'b'),
        ('delta_T',    'delta_T'),
        ('tau_w',      'tau_w'),
        ('v_thresh',   'v_thresh'),
        ('e_rev_E',    'e_rev_E'),
        ('tau_syn_E',  'tau_syn_E'),
        ('e_rev_I',    'e_rev_I'),
        ('tau_syn_I',  'tau_syn_I'),
    )
    gui_name = 'EIF_cond_exp_isfa_ista'
    standard_receptor_type = True
