.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

Variational Tight Binding
=========================

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

        U=-EJ[1]\cos(\phi_1)-EJ[2]\cos(\phi_2)-...-EJ[N]\cos(bc[1]\phi_1+bc[2]\phi_2+...-2\pi f),


where the array :math:`bc` denotes the coefficients of terms in the boundary term.
For the flux qubit, the last term looks
like :math:`-\alpha\cdot EJ\cos(\phi_1-\phi_2-2\pi f)`, where :math:`0.5\leq\alpha<1.0`.
For the current mirror it is :math:`-EJ[N]\cos(\sum_i(\phi_i)-2\pi f)`.
Extensions to different types of potentials requires overriding the function::

   VariationalTightBinding._local_potential

An example can be found in scqubits/core/zero_pi_vtb.py,
where we must implement a potential of the form

   .. math::

      U=E_{L}\phi^2 - 2E_{J}\cos(\theta)\cos(\phi-2\pi f/2)

If the user would like to define a new qubit class ``MyQubit`` that inherits
``VariationalTightBinding``, the user must define the functions::

   MyQubit.potential()
   MyQubit.build_capacitance_matrix()
   MyQubit.build_EC_matrix()
   MyQubit.find_minima()

which encode the qubit specific information. Additionally, if the qubit potential has
the default form, the user must initialize::

   MyQubit.boundary_coefficients

an ndarray of the coefficients in the boundary term in ``MyQubit.__init__()``.

Inside of ``MyQubit.__init__()`` initialize ``VariationalTightBinding`` for example in the following way::

   def __init__(self, EJ1, EJ2, EJ3, ECJ1, ECJ2, ECJ3,
                ECg1, ECg2, ng1, ng2, flux, truncated_dim=None, **kwargs):
       EJlist = np.array([EJ1, EJ2, EJ3])
       nglist = np.array([ng1, ng2])
       VariationalTightBinding.__init__(self, EJlist, nglist, flux, number_degrees_freedom=2,
                      number_periodic_degrees_freedom=2, **kwargs)


where we have used the Flux Qubit as an example application of ``VariationalTightBinding``. Two
required keyword-arguments ``kwargs`` are ``maximum_periodic_vector_length`` and
``num_exc``. ``maximum_periodic_vector_length`` determines the maximum
Manhattan length of a possible periodic continuation vector and
``num_exc`` is the maximum number of excitations kept per mode.

A global excitation cutoff scheme is implemented in ``Hashing``, in which case
the keyword argument ``global_exc`` must be set and ``num_exc`` should
not be passed as an argument. The class ``MyQubit`` must inherit
``Hashing`` before ``VariationalTightBinding`` in order for methods to be overridden correctly.

If the user would like to squeeze states localized in non-global minima in
order to accurately reflect the local curvature, this can be done by
instead inheriting ``VariationalTightBindingSqueezing``. No other changes need to be made.

If the user would like to optimize the harmonic lengths of the ansatz states,
this can be done by setting the flag ``MyQubit.harmonic_length_optimization=1``.
By default the flag is set to 0. If the user is using squeezing and would
like to optimize the harmonic lengths of states localized in all minima,
as opposed to just the global minimum, this can be done by setting the flag
``MyQubit.optimize_all_minima=1``.

If the user is implementing a qubit that has both real and periodic degrees of freedom,
note that the convention used in the code is that for arrays of the
coordinates (necessary for constructing periodic continuation vectors, for example),
the extended degrees of freedom come first. For
example, for the :math:`0-\pi` qubit, with real :math:`\phi` and periodic :math:`\theta`
degrees of freedom, in the position vector ``[0, 2*np.pi]``, ``0`` refers to :math:`\phi`
and ``2*np.pi`` refers to :math:`\theta`.

See current_mirror_vtb.py, flux_qubit_vtb.py and zero_pi_vtb.py for examples
of qubits implemented using variational tight binding.


Calculational methods related to transfer matrix and inner-product matrix
_________________________________________________________________________

.. autosummary::

   scqubits.VariationalTightBinding.transfer_matrix
   scqubits.VariationalTightBinding.kinetic_matrix
   scqubits.VariationalTightBinding.potential_matrix
   scqubits.VariationalTightBinding.inner_product_matrix



Define Harmonic States
______________________

.. autosummary::

   scqubits.VariationalTightBinding.build_gamma_matrix
   scqubits.VariationalTightBinding.eigensystem_normal_modes
   scqubits.VariationalTightBinding.omega_matrix
   scqubits.VariationalTightBinding.Xi_matrix
   scqubits.VariationalTightBinding.sorted_minima
   scqubits.VariationalTightBinding.find_relevant_periodic_continuation_vectors