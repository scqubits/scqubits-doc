.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _install:

*******
Install
*******


.. _install-via_conda:

Installing via conda
====================

scqubits can be installed via conda by executing

.. code-block:: bash

   conda install -c conda-forge scqubits

Upgrading to the latest version of scqubits can be done by 

.. code-block:: bash

   conda update -c conda-forge scqubits


.. _install-via_pip:

Installing via pip
==================

scqubits can be installed using the Python package manager `pip <http://www.pip-installer.org/>`_ (Note: when working
inside a conda environment, pip installs can lead to environment inconsistencies and should be avoided.)

.. code-block:: bash

   pip install scqubits

To upgrade to the latest version of scqubits one can execute 

.. code-block:: bash

   pip install scqubits -U

.. _install-requires:


ARM64 Compatibility
===================

Apple M1 machines with arm64 architecture, scqubits is only compatible with SciPy < 1.7 and Python < 3.9, in addition to
the requirements listed below. Alternatively, it is possible to create conda environments with x86 architecture.


.. toctree::
   :hidden:

   install/gen-requirements
   install/verify-install
