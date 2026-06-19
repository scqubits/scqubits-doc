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

.. list-table::
   :header-rows: 1
   :widths: 30 30 50
   :class: table-striped

   * - Setting
     - Options
     - Description
   * - ``FILE_FORMAT``
     - ``FileType.h5``, ``FileType.csv``
     - Switches between supported file formats for writing data to disk.
   * - ``PROGRESSBAR_DISABLED``
     - ``True`` / ``False``
     - Switches display of progressbar on/off.
   * - ``AUTORUN_SWEEP``
     - ``True`` / ``False`` (default: ``True``)
     - Whether to generate ``ParameterSweep`` immediately upon initialization.
   * - ``DISPATCH_ENABLED``
     - ``True`` / ``False`` (default: ``True``)
     - Whether to use central dispatch system.
   * - ``MULTIPROC``
     - ``str``
     - ``"pathos"`` (default) or ``"multiprocessing"``.
   * - ``NUM_CPUS``
     - ``int``
     - Number of cores to be used in parallelization (default: 1).
   * - ``FUZZY_SLICING``
     - ``True`` / ``False`` (default: ``False``)
     - Whether to enable approximate value-based slicing.
   * - ``FUZZY_WARNING``
     - ``True`` / ``False`` (default: ``True``)
     - Whether to warn user about use of approximate values in slicing.
   * - ``SYM_INVERSION_MAX_NODES``
     - ``int`` (default: ``3``)
     - Threshold number of nodes above which the capacitance matrix is inverted numerically.
   * - ``CSC_DEFAULT_TARGET_ABS_GHZ``
     - ``float`` (default: ``1e-4``)
     - Default absolute energy-error target (GHz) used by the zero-input :func:`scqubits.csc` convenience. Tune for tighter (kHz) or looser (MHz) precision needs.
   * - ``CSC_DEFAULT_NLEVELS_CAP``
     - ``int`` (default: ``6``)
     - Upper bound on ``n_levels`` chosen automatically by :func:`scqubits.csc` from ``truncated_dim`` / ``dimension`` / ``hilbertdim()``. Raise this if you routinely care about more states.

Users can also set up units of the energy scales. This is discussed in the
:ref:`guide_units` section of the user guide.


.. _settings-usage:

Example: Changing Settings
==========================

Modifying the settings is simple, for example::

   scqubits.settings.PROGRESSBAR_DISABLED = True

