.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski


scQubits documentation
======================

scqubits is an open-source Python library for simulating superconducting qubits.

.. grid:: auto

    .. grid-item::

       Get the latest info on updates and releases by joining our mailing list:

    .. grid-item::

        .. button-link:: https://sites.northwestern.edu/koch/scqubits-news-sign-up/
            :color: info
            :shadow:

            SUBSCRIBE




.. figure:: ./graphics/slideshow.gif
   :align: center
   :width: 5in

Getting Started
***************

After :ref:`Install` of scqubits, check out the
:ref:`User Guide`, as well as the :ref:`Jupyter Examples`.

We are also building up a set of `YouTube Tutorials <https://www.youtube.com/channel/UCI43mhRw6oY01FbPuOc5CVQ>`_.


Overview
********

The package provides convenient ways to obtain energy spectra of common superconducting qubits, to plot their energy
levels as a function of external parameters, to calculate matrix elements and predict coherence times etc. scqubits
further offers an interface to QuTiP, making it easy to work with composite Hilbert spaces consisting of multiple
coupled superconducting qubits and harmonic modes.

scqubits performs numerics utilizing Numpy and Scipy; plotting capabilities rely on Matplotlib.

Citations
*********

If you employ scqubits in your research, please support its continued
development and maintenance. Use of scqubits in research publications is
appropriately acknowledged by citing:

   | Sai Pavan Chitta, Tianpu Zhao, Ziwen Huang, Ian Mondragon-Shem, and Jens Koch
   | *Computer-aided quantization and numerical analysis of superconducting circuits*
   | arXiv:2206.08320 (2022).
   | https://iopscience.iop.org/article/10.1088/1367-2630/ac94f2

   | Peter Groszkowski and Jens Koch,
   | *scqubits:  a Python package for superconducting qubits*,
   | Quantum 5, 583 (2021).
   | https://quantum-journal.org/papers/q-2021-11-17-583/



.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: GETTING STARTED

   ./installation.rst
   ./guide/gui/ipynb/gui.ipynb
   ./guide/basics/basics.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: COMMON QUBITS, CIRCUITS

   ./guide/qubits/guide-qubits.rst
   ./guide/noise/guide-noise.rst
   Single-Qubit Parameter Sweep <./guide/parametersweep/ipynb/paramsweep.ipynb>


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: CUSTOM CIRCUIT

   ./guide/circuit/ipynb/custom_circuit_root.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: COMPOSITE SYSTEMS

   ./guide/hilbertspace/ipynb/hilbertspace.ipynb
   ./guide/hilbertspace/ipynb/branch_analysis.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: EXPLORING PARAMETERS

   Simple Sweeps (1d, single qubit) <./guide/parametersweep/ipynb/paramsweep.ipynb>
   General Sweeps: ParameterSweep class  <./guide/parametersweep/ipynb/paramsweep2.ipynb>
   ./guide/explorer/ipynb/explorer.ipynb


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: SETTINGS

   Eigensolver options & GPU <./guide/settings/ipynb/custom_diagonalization.ipynb>
   ./guide/settings/ipynb/parallel.ipynb
   ./guide/settings/guide-plot-options.rst
   ./guide/settings/guide-units.rst
   Global Settings <./guide/settings/guide-settings.rst>


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: DATA

   ./guide/storage/ipynb/storage.ipynb
