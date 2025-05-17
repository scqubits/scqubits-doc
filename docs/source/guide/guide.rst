.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide:

*******************
User Guide
*******************


Guide Overview
==============

This guide introduces the main building blocks of scqubits and demonstrates with examples how to use them.
Topics addressed here include the different implemented superconducting qubits, as well as the interface to
QuTiP. The latter allows for simple creation of composite Hilbert spaces, consisting of multiple qubits and/or
oscillators.

This guide does not mean to be exhaustive. For a complete references see  the :ref:`apidoc` at the end which lists the
relevant classes and functions of scqubits.


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: GETTING STARTED

   ../installation.rst
   ./gui/ipynb/gui.ipynb
   ./basics/basics.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: COMMON QUBITS, CIRCUITS

   qubits/guide-qubits.rst
   noise/guide-noise.rst
   Single-Qubit Parameter Sweep <./parametersweep/ipynb/paramsweep.ipynb>


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: CUSTOM CIRCUIT

   ./circuit/ipynb/custom_circuit_root.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: COMPOSITE SYSTEMS

   ./hilbertspace/ipynb/hilbertspace.ipynb
   ./hilbertspace/ipynb/branch_analysis.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: EXPLORING PARAMETERS

   Simple Sweeps (1d, single qubit) <./parametersweep/ipynb/paramsweep.ipynb>
   General Sweeps: ParameterSweep class  <./parametersweep/ipynb/paramsweep2.ipynb>
   ./explorer/ipynb/explorer.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: SETTINGS

   ./settings/ipynb/custom_diagonalization.ipynb
   ./settings/ipynb/parallel.ipynb
   ./settings/guide-plot-options.rst
   ./settings/guide-units.rst
   Global Settings <./settings/guide-settings.rst>


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: DATA

   ./storage/ipynb/storage.ipynb
   ./parametersweep/ipynb/namedslots.ipynb
