.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

Dephasing
==============

Dephasing noise leads to loss of coherence, i.e., the relative phases associated with superpositions of multiple states
are lost over time.


1/f noise
---------------

One of the most important noise channels affecting superconducting qubits is 1/f noise. The spectral
density function characterizing this noise is given by

.. math::

   S(\omega) = \frac{2 \pi A_{\lambda}^{2} }{|\omega|}.

1/f noise typically leads to slow fluctuations of the energy-level spacing, resulting in dephasing [Ithier2005]_.
In the above expression, :math:`A_{\lambda}` corresponds to the amplitude or strength of the particular noise
channel :math:`\lambda`. scqubits uses sensible default values for this quantity based on the literature. Alternative
values can be set by the user.

The resulting dephasing time (away from sweet spots) is given by

.. math::

   T_{\phi} = \sqrt{2} A_{\lambda} \frac{\partial \omega_{01}}{\partial \lambda}  \sqrt{| \ln \omega_{\rm low} t_{\rm exp} |}


with the following parameters:

+--------------------------+---------------+----------------------+-----------------------+
| Parameter                | Default Value | Description          | Method Parameter Name |
+==========================+===============+======================+=======================+
| :math:`\omega_{\rm low}` | `1 rad/s`     | Low-frequency cutoff | ``omega_low``         |
+--------------------------+---------------+----------------------+-----------------------+
| :math:`t_{\rm exp}`      | `1 s`         | Experiment time      | ``t_exp``             | 
+--------------------------+---------------+----------------------+-----------------------+

The frequency derivatives in the above expressions are calculated from matrix elements of :math:`\partial_\lambda H`. The `Method Parameter Name` column in the above table describes the argument names that can be passed to various 1/f noise methods (see below) when one wants to use custom parameter values.

The general-purpose scqubits method for calculating 1/f dephasing times due to an arbitrary noise channel
is given by ``tphi_1_over_f()``. Depending on the qubit of interest, more specific methods for the different kinds
of 1/f noise channels are available. These set appropriate defaults for noise strength :math:`A_{\lambda}`,
the correct noise operator :math:`\partial_\lambda H`, etc.

See the API for method signatures. 

1/f flux noise
^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------+-----------------------------------------+
| Method name                                | ``tphi_1_over_f_flux``                  |
+--------------------------------------------+-----------------------------------------+
| Noise operator                             | :math:`\partial H/\partial \Phi_{x}`    |
+--------------------------------------------+-----------------------------------------+
| Default value of  :math:`A_{\lambda}`      |  :math:`10^{-6} \Phi_0`                 |
+--------------------------------------------+-----------------------------------------+

A custom value of :math:`A_{\lambda}` can be provided to the ``tphi_1_over_f_flux`` method using the ``A_noise`` parameter. 
See the API documentation of individual qubits for details.

Qubits that support this noise channel include: 
:ref:`Cos2phi <cos2phi_qubit>`,
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FluxQubit <qubit_flux_qubit>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`ZeroPi <qubit_zeropi>`.

1/f charge noise
^^^^^^^^^^^^^^^^^^^^^

+--------------------------------------------+-----------------------------------------+
| Method name                                | ``tphi_1_over_f_ng``                    |
+--------------------------------------------+-----------------------------------------+
| Noise operator                             | :math:`\partial H/\partial n_g`         |
+--------------------------------------------+-----------------------------------------+
| Default value of  :math:`A_{\lambda}`      |  :math:`10^{-4} e`                      |
+--------------------------------------------+-----------------------------------------+

A custom value of :math:`A_{\lambda}` can be provided to the ``tphi_1_over_f_ng`` method using the ``A_noise`` parameter. 
See the API documentation of individual qubits for details.


Qubits that support this noise channel include: 
:ref:`Cos2phi <cos2phi_qubit>`,
:ref:`FluxQubit <qubit_flux_qubit>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`Transmon <qubit_transmon>`, 
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`ZeroPi <qubit_zeropi>`.

1/f critical current noise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Critical-current noise is suspected to arise from trapping and de-trapping of charges at defect sites inside Josephson
junctions. These trapped charges then may locally suppress or enhance the tunneling across the junction, leading to
fluctuations of the critical current.


+--------------------------------------------+-----------------------------------------+
| Method name                                | ``tphi_1_over_f_cc``                    |
+--------------------------------------------+-----------------------------------------+
| Noise operator                             | :math:`\partial H/\partial I_{c}`       |
+--------------------------------------------+-----------------------------------------+
| Default value of  :math:`A_{\lambda}`      |  :math:`10^{-7} I_{c}`                  |
+--------------------------------------------+-----------------------------------------+

A custom value of :math:`A_{\lambda}` can be provided to the ``tphi_1_over_f_cc`` method using the ``A_noise`` parameter. 
See the API documentation of individual qubits for details.


Qubits that support this noise channel include: 
:ref:`Cos2phi <cos2phi_qubit>`,
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FluxQubit <qubit_flux_qubit>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`Transmon <qubit_transmon>`, 
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`ZeroPi <qubit_zeropi>`.

Shot noise
---------------

.. todo:: To be added for certain qubits


