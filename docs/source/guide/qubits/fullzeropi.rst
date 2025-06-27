.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

.. _qubit_fullzeropi:

`FullZeroPi`
============

.. figure:: ../../graphics/fullzeropi.png
   :align: center
   :width: 4in

The full Zero-Pi qubit [Brooks2013]_ [Dempster2014]_ includes the coupling of the
primary qubit degrees of freedom to the zeta mode. It is described by the
Hamiltonian :math:`H = H_{0-\pi} + H_\text{int} + H_\zeta`, where

.. math::
   H_{0-\pi} =& -2E_\text{CJ}\partial_\phi^2+2E_{\text{C}\Sigma}(i\partial_\theta-n_g)^2
    +2E_{C\Sigma}dC_J\,\partial_\phi\partial_\theta\\
     & -2E_\text{J}\cos\theta\cos(\phi-\varphi_\text{ext}/2)+E_L\phi^2+2E_\text{J}
    + E_J dE_J \sin\theta\sin(\phi-\varphi_\text{ext}/2) \\
   H_\text{int} =& 2E_{C\Sigma}dC\,\partial_\theta\partial_\zeta + E_L dE_L \phi\,\zeta\\
   H_\zeta =& \omega_\zeta a^\dagger a

expressed in the phase basis. The definition of the relevant charging energies
:math:`E_\text{CJ}`, :math:`E_{\text{C}\Sigma}`,
Josephson energies :math:`E_\text{J}`, inductive energies :math:`E_\text{L}`, and relative amounts of disorder
:math:`dC_\text{J}`, :math:`dE_\text{J}`, :math:`dC`, :math:`dE_\text{L}` follows [Groszkowski2018]_.
Internally, the ``FullZeroPi`` class formulates the Hamiltonian matrix via the product basis of the decoupled Zero-Pi
qubit (realized by ``ZeroPi``)  on one hand, and the zeta LC oscillator on the other hand.

An instance of the full Zero-Pi qubit is created as follows::

   phi_grid = scqubits.Grid1d(-6*np.pi, 6*np.pi, 200)

   zero_pi = scqubits.FullZeroPi(grid = phi_grid,
                                EJ   = 0.25,
                                EL   = 10.0**(-2),
                                ECJ  = 0.5,
                                EC   = 0.001,
                                dEJ  = 0.05,
                                dCJ  = 0.05,
                                dEL  = 0.01,
                                dC   = 0.08,
                                ng   = 0.1,
                                flux = 0.23,
                                ncut = 30,
                                zeropi_cutoff = 10,
                                zeta_cutoff = 30)

Here, ``flux`` is given in in terms of the flux quantum, i.e., in the form :math:`\Phi_\text{ext}/\Phi_0`. In the above example,
the disorder parameters ``dEJ`` and ``dCJ`` are not specified, and hence take on the default value zero (no disorder).

From within Jupyter notebook, an instance of the disordered Zero-Pi qubit can alternatively be created with::

   zero_pi = scqubits.FullZeroPi.create()

This functionality is  enabled if the ``ipywidgets`` package is installed, and displays GUI forms prompting for
the entry of the required parameters.



Calculational methods related to Hamiltonian and energy spectra
---------------------------------------------------------------

.. autosummary::
   :toctree: ../../_generated/

    scqubits.FullZeroPi.hamiltonian
    scqubits.FullZeroPi.eigenvals
    scqubits.FullZeroPi.eigensys
    scqubits.FullZeroPi.get_spectrum_vs_paramvals


Implemented operators
---------------------

The following operators are implemented for use in matrix element calculations.

.. autosummary::
   :toctree: ../../_generated/

    scqubits.FullZeroPi.i_d_dphi_operator
    scqubits.FullZeroPi.phi_operator
    scqubits.FullZeroPi.n_theta_operator


Computation and visualization of matrix elements
------------------------------------------------

.. autosummary::
   :toctree: ../../_generated/

    scqubits.FullZeroPi.matrixelement_table
    scqubits.FullZeroPi.plot_matrixelements
    scqubits.FullZeroPi.get_matelements_vs_paramvals
    scqubits.FullZeroPi.plot_matelem_vs_paramvals
    scqubits.FullZeroPi.g_coupling_matrix
    scqubits.FullZeroPi.g_phi_coupling_matrix
    scqubits.FullZeroPi.g_theta_coupling_matrix

Utility method for setting charging energies
--------------------------------------------

.. autosummary::
   :toctree: ../../_generated/

    scqubits.ZeroPi.set_EC_via_ECS
