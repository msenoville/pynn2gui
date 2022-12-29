Python module to export any PyNN script to the PyNN graphical model builder (PyNN GUI).

This module is an extension of pyNN.mock module which is a mock simulator backend of the PyNN API that may be used for testing and documentation purposes. of the PyNN API.

This backend implements the PyNN API, but was developped in order to generate an xml description of a network. 
Each objects (Population, Projection, etc...) of a PyNN model is stored in a Network object which is then converted in xml format.

:copyright: Copyright 2006-2022 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.
