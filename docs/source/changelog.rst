.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _changelog:

**********
Change Log
**********

Version 4.3.1
+++++++++++++

**BUG FIXES**

    - Fixed issue with `Circui`t module not utilizing custom diagonalization methods from `diag.py`.
    - Fixed issue where setting `ext_basis` did not work for purely harmonic subsystems.
    - Fixed issue with inconsistent eigenenergies of the subsystem when parent's parameters were changed.

**UNDER THE HOOD**

    - Updated Github Actions workflow to account for the deprecations.
    - Updated the local `meta.yaml` to match corresponding file in `scqubits-feedstock`.


Version 4.3
+++++++++++

**ADDITIONS**

    - Meshgrids can now be directly generated in the `Parameters` class by `meshgrids_by_paramname`
    - `HilbertSpace.dressed_state_component()` and `ParameterSweep.dressed_state_component()`. These provide the probability of occupying particular bare states when the 
      system is in an eigenstate.
    - For a non-dispersively coupled system, the eigenstates labeling by overlap might fail. Instead, we can use the branch analysis method to get a reliable labeling, 
      following Dumas et al. (2024). Try this functionality by `HilbertSpace.generate_lookup(ordering="LX")` or `ParameterSweep(..., labeling_scheme="LX")`. For more info 
      about the use and the implementation, please refer to the documentation and the docstrings.
    - Migrated to `pyproject.toml` from `setup.py` for installation with pip.

**BUG FIXES**

    - Fix #193. We use `id_str` to identify subsystems instead of the subsystem object for `subsys_update_info`. We perform multiple checks when initializing the object to 
      make sure this is secure. 
    - Fix parameter functions for parametric driving in the Circuit module.
    - Fix configure method in `SymbolicCircuit`, now does not reset the instance when run with no arguments.
    - Fix bugs #193 and #209 related to`ParameterSweep`.
    - Fix compatibility of `Circuit` module with `HilbertSpace`, bugs #253 and #254.
    - Fix #211, a bug that could occur when `op_in_dressed_eigenbasis` was called without prior lookup generation.
    - `SymbolicCircuit` instances now do not need to be re-initiated when their `configure` method fails (e.g., because of incorrect parameters).

**UNDER THE HOOD**

    - `SpectrumLookupMixin.reset_preslicing()` now resets the slice to a tuple of multi-dimensional slices
    - `ParameterSweep._preslicing_reset()` is redundant (exactly the same as `SpectrumLookupMixin.reset_preslicing()`) and is replaced.
    - A more rigorous implementation for `SpectrumLookupMixin.all_params_fixed()` for all different supported slicing methods
    - `ParameterSweep` now keeps the original instance when `deepcopy=True`.
    - Reduce redundant diagonalizations when `ParamtersSweep` is used with the `hilbert_space` object of a `Circuit` instance.
    - Added plotting tests and refactor code for `Circuit` instance.
    - Type annotations fixes and code cleanup.


Version 4.2
+++++++++++

**ADDITIONS**

    - Allow loops with capacitances when dynamical flux grouping is used in custom circuits.
    - Allow setting branch parameters with negative values - a feature useful for higher order junctions in custom circuits.

**BUG FIXES**

    - Fix prefactor for evaluations noise spectral density for quasiparticle noise - adds an additional factor of :math:`\hbar/e^2`.
    - Fix error in symbolic Hamiltonian for multi-harmonic junctions.

**UNDER THE HOOD**

    - Support for `numpy`>=2.0.
    - Fix type annotations for certain functions, code cleanup.
    - Updates to various testing functions.
    - Internal updates to the custom diagonalization module.


Version 4.1
+++++++++++

**ADDITIONS**

    - Allow Henries as units for Josephson junctions in `Circuit` definitions.
    - The info for `Circuit` module is just the `_repr__latex_`, which returns Circuit info from a code cell.

**BUG FIXES**

    - Fix compatibility with `qutip` version 5. 
    - Fix crashes for oscillator subsystems in hierarchical diagonalization, in `exp_i_operator`.
    - Fix :math:`2\pi` factor in external flux terms in purely harmonic subsystems.
    - Fix crashes, related to the warning attribute which is not defined for `HilbertSpace` object.
    - Fix Github actions for `macos-latest` runs, which failed for `qutip` version 5.

**UNDER THE HOOD**

    - Updates and clean up of Github tests.
    - No longer require `cython<3.0`.
    - Added python-version specific `qutip` installs that guarantee full support.


