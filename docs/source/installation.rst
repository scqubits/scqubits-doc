.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _install:

**************
Installation
**************


.. _install-via_conda:

Installing via conda
====================

For Python 3.6, 3.7 and 3.8, installation via conda is supported. This is done by executing

.. code-block:: bash

   conda install -c conda-forge scqubits

Upgrading to the latest version of scqubits can be done by 

.. code-block:: bash

   conda update -c conda-forge scqubits


.. _install-via_pip:

Installing via pip
==================

scqubits can also be installed using the Python package manager `pip <http://www.pip-installer.org/>`_ (although it should be noted that installing via pip under a conda environment is strongly discouraged, and is not guaranteed to work).

.. code-block:: bash

   pip install scqubits

To upgrade to the latest version of scqubits one can execute 

.. code-block:: bash

   pip install scqubits -U

.. _install-requires:

General Requirements
=====================

scqubits depends on the following Python open-source libraries:


.. cssclass:: table-striped

+----------------+--------------+-----------------------------------------------------+
| Package        | Version      | Details                                             |
+================+==============+=====================================================+
| **Python**     | 3.6+         | Version 3.6 and higher is supported.                |
+----------------+--------------+-----------------------------------------------------+
| **NumPy**      | 1.14.2+      | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **SciPy**      | 1.1.0+       | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **Matplotlib** | 3.0.0+       | Some plotting does not work on lower versions.      |
+----------------+--------------+-----------------------------------------------------+
| **QuTiP**      | 4.3+         |  Needed for composite Hilbert spaces.               |
+----------------+--------------+-----------------------------------------------------+
| **Cython**     | 0.28.5+      |  Required by QuTiP                                  |
+----------------+--------------+-----------------------------------------------------+
| **tqdm**       | 4.0+         |  Needed for display of progress bar                 |
+----------------+--------------+-----------------------------------------------------+


The following packages are optional:

+------------------------+--------------+-----------------------------------------------------+
| Package                | Version      | Details                                             |
+========================+==============+=====================================================+
| ipywidgets             | 7.5+         | For use of the interactive explorer                 |
+------------------------+--------------+-----------------------------------------------------+
| h5py                   | 2.10+        |  Needed for writing data to h5 file                 |
+------------------------+--------------+-----------------------------------------------------+
| pytest                 | 5.3+         | For running the test suite.                         |
+------------------------+--------------+-----------------------------------------------------+
| matplotlib-label-lines | 0.3.6+       | For smart labelling of matrix element plots         |
+------------------------+--------------+-----------------------------------------------------+





.. _install-verify:

Verifying the Installation
==========================

scqubits includes a set of tests that can be executed to verify that installation was successful:

.. code-block:: python

   import scqubits.testing as sctest
   sctest.run()

This requires the pytest package.
