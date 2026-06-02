.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide-settings:

*************************************
Modifying Settings of scqubits
*************************************

.. _settings-params:

User Accessible Parameters
==========================

scqubits has a few internal parameters that can be changed by the user:

.. tabularcolumns:: | p{3cm} | p{3cm} | p{3cm} |

.. cssclass:: table-striped

+------------------------------+------------------------------+-------------------------------------------------------------------+
| Setting                      |  Options                     | Description                                                       |
+==============================+==============================+=============+=====================================================+
| ``FILE_FORMAT``              | `FileType.h5`, `FileType.csv`| Switches between supported file formats for writing data to disk. |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``PROGRESSBAR_DISABLED``     |  True / False                | Switches display of progressbar on/off.                           |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``AUTORUN_SWEEP``            | True / False (default: True) | Whether to generate ``ParameterSweep``                            |
|                              |                              | immediately upon initialization                                   |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``DISPATCH_ENABLED``         | True / False (default: True) | Whether to use central dispatch system                            |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``MULTIPROC``                | `str`                        | 'pathos' (default) or 'multiprocessing'                           |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``MULTIPROC_START_METHOD``   | str or None (default: None)  | Worker-process start method: None (platform default), 'fork',     |
|                              |                              | 'spawn', or 'forkserver'. Default is 'fork' on Linux and          |
|                              |                              | 'spawn' on macOS/Windows (fork is unsafe on macOS).               |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``NUM_CPUS``                 | int                          | Number of cores to be used in parallelization (default: 1)        |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``MULTIPROC_BLAS_THREADS``   | int or None (default: None)  | Cap BLAS/OpenMP threads per worker process during parallel sweeps |
|                              |                              | (``NUM_CPUS`` > 1), avoiding core oversubscription. Needs         |
|                              |                              | ``threadpoolctl`` for fork-based workers; no effect when numpy's  |
|                              |                              | BLAS exposes no thread control (e.g. Apple Accelerate).           |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``FUZZY_SLICING``            | True / False (default: False)| Whether to enable approximate value-based slicing                 |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``FUZZY_WARNING``            | True / False (default: True) | Whether to warn user about use of approximate values in slicing   |
+------------------------------+------------------------------+-------------------------------------------------------------------+
| ``SYM_INVERSION_MAX_NODES``  | int (default: 3)             | Threshold number of nodes above which the capacitance matrix is   |
|                              |                              | inverted numerically                                              |
+------------------------------+------------------------------+-------------------------------------------------------------------+

Users can also set up units of the energy scales. This is discussed in the
:ref:`guide_units` section of the user guide.


.. _settings-usage:

Example: Changing Settings
==========================

Modifying the settings is simple, for example::

   scqubits.settings.PROGRESSBAR_DISABLED = True