Version 4.0
+++++++++++

**ADDITIONS**

Following additions are for the `Circuit` module:

    - Support for custom diagonalization.
    - Coherence time calculations for a general circuit, with the argument `generate_noise_methods`.
    - Ability to provide circuit parameters using physical units and multiplier prefixes.
    - Helper function `hamiltonian_for_qutip_dynamics` to easily simulate time dynamics for a given parameter.
    - Ability to set basis for extended variables for each subsystem individually when hierarchical diagonalization is used.
    - Can instantiate `Circuit` instance with a symbolic Hamiltonian.
    - Flux grouping when external flux is time dependent for superconducting loops in a circuit.
    - New info method to give a description of the `Circuit` instance.
    - Make certain attributes read-only, which need to be changed using the `configure` method.
    - Ability to change the spanning tree by defining a custom set of `closure_branches`.
    - The `plot_wavefunction` now supports options to plot the real, imaginary, absolute-square and absolute value of a wavefunction when applicable.

**BUG FIXES**

    - Fix diagonalization for purely harmonic systems using the `Circuit` module
    - Fix bugs in `Circuit` plotting routines.
    - `Circuit` module supports parallel processing.
    - Fix bugs when defining custom variable transformation in `Circuit` module.
    - Fix typos in `ZeroPi` related to custom diagonalization
    - Fixed a bug in `plot_wavefunction`  method `Circuit` , where the user-provided `grids_dict` argument was not applied in the plot.

**UNDER THE HOOD**

    - More efficient evaluation of eigenvalues for purely harmonic circuits.
    - More efficient attribute updates for the `Circuit` instance.
    - Using `pyparsing` instead of `pyyaml` to parse the input string for the `Circuit` module.
    - Initial work on making the `Circuit` instance writable to file.
    - Refactoring and improving code quality.
    - Improve the accuracy of `_evaluate_symbolic_expr`


Version 3.3
+++++++++++

**ADDITIONS**

    - The custom diagonalization module now also supports the `jax` library. 
    - Custom diagonalization is now possible for the `FullZeroPi` qubit. 

**BUG FIXES**

    - Fixed how `op_in_dressed_eigenbasis` sets operator dimensions.

**UNDER THE HOOD**

    - Initial work on QuTiP 5 compatibility 
    - Initial work to allow for custom diagonalization in the `Circuit` module in the near future.
    - Updates on how annotations are handled in some cases.
    - Automatic generation of `__all__` list in the `__init__.py`.

Version 3.2
+++++++++++

**ADDITIONS**

    - New diagonalization module allows users to easily customize how, and what library is used to calculate the eigenvalues and eigenvectors of the various quantum systems that scqubits implements (custom Circuits and FullZeroPi are not yet supported). Both sparse and dense diagonalization procedures from libraries such as scipy, primme, and cupy (which offers GPU support), are exposed, and can be easily selected with different sets of predefined options and parameters. Completely arbitrary diagonalization functions can be also set by the user.
    - Added support for 1/f flux noise dephasing time calculation to the `FluxQubit` class.
    - Overhaul of the graphical user interfaces, including `scqubits.GUI`, `scqubits.Explorer`, and `scqubits.HilbertSpace.create`

**BUG FIXES**

    - Fixed a bug affecting numerical results in certain `ParameterSweep` cases. The problem arises in cases where the
      operators appearing in `InteractionTerm` need updating under parameter changes. (Not applicable to `Transmon`, `TunableTransmon`,
      or `Oscillator`, but relevant for `Fluxonium`, for example.)
    - Fixed a bug that could result in repeated Matplotlib warnings about missing fonts
    - Fixed bug that could prevent progress bar visibility settings to take effect
    - Fixed a bug that could change how the T1 coherence time due to a flux bias line was calculated in a `TunableTransmon` qubit.

**UNDER THE HOOD**

    - Removed `nan` checks inside
    - Added missing flux-noise support to `FluxQubit`
    - Docstring fixes and additions, improvements to type annotations


Version 3.1.1
+++++++++++++

**ADDITIONS**

    - Enhanced support for interfacing with QuTiP/mesolve: for simulation of time evolution it is often preferable to work with matrices in the dressed eigenenergy basis (in the absence of a time-dependent drive).
    - To simplify this, all qubits (i.e., `QuantumSystem` children) now offer an `energy_esys` keyword argument, and introduce `HilbertSpace.op_in_dressed_eigenbasis`.
    - Add fit method `Transmon.find_EJ_EC` that extracts EJ, EC of a transmon, based on given E01 and anharmonicity.
    - Add `E01`, `anharmonicity` as attributes to all qubits inheriting from `QubitBaseClass`.


