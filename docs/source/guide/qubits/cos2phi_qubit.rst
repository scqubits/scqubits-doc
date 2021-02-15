.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

.. _cosine_two_phi_qubit:

Cosine Two Phi Qubit
=========================

.. figure:: ../../graphics/fluxqubit.png
   :align: center 
   :width: 4in  
 
The cosine two phi qubit [Smith2020]_ is described by the Hamiltonian

.. math::

   H = & \,2 E_\text{CJ}n_\phi^2 + 2 E_\text{CJ} (n_\theta - n_\text{g} - n_\zeta)^2 + 4 E_\text{C} n_\zeta^2\\
   & + E_\text{L}(\phi - \varphi_\text{ext}/2)^2 + E_\text{L} \zeta^2 - 2 E_\text{J}\cos{\theta}\cos{\phi}.

In the presence of disorder, the above Hamiltonian is modified 

.. math::

    H = & \,2 E_\text{CJ}'n_\phi^2 + 2 E_\text{CJ}' (n_\theta - n_\text{g} - n_\zeta)^2 + 4 E_\text{C} n_\zeta^2\\
    & + E_\text{L}'(\phi - \varphi_\text{ext}/2)^2 + E_\text{L}' \zeta^2 - 2 E_\text{J}\cos{\theta}\cos{\phi} \\
    & + 2 \delta_\text{EJ} E_\text{J}\sin{\theta}\sin{\phi} \\
    & - 4 \delta_\text{CJ} E_\text{CJ}' n_\phi (n_\theta - n_\text{g}-n_\zeta) \\
    & + \delta_\text{L}E_\text{L}'(2\phi - \varphi_\text{ext})\zeta , 

where :math:`E_\text{CJ}' = E_\text{CJ} / (1 - \delta_\text{CJ})^2` and :math:`E_\text{L}' = E_\text{L} / (1 - \delta_\text{L})^2`. Here, the disorder is defined as follows: the inductive energy of the two inductors are :math:`E_\text{L}/(1 \pm \delta_\text{L})`; the charging energy of the two Josephson junctions are :math:`E_\text{CJ}/(1 \pm \delta_\text{CJ})`; the junction energy of the two Josephson junctions are :math:`E_\text{J} (1 \pm \delta_\text{EJ})`. 

Here, we adopt notation that is consistent with other qubit classes. A conversion to the notation used in Ref. [Smith2020]_ can be founded in the following table.

.. list-table:: 
   :widths: 25 25

   * - Notation used here
     - Notation used in Ref. [Smith2020]_
   * - :math:`\zeta`
     - :math:`\theta`
   * - :math:`\theta`
     - :math:`\varphi`
   * - :math:`\phi`
     - :math:`\phi/2`  
   * - :math:`E_\text{C}`
     - :math:`E_\text{C} x` 
   * - :math:`E_\text{CJ}`
     - :math:`E_\text{C}` 

                
To numerically diagonalize the Hamiltonian in the ``Cos2PhiQubit`` class, harmonic basis is used for both the :math:`\phi` and :math:`\zeta` variables, and charge basis is used for :math:`\theta` variable. The user needs to specify cutoffs for basis states described above, i.e., ``phi_cut``, ``zeta_cut``, and ``n_cut``, chosen large enough so that convergence is achieved.

An instance of the cosine two phi qubit is initialized as follows::

   cos2phi_qubit = scqubits.Cos2PhiQubit(EJ = 15.0,
                                         ECJ = 2.0,
                                         EL = 1.0,
                                         EC = 0.04,
                                         dCJ = 0.0,
                                         dL = 0.6,
                                         dEJ = 0.0,
                                         flux = 0.5,
                                         ng = 0.0,
                                         n_cut = 7,
                                         phi_cut = 7,
                                         zeta_cut = 30)


From within Jupyter notebook, a cosine two phi qubit instance can alternatively be created with::

   cos2phi_qubit = scqubits.Cosi2PhiQubit.create()

This functionality is  enabled if the ``ipywidgets`` package is installed, and displays GUI forms prompting for
the entry of the required parameters.


Calculational methods related to Hamiltonian and energy spectra
---------------------------------------------------------------

.. autosummary::

    scqubits.Cos2PhiQubit.hamiltonian
    scqubits.Cos2PhiQubit.eigenvals
    scqubits.Cos2PhiQubit.eigensys
    scqubits.Cos2PhiQubit.get_spectrum_vs_paramvals


Wavefunctions and visualization of eigenstates and the potential
----------------------------------------------------------------

.. autosummary::

    scqubits.Cos2PhiQubit.wavefunction
    scqubits.Cos2PhiQubit.plot_wavefunction
    scqubits.Cos2PhiQubit.plot_potential


Implemented operators
---------------------

The following operators are implemented for use in matrix element calculations.

.. autosummary::

    scqubits.Cos2PhiQubit.n_1_operator
    scqubits.Cos2PhiQubit.n_2_operator
    scqubits.Cos2PhiQubit.phi_1_operator
    scqubits.Cos2PhiQubit.phi_2_operator
    scqubits.Cos2PhiQubit.phi_operator
    scqubits.Cos2PhiQubit.n_phi_operator
    scqubits.Cos2PhiQubit.n_theta_operator
    scqubits.Cos2PhiQubit.zeta_operator
    scqubits.Cos2PhiQubit.n_zeta_operator



Computation and visualization of matrix elements
------------------------------------------------

.. autosummary::

    scqubits.Cos2PhiQubit.matrixelement_table
    scqubits.Cos2PhiQubit.plot_matrixelements
    scqubits.Cos2PhiQubit.get_matelements_vs_paramvals
    scqubits.Cos2PhiQubit.plot_matelem_vs_paramvals

   
Estimation of coherence times
-----------------------------

.. autosummary::

    scqubits.Cos2PhiQubit.plot_coherence_vs_paramvals
    scqubits.Cos2PhiQubit.plot_t1_effective_vs_paramvals
    scqubits.Cos2PhiQubit.plot_t2_effective_vs_paramvals
    scqubits.Cos2PhiQubit.t1_effective
    scqubits.Cos2PhiQubit.t2_effective
    scqubits.Cos2PhiQubit.t1_capacitive
    scqubits.Cos2PhiQubit.t1_inductive
    scqubits.Cos2PhiQubit.t1_purcell
    scqubits.Cos2PhiQubit.tphi_1_over_f
    scqubits.Cos2PhiQubit.tphi_1_over_f_cc
    scqubits.Cos2PhiQubit.tphi_1_over_f_flux
    scqubits.Cos2PhiQubit.tphi_1_over_f_ng
