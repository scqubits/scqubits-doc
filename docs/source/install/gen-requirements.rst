.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _geneneral_requirements:

General Requirements
=====================

scqubits depends on the following Python open-source libraries:


.. cssclass:: table-striped

+----------------+--------------+-----------------------------------------------------+
| Package        | Version      | Details                                             |
+================+==============+=====================================================+
| **Python**     | 3.9+         | Version 3.9 and higher is supported.                |
+----------------+--------------+-----------------------------------------------------+
| **pathos**     | 0.3+         | Required for multiprocessing                        |
+------------------------+--------------+---------------------------------------------+
| **NumPy**      | 1.14.2+      | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **SciPy**      | 1.5+         | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **Matplotlib** | 3.5.1+       | Some plotting does not work on lower versions.      |
+----------------+--------------+-----------------------------------------------------+
| **QuTiP**      | 4.3.1+       |  Needed for composite Hilbert spaces.               |
+----------------+--------------+-----------------------------------------------------+
| **Cython**     | 0.29.2+      |  Required by QuTiP                                  |
+----------------+--------------+-----------------------------------------------------+
| **tqdm**       | 4.0+         |  Needed for display of progress bar                 |
+----------------+--------------+-----------------------------------------------------+
| **sympy**      | 1.7.1+       |  Needed for custom circuit analysis                 |
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

.. warning::

   For Apple M1 and M2 machines with ARM64 architecture, scqubits is only compatible with SciPy < 1.7.0, >=1.7.3,
   in addition to the requirements listed above. Please make sure compatible versions of these libraries are installed.
   Alternatively, create a conda environment for x86 architecture, where additional constraints does not apply.
