.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

Tight Binding
==============

This module serves as a parent class that qubit classes can be derived from.
The idea is to attempt to diagonalize superconducting circuit
Hamiltonians using tight-binding states that in some cases more closely
approximate the low-energy eigenstates as compared to charge basis states.
The relatively complicated nature of the source code as compared to other standard
numerical diagonalization procedures (charge basis, harmonic oscillator basis,
real space discretization, etc.) is due to the need to normal order all expressions
involving ladder operators.
This module assumes that the potential is of the form

    .. math::

        U=-EJ[1]*\cos(\phi_1)-EJ[2]*\cos(\phi_2)-...-EJ[N]*\cos(bc[1]*\phi_1+bc[2]*\phi_2+...-2\pi f),


where the array :math:`bc` denotes the coefficients of terms in the boundary term.
For the flux qubit, the last term looks
like :math:`-\alpha*EJ*\cos(\phi_1-\phi_2-2\pi f)`, where :math:`0.5\leq\alpha<1.0`.
For the current mirror it is :math:`-EJ[N]*\cos(\sum_i(\phi_i)-2\pi f)`.
Extensions to different types of potentials requires overriding the function::

   VCHOS._local_potential

An example can be found in scqubits/core/zero_pi_vchos.py,
where we must implement a potential of the form

   .. math::

      U=E_{L}\phi^2 - 2E_{J}\cos(\theta)\cos(\phi-2\pi f/2)

If the user would like to define a new qubit class ``MyQubit`` that inherits
``VCHOS``, the user must define the functions::

   MyQubit.potential()
   MyQubit.build_capacitance_matrix()
   MyQubit.build_EC_matrix()
   MyQubit.find_minima()

which encode the qubit specific information. Additionally, if the qubit potential has
the default form, the user must initialize::

   MyQubit.boundary_coefficients

an ndarray of the coefficients in the boundary term in ``MyQubit.__init__``.

Initialize ``VCHOS`` for example in the following way::

   EJ = 1.0
   ng = 0.0
   flux = 0.0
   maximum_periodic_vector_length = 8
   number_degrees_freedom = 2
   number_periodic_degrees_freedom = 2
   num_exc = 4
   vchos = VCHOS(EJlist=np.array([EJ, EJ]), nglist=np.array([ng, ng]), flux=flux,
                 maximum_periodic_vector_length=maximum_periodic_vector_length,
                 number_degrees_freedom=number_degrees_freedom,
                 number_periodic_degrees_freedom=number_periodic_degrees_freedom,
                 num_exc=num_exc)

where we have used the Flux Qubit as an example application of ``VCHOS``.
``maximum_periodic_vector_length`` determines the maximum Manhattan length
of a possible periodic continuation vector, ``number_degrees_freedom`` is the number
of degrees of freedom your qubit possesses, ``number_periodic_degrees_freedom`` is the
number of those degrees of freedom that are periodic, and ``num_exc`` is the maximum
number of excitations kept per mode.

A global excitation cutoff scheme is implemented in ``Hashing``, in which case
the keyword argument ``global_exc`` must be set and ``num_exc`` should
not be passed as an argument. The class ``MyQubit`` must inherit
``Hashing`` before ``VCHOS`` in order for methods to be overridden correctly.

If the user would like to squeeze states localized in non-global minima in
order to accurately reflect the local curvature, this can be done by
instead inheriting ``VCHOSSqueezing``. No other changes need be made.

If the user would like to optimize the harmonic lengths of the ansatz states,
this can be done by setting the flag ``vchos.harmonic_length_optimization=1``.
By default the flag is set to 0. If the user is using squeezing and would
like to optimize the harmonic lengths of states localized in all minima,
as opposed to just the global minimum, this can be done by setting the flag
``vchos.optimize_all_minima=1``.

If the user is implementing a qubit that has both real and periodic degrees of freedom,
note that the convention used in the code is that for arrays of the
coordinates (necessary for constructing periodic continuation vectors, for example),
the extended degrees of freedom come first. For
example, for the :math:`0-\pi` qubit, with real :math:`\phi` and periodic :math:`\theta`
degrees of freedom, the array ``position=np.array([0, 2*np.pi])`` describes
a periodic continuation vector where no periodic continuation is done in the
:math:`\phi` direction, and we periodically continue by :math:`2\pi` in the :math:`\theta` direction.
See current_mirror_vchos.py, flux_qubit_vchos.py and zero_pi_vchos.py for examples.


Calculational methods related to Hamiltonian and energy spectra
_______________________________________________________________

.. autosummary::

   scqubits.VCHOS.transfer_matrix
   scqubits.VCHOS.kinetic_matrix
   scqubits.VCHOS.potential_matrix
   scqubits.VCHOS.inner_product_matrix
   scqubits.VCHOS.eigenvals
   scqubits.VCHOS.eigensys



Define Harmonic States
______________________

.. autosummary::

   scqubits.VCHOS.build_gamma_matrix
   scqubits.VCHOS.eigensystem_normal_modes
   scqubits.VCHOS.omega_matrix
   scqubits.VCHOS.Xi_matrix
   scqubits.VCHOS.sorted_minima
   scqubits.VCHOS.find_relevant_periodic_continuation_vectors