**BUG FIXES**

    - Fixed a bug affecting certain matrix element parameter sweeps that required recomputing of operators under parameter changes (#114 and #177).
    - Fixed a bug where `energy_by_bare_index` could throw an exception because np.int32 is not recognized by isinstance(myvar, int)  (#172).
    - Fix for inconsistencies in global signs used for harmonic oscillator and discrete charge basis, originating in definitions of charge-basis lowering/raising operators; e^(i theta) is raising operator. Related fix in harm. osc. momentum operator sign (#166).
    - Corrected `Transmon.d_hamiltonian_d_flux` to account for the shift in generalized flux (#178).
    - Various GUI bug fixes.
    - Various docstring typo fixes (incl. #165).


**UNDER THE HOOD**

    - Renamed branch master → main.
    - Constrain changes to matplotlib settings to scqubits.
    - Account for scipy deprecation: `linalg.eigh` option `eigvals` -> `subset_by_index`.
    - Introduce check for existence of lookup in `HilbertSpace` and `ParameterSweep`; emit meaningful exception message otherwise.
    - Phase out `HilbertSpace.subsys_list` in favor of `subsystem_list` (#160).
    - Remove deprecated `HilbertSpace.lookup` interface and corresponding adapter class.
    - Distinguish preslicing reset for `ParameterSweep` and `HilbertSpace` (#170).
    - Changed pytest data for `ZeroPi`, `FullZeroPi`, `Cos2Phi` to account for the sign fix in 3c1c5914e41d944d8234a8cfc8f7ef2f5ae7b67e.
    - Increase required pathos version to 0.3.0 to fix the multiprocessing issue in python 3.7.


Version 3.1
+++++++++++

**Additions**

    - GUI now includes functionality to plot coherence time estimates for various qubits

**Under the hood**

    - Speedup for diagonalization of Transmon and TunableTransmon by recognizing the Hamiltonian matrix as tridiagonal.


Version 3.0.3
+++++++++++++

**Bug fixes for GUI**

    - `get_operator_names` has been eliminated from the operator dropdown menu
    - "State No." sliders for `FluxQubit`, `ZeroPi`, and `Cos2PhiQubit` do not exclude the ground state anymore.
    - Fixed a bug where the plot was not being erased after switching to another qubit while in manual-update mode.
    - Changing to a non-manual scqubit now switches manual-mode off.
    - Fixed a bug where the maximum state number could be larger than `hilbertdim`.

**Under the hood**

    - Initialization of a circuit instance now does not globally switch to latex output (avoids unnecessary slowdowns with regular, non-sympy, output.


Version 3.0.2
+++++++++++++

**Additions**

    - `Circuit` now implements multiprocessing in routines like `get_evals_vs_paramvals` when specifying `num_cpus=2` or higher as optional keyword argument.
    - The class `Circuit` is now “frozen” to prevent accidental creation of new instance attributes. Doing `<circuit instance>.non_existing_attribute = 3` will now raise an error message instead of creating a new attribute.
    - New threshold setting `scqubits.settings.SYM_INVERSION_MAX_NODES`  (default: `=3`) decides whether the capacitance matrix is inverted symbolically (number of nodes ≤ threshold) or numerically (number of nodes > threshold). This avoids apparent hang-ups due to generation of massive symbolic expressions for matrix inverses.

**Bug fixes**

    - Branches are now distinguished by a unique id. This solves an issue of incorrect spanning trees when two branches of the same type were connected across the same set of nodes.
    - Fixed a bug in plotting routines which led to an `Exception` for cases with two or more layers in the system hierarchy.
    - Fixed a bug that could break `Subsystem` instances when the symbolic Hamiltonian had no potential terms.
    - `GUI`: establish correct clearing when turning manual plot on or when switching to another plot while on manual update.

**Under the hood**

    - All numerical diagonalization is now delayed until explicitly required. Changing circuit parameters thus does not incur a repeated runtime cost anymore.
    - When hierarchical diagonalization is used, the bare eigensystems for each subsystems are now stored and reused for calculations, and only replaced by a new set when necessary. This dramatically improves the performance of wavefunction plotting, identity wrapping, etc.
    - If the circuit parameters are not updated, successive diagonalizations are skipped for all subsystems.
    - Implemented `eigsh_safe` (wrapper for scipy.sparse.linalg.eigsh) that orthogonalizes the eigenvectors when degenerate eigenvalues are detected. In rare cases of actual degeneracies in the spectrum, sparse matrix methods could have given incorrect results because `scipy.sparse.linalg.eigsh` does not guarantee orthogonality of eigenvectors in degenerate subspaces.

**Deprecations**

    - The `Circuit.from_yaml` method will be phased out. Instead simply use the regular instance creation method `scq.Circuit(...)` with the same arguments as in the `from_yaml` class method.



Version 3.0.1
+++++++++++++

**Additions**

    - Modified `SymbolicCircuit` and `Circuit` classes to simulate linear LC circuits efficiently.
    - Added the option `grids_dict` to `plot_wavefunction`, which provides an option to define a custom grid for `wavefunction` plots.
    - File input/output is now functional for the Circuit class, which will enable users to store `Circuit` objects to file.

**Bug Fixes**

    - `sym_external_fluxes` now functions as expected for circuits with capacitive sub-circuits; external fluxes are now distributed in a deterministic way by default.
    - Fixed and improved functions that display symbolic Hamiltonians, Lagrangians, potentials, etc.; added factor 2pi for displayed external fluxes to reflect units correctly.
    - Fixed the representation of cosine operator for periodic variables which previously resulted in an erroneous shift of pi in the `wavefunction` plots.
    - Multiple corrections to plot functionality of `Circuit` class.
    - GUI: fixed issue with “update” button for slow qubits.
    - GUI: fixed bad range default for `wavefunction` plots of fluxonium.

**Under the Hood**

    - Changed the way to calculate the junction potential matrix in `Circuit` class, which now uses `expm` to evaluate the cosine terms.
    - f-strings are now used for most of the string manipulations in `Circuit` and `SymbolicCircuit` class.
    - Fixed the overall energy shift in the eigenvalues by incorporating omega/2 for every harmonic oscillator.


Version 3.0
+++++++++++

**Additions**

    - Add circuit and symbolic_circuit modules, introducing the Circuit class for symbolic and numerical analysis of custom circuits
    - Add official support for Python 3.9 and 3.10
    - Improved GUI for single qubits (incl., e.g., a Dropdown menu with parameter choices from papers)
    - Improved Explorer class
    - Additional options for specifying initial and final states in transitions and plot_transitions inside ParameterSweep
    - Additional helper functions in ParameterSweep: get_subsys(index), subsys_by_id_str(id_str), subsys_evals_count(index), dressed_evals_count
    - ParameterSweep offers a new option ignore_low_overlap
    - Improved status information output when using parallel processing of ParameterSweep data

**Deprecations**

    - Remove deprecation support for outdated InteractionTerm / HilbertSpace interface
    - Remove deprecation support for outdated Explorer interface

**Bug Fixes**

    - Fixed incorrect output/return from supported_noise_channels for the FullZeroPi qubit
    - Fixed accidental support of h5py without safeguard (remains optional)
    - Fixed ordering bug in de-serialization of OrderedDict which could prevent reading of ParameterSweep objects
    - Fixed plotting issue in which presence of nans could reduce the intended plot range

**Under the Hood**

    - Remove _evec_dtype attribute from qubit classes
    - Eliminated code duplication for SpectrumLookup between HilbertSpace and ParameterSweep . Both classes now use SpectrumLookupMixin
    - ParameterSweep now has read-only property hilbertspace
    - Added quantitative pytest for FullZeroPi


Version 2.2.2
+++++++++++++

**Bug Fixes**
    - Fixed issue that could make import of scqubits fail when optional h5py package
      was not installed.
    - Plot options were not properly handled by `plotting.data_vs_paramvals`, leading
      to poor formatting of `plot_dispersion_vs_paramvals`
    - In certain scenarios (likely related to dependency version updates), GUI
      displays were duplicated rather than substituted.
    - Adjusted calculations mapping dressed-basis to bare-state labels: use (state
      overlap)^2 instead of (state overlap) for thresholding.

**Under the Hood**
    typing_extensions is new dependency (used for enhanced typing annotations such as
    `@overload` and `Literal`


Version 2.2
+++++++++++++

**Bug Fixes**
    - Use of `<ParameterSweep>.plot_transitions` could previously lead to a spurious
      switch of `<ParameterSweep>["evals"]` to transition energies.
    - Include the :math:`/frac{1}{1}hbar` omega term when diagonalizing fluxonium in the harmonic
      osc. basis. The omission of this only affected absolute energies, not the energy
      differences which are the relevant quantities in most cases. However, wavefunction
      plots for fluxonium were previously incorrectly positioned relative to the potential energy.
    - Some dispersion calculations previously failed for qubits other than Transmon
      and  `TunableTransmon`.
    - Eliminated rare `NamedSlotsNdarray` indexing failure modes.
    - `ParameterSweep` previously failed for a "sweep" over just one parameter value.
    - Fixed issue where the depolarization time due to quasiparticle tunneling could
      be negative.
    - Fixed issue where accumulating legend label information in multiple plots to the
      same figure would fail to produce the desired legend.

**Additions**
    - Support access to `Figure`, `Axes` objects from `scq.GUI()`.
    - Support access to `Figure`, `Axes` from `ParameterSweep.plot_transitions`.
    - Support multi-photon transitions in `ParameterSweep.transitions()` and
      `.plot_transitions()` via new keyword argument `photon_number`
    - Added functionality for naming quantum system instances and interaction terms
      via `id_str` at initialization. This supports easier dict-like access to objects
      interior to `ParameterSweep`. Added deepcopy option to `ParameterSweep` that
      disconnects global variables from a deep copy saved inside `ParameterSweep`.
    - Refactored `Explorer` class for usage of new `ParameterSweep`
    - `supported_noise_channels` and `effective_noise_channels` are now `@classmethods`
      and can be called either directly through a class, or through a class instance.
    - `t1_charge_impedance` is no longer returned by `effective_noise_channels` in the
      case of a `TunableTransmon` and `Transmon` qubits
    - Added about function that shows basic information about scqubits as well as
      versions of some of the most important libraries that scqubits relies on.
    - Extended `pytests` for enhanced coverage.

**Deprecations**
    - Old version of `Explorer` is still available with deprecation warning, but will
      be phased out in the future.
    - Deprecated `omega` parameter for `Oscillator` has been removed.



Version 2.1
+++++++++++++

**Bug Fixes**
    - Fixed a bug that overwrote `<ParameterSweep>["evals"]` data with transition data when using `plot_transitions()`.
    - Fixed proper integration of `ParameterSweep` into `CentralDispatch`, enabling proper warnings to the user when internal computed sweep data is out of sync with associated quantum system parameters.
    - Fixed a bug that could occur when a `ParameterSweep` was applied to a `HilbertSpace` object involving only a single subsystem.

**Under the Hood**
    - Enable use of `weakref` in `CentralDispatch` for proper garbage collection.
    - Extended pytests to basic `CentralDispatch` functionality



Version 2.0
+++++++++++++

**Additions**
    - New graphical user interface ``scqubits.GUI()`` illustrating single-qubit
      functionality of scqubits.
    - Introducing ``NamedSlotsNdarray`` as a convenient subclass of ndarray with
      name-based and value-based slicing, and immediate support for basic plots
    - Added functionality for extracting dispersive energy parameters (such as Kerr
      coupling strengths)
    - Improved support for transition plots (subsystem transitions, sidebands etc.)
    - Added ``Cos2PhiQubit`` class.
    - Added ``KerrOscillator`` class
    - Added ``GenericQubit`` (two-level system) so that toy models such as the
      Jaynes-Cummings model can be readily realized with ``HilbertSpace``.
    - Added ``n`` and ``phi`` operators to the Oscillator class
    - Added helper methods ``convert_to_E_osc`` and ``convert_to_l_osc`` for ``Oscillator``
      initialization
    - New and enhanced interface for defining interaction terms in HilbertSpace objects
      via ``.add_interaction()``
    - Added option to input interaction as a ``Qobj``, or specify interaction terms as
      string expressions; also represented in ``HilbertSpace.create()`` GUI

**Improvements**
    - Convergence for ``ZeroPi`` is now faster, thanks to a correction to the expression
      for the grid spacing in discretization.py.
    - Refactored ``ParameterSweep`` class, now allowing for multi-dimensional parameter sweeps
    - Added a warning describing ``total=True`` being the default in t1 calculations


**Bug fixes**
    - Fix to type conversion error affecting the ``number`` operator in operators.py
    - Rectified orientation of ``matrix2d`` plots to match axes labels
    - ``mode`` option for values displayed in matrix element plots was ignored


**Internals**
    - New support for higher-order stencils in discretized derivatives.
    - Improved formatting of ``__str__`` methods (called when "printing" an scqubits class instance).
    - Under the hood: use of Python 3.6 compatible type annotations; unified formatting enabled by the ``black`` package
    - Improvements to fileIO speeding up operations (increased memore cache) and requiring less disk space (avoid literal redundancies in stored data).



Version 1.3.2
+++++++++++++

**Bug fixes**
    - bug fix: ``<qubit>.create()`` failed in jupyter notebooks due to missing image files
    - bug fix: corrected the form of the quasiparticle noise operator


Version 1.3.1
+++++++++++++

**Major changes/additions**
    - Coherence calculations for the majority of qubits. These allow for estimating coherence times and rates due to various noise channels.
    - A new units system: users can specify energy units of their system Hamiltonian. These units are automatically considered when plotting and in coherence time calculations.
    - Separated documentation and example jupyter notebooks into individual repositories, see scqubits-doc and scqubits-examples.

**Minor changes/additions**
    - Introduced tests for real-valuedness of zero-pi Hamiltonians (for speedup).
    - New options in plotting (e.g. grid).

**Bug fixes**
    - Fixed bug preventing the proper disabling of the progress bar.
    - Various bug fixes and improvements of file IO operations.
    - Fixed issue with color legend bar in .plot_matrixelements.


Version 1.2.3
+++++++++++++

- **Bug fix**: the ``FullZeroPi`` Hamiltonian was incorrect in the case of nonzero ``dC``.
- improvement: thanks to adjusted ARPACK options, diagonalization should be noticeably faster for ``ZeroPi`` and ``FullZeroPi``.
- make ``pathos`` and ``dill`` the default for multiprocessing.


Version 1.2.2
+++++++++++++

- **Bug fix**: implementation of the ``add_hc=True`` flag in ``InteractionTerm`` involved a bug that could lead to incorrect results
- update to plotting routines now supports various extra plotting options such as ``linestyle=...`` etc.
- added ``TunableTransmon`` class for flux-tunable transmon, including junction asymmetry
- limit support to Python >= 3.6
- corrections to documentation of ``FullZeroPi``
- added missing jupyter notebook illustrating use of ``HilbertSpace`` and ``ParameterSweep``
- overhaul of file IO system now allows saving and loading various scqubit data via a custom h5 file format
- ipywidget support for creating qubits inside jupyter (try, for example, ``tmon = scqubits.Transmon.create()``)



Version 1.2.1
+++++++++++++
- update to the setup script to properly include testing data with the PyPi release.


Version 1.2
+++++++++++

**Major changes/additions**
   - scqubits now offers multiprocessing support for a number of methods.
   - Introduced checks ensuring that umbrella objects like ``HilbertSpace`` and ``ParameterSweep`` instances do not accidentally go "out-of-sync" with respect to their basic components. When needed, warnings are thrown for the user to re-run sweeps or spectrum lookups.

**Under the hood:**
   - Monitoring for changes of interdependent class instances is implemented through a central dispatch system. (disable: ``settings.DISPATCH_ENABLED``)
   - Removed ``HilbertSpace`` reference from within `InteractionTerm` (throws deprecation warning if still used)
   - Made ``HilbertSpace`` inherit from ``tuple`` rather than ``list``; composition changes to ``HilbertSpace`` warrant generating a new ``HilbertSpace`` instance
   - Shifted ``InteractionTerm.hamiltonian`` to ``HilbertSpace.interaction_hamiltonian``
   - Created ``DataStore`` as general purpose parent class to ``SpectrumData``
   - No longer store custom data inside ``ParameterSweep``, ``sweep_generators.py`` functions return ``DataStore`` objects


Version 1.1.1
+++++++++++++

   - fixed a bug in display of ``FluxQubit`` wavefunction
   - internal refactoring


Version 1.1.0
+++++++++++++

   - new class ``InteractionTerm`` works in tandem with ``HilbertSpace`` to ease setup of composite systems with pairwise interactions
   - new ``ParameterSweep`` class efficiently generates spectral data for performing a scan of a ``HilbertSpace`` object over an external parameters
   - new ``Explorer`` class introduces interactive plots (see docs and demo ipynb)
   - cleaned up implementation of file Serializable operations


Version 1.0.0 (first release)
++++++++++++++++++++++++++++++
