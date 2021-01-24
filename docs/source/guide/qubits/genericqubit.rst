.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski


.. _qubit_generic:

Generic Qubit (two-level system)
================================

While superconducting always have more than two eigenstates, it is nonetheless possible to reduce the more complicated
multi-level model to an effective two-level system description. The Jaynes-Cummings model can be understood as serving
as a simplified toy model for a superconducting qubit coupled to a harmonic oscillator.

To streamline the comparison between full circuit modeling and reduced models based on truncation to a qubit's
computational subspace, we can use the `GenericQubit` class. This class implements a quantum two-level system with
Hamiltonian

.. math::

   H=\frac{E}{2}\sigma_z,

where :math:`E` is the qubit's energy splitting.

An instance of such a generic qubit is obtained like this::

   qubit = scq.GenericQubit(E=5.0)


Calculational methods related to Hamiltonian and energy spectra
---------------------------------------------------------------

.. autosummary::

    scqubits.GenericQubit.hamiltonian
    scqubits.GenericQubit.eigenvals
    scqubits.GenericQubit.eigensys



Implemented operators
---------------------

The following operators are implemented for use in matrix element calculations.

.. autosummary::
    scqubits.GenericQubit.sx
    scqubits.GenericQubit.sy
    scqubits.GenericQubit.sz
    scqubits.GenericQubit.sp
    scqubits.GenericQubit.sm
