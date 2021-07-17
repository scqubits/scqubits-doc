.. scqubits
   Copyright (C) 2017 and later, Jens Koch & Peter Groszkowski

Depolarization
================

Noise may cause depolarization of the qubit by inducing spontaneous transitions among eigenstates. scqubits uses the
standard perturbative approach (Fermi's Golden Rule) to approximate the resulting transition rates due to different
noise channels.

The rate of a transition from state :math:`i` to state :math:`j` can be expressed as

.. math::

   \Gamma_{ij} = \frac{1}{\hbar^2} |\langle i| B_{\lambda} |j \rangle|^2 S(\omega_{ij}),

where :math:`B_\lambda` is the noise operator, and :math:`S(\omega_{ij})` the spectral density function evaluated at
the angular frequency associated with the transition frequeny, :math:`\omega_{ij} = \omega_{j} - \omega_{i}`.
:math:`\omega_{ij}` is positive in the case of  decay (the qubit emits energy to the bath), and negative in case of
excitations (the qubit absorbs energy from the bath).

Unless stated otherwise, it is assumed that the depolarizing noise channels satisfy detailed balanced. This implies

.. math::

    \frac{S(\omega)}{S(-\omega)} = \exp{\frac{\hbar \omega}{k_B T}},

where :math:`T` is the bath temperature, and :math:`k_B` Boltzmann's constant.


.. note::

    By default all :math:`t_1` methods estimate the coherence depolarization times from the sum of the upward and downard rates.  
    This behavior is controlled by the arugment `total`, which can be modified by the user. For example, setting `total=False` 
    will calculate only a single-directional transition rate from the state indexed `i` to the state indexed `j` (both of which
    cal also be changed by the user through providing their values as arguments) 


Capacitive noise
-----------------------

+-------------------+--------------------+
| Noise operator    | ``t1_capacitive``  |
+===================+====================+
| :math:`B_\lambda` | :math:`2e \hat{n}` |
+-------------------+--------------------+

Capacitive noise corresponds to noise coming from a lossy capacitance. The assumed spectral density reads

.. math::

    S(\omega) = \frac{\omega \hbar}{|\omega| C_J Q_{\rm cap}(\omega)} \left(1 + \coth \frac{\hbar |\omega|}{2 k_B T} \right)

where :math:`C_J` is the relevant capacitance, and :math:`Q_{\rm cap}` the corresponding capacitive quality factor.
The default value of the frequency-dependent quality factor is assumed to be

.. math::

    Q_{\rm cap}(\omega) =  10^{6}  \left( \frac{2 \pi \times 6 {\rm GHz} }{ |\omega|} \right)^{0.7}. 

To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are
:ref:`Cos2phi <cos2phi_qubit>`,
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`ZeroPi <qubit_zeropi>`.

The parameters that determine what transitions are taken into account during the calculation of :math:`T_1` due to this channel, 
are ``i``, ``j`` and ``total``. Their properties are described below. 

+----------------+---------------+----------------------------------------------------------------------------------+
| Parameter name | Default value | Description                                                                      |
+================+===============+==================================================================================+
| i              | 1             | Index of the first state involved in the transition                              |
+----------------+---------------+----------------------------------------------------------------------------------+
| j              | 0             | Index of the second state involved in the transition                             |
+----------------+---------------+----------------------------------------------------------------------------------+
| total          | True          | Determines how the :math:`T_1` time (or rate) is calculated.                     |
|                |               |                                                                                  |
|                |               | If ``total=False`` then a transition from state ``i`` to state ``j`` is assumed. |
|                |               | Depending on whether :math:`i>j` or :math:`i<j`, the resulting :math:`T_1`       |
|                |               | time (or rate) corresponds to a relaxation or excitation process, respectively.  |
|                |               |                                                                                  |
|                |               | If ``total=True`` then both transition rates from ``j`` to ``i``                 |
|                |               | and ``i`` to ``j`` are combined to give  total effective depolarization          |
|                |               | time (or rate).                                                                  |
+----------------+---------------+----------------------------------------------------------------------------------+


.. warning::

    By default, ``total=True`` is used when calculating the :math:`T_1` coherence time for this channel.
    This means that both the excitation and relaxation rates are combined to give an effective :math:`T_1` 
    depolarization time (or rate). See table above for details. 

Other parameters that could be used for further customization are:

+----------------+-----------------------------+------------------------------------------------+
| Parameter name | Default value               | Description                                    |
+================+=============================+================================================+
| Q_cap          | :math:`Q_{\rm cap}(\omega)` | Capacitive quality factor                      |
|                |                             |                                                |
|                |                             | Can be function of :math:`\omega`, or a number |
+----------------+-----------------------------+------------------------------------------------+
| T              | 0.015                       | Temperature (in K)                             |
+----------------+-----------------------------+------------------------------------------------+
| get_rate       | False                       | Return rate instead of time                    |
+----------------+-----------------------------+------------------------------------------------+


References: [Nguyen2019]_, [Smith2020]_  

Inductive noise
-----------------------

+-------------------+----------------------------------------+
| Noise operator    | ``t1_inductive``                       |
+===================+========================================+
| :math:`B_\lambda` | :math:`\frac{\Phi_0}{2\pi} \hat{\phi}` |
+-------------------+----------------------------------------+

Inductive noise due to lossy inductance. The assumed spectral density reads

.. math::

    S(\omega) = \frac{\omega \hbar}{|\omega| L_{J} Q_{\rm ind}(\omega)} \left(1 + \coth \frac{\hbar |\omega|}{2 k_B T} \right)

where :math:`L_J` is the relevant inductance or superinductance, and :math:`Q_{\rm ind}` the corresponding inductive
quality factor. The default value of the frequency-dependent quality factor is assumed to be

.. math::

    Q_{\rm ind}(\omega) =  500 \times 10^{6} \frac{ K_{0} \left( \frac{h \times 0.5 {\rm GHz}}{2 k_B T} \right) 
    \sinh \left( \frac{h \times 0.5 {\rm GHz} }{2 k_B T} \right)}{K_{0} \left( \frac{\hbar |\omega|}{2 k_B T} \right)\
    \sinh \left( \frac{\hbar |\omega| }{2 k_B T} \right)},

where :math:`K_0` is the Bessel function of the second kind. 


To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are:
:ref:`Cos2phi <cos2phi_qubit>`,
:ref:`Fluxonium <qubit_fluxonium>`.

The parameters that determine what transitions are taken into account during the calculation of :math:`T_1` due to this channel, 
are ``i``, ``j`` and ``total``. Their properties are described below. 

+----------------+---------------+----------------------------------------------------------------------------------+
| Parameter name | Default value | Description                                                                      |
+================+===============+==================================================================================+
| i              | 1             | Index of the first state involved in the transition                              |
+----------------+---------------+----------------------------------------------------------------------------------+
| j              | 0             | Index of the second state involved in the transition                             |
+----------------+---------------+----------------------------------------------------------------------------------+
| total          | True          | Determines how the :math:`T_1` time (or rate) is calculated.                     |
|                |               |                                                                                  |
|                |               | If ``total=False`` then a transition from state ``i`` to state ``j`` is assumed. |
|                |               | Depending on whether :math:`i>j` or :math:`i<j`, the resulting :math:`T_1`       |
|                |               | time (or rate) corresponds to a relaxation or excitation process, respectively.  |
|                |               |                                                                                  |
|                |               | If ``total=True`` then both transition rates from ``j`` to ``i``                 |
|                |               | and ``i`` to ``j`` are combined to give  total effective depolarization          |
|                |               | time (or rate).                                                                  |
+----------------+---------------+----------------------------------------------------------------------------------+


.. warning::

    By default, ``total=True`` is used when calculating the :math:`T_1` coherence time for this channel.
    This means that both the excitation and relaxation rates are combined to give an effective :math:`T_1` 
    depolarization time (or rate). See table above for details. 

Other parameters that could be used for further customization are:


+----------------+-----------------------------+------------------------------------------------+
| Parameter name | Default value               | Description                                    |
+================+=============================+================================================+
| Q_ind          | :math:`Q_{\rm ind}(\omega)` | Inductive quality factor                       |
|                |                             |                                                |
|                |                             | Can be function of :math:`\omega`, or a number |
+----------------+-----------------------------+------------------------------------------------+
| T              | 0.015                       | Temperature (in K)                             |
+----------------+-----------------------------+------------------------------------------------+
| get_rate       | False                       | Return rate instead of time                    |
+----------------+-----------------------------+------------------------------------------------+



References: [Nguyen2019]_, [Smith2020]_  

Charge-coupled impedance noise
------------------------------

+--------------------------------------------+-----------------------------------------+
| Noise operator                             | ``t1_charge_impedance``                 |
+--------------------------------------------+-----------------------------------------+
| :math:`B_\lambda`                          | :math:`2e \hat{n}`                      |
+--------------------------------------------+-----------------------------------------+

Noise from a charge coupling to an impedance :math:`Z(\omega)`. The assumed spectral density reads

.. math::

    S(\omega) = \frac{\hbar \omega}{{\rm Re} Z(\omega)} \left(1 + \coth \frac{\hbar |\omega|}{2 k_B T} \right).

By default we assume the qubit couples to a infinite transmission line, which leads to 

.. math::

   {\rm Re} Z(\omega) = 50 \Omega.

To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`.


The parameters that determine what transitions are taken into account during the calculation of :math:`T_1` due to this channel, 
are ``i``, ``j`` and ``total``. Their properties are described below. 

+----------------+---------------+----------------------------------------------------------------------------------+
| Parameter name | Default value | Description                                                                      |
+================+===============+==================================================================================+
| i              | 1             | Index of the first state involved in the transition                              |
+----------------+---------------+----------------------------------------------------------------------------------+
| j              | 0             | Index of the second state involved in the transition                             |
+----------------+---------------+----------------------------------------------------------------------------------+
| total          | True          | Determines how the :math:`T_1` time (or rate) is calculated.                     |
|                |               |                                                                                  |
|                |               | If ``total=False`` then a transition from state ``i`` to state ``j`` is assumed. |
|                |               | Depending on whether :math:`i>j` or :math:`i<j`, the resulting :math:`T_1`       |
|                |               | time (or rate) corresponds to a relaxation or excitation process, respectively.  |
|                |               |                                                                                  |
|                |               | If ``total=True`` then both transition rates from ``j`` to ``i``                 |
|                |               | and ``i`` to ``j`` are combined to give  total effective depolarization          |
|                |               | time (or rate).                                                                  |
+----------------+---------------+----------------------------------------------------------------------------------+


.. warning::

    By default, ``total=True`` is used when calculating the :math:`T_1` coherence time for this channel.
    This means that both the excitation and relaxation rates are combined to give an effective :math:`T_1` 
    depolarization time (or rate). See table above for details. 

Other parameters that could be used for further customization are:

+----------------+---------------+----------------------------------------------------+
| Parameter name | Default value | Description                                        |
+================+===============+====================================================+
| Z              | 50            | Complex Impedance of coupled line (:math:`\Omega`) |
|                |               |                                                    |
|                |               | Can be function of :math:`\omega`, or a number     |
+----------------+---------------+----------------------------------------------------+
| T              | 0.015         | Temperature (in K)                                 |
+----------------+---------------+----------------------------------------------------+
| get_rate       | False         | Return rate instead of time                        |
+----------------+---------------+----------------------------------------------------+


References: [Schoelkopf2003]_, [Ithier2005]_

Flux-bias line noise
-------------------------

+-------------------+--------------------------------------------------+
| Noise operator    | ``t1_flux_bias_line``                            |
+===================+==================================================+
| :math:`B_\lambda` | :math:`\frac{\partial \hat{H}}{\partial \Phi_x}` |
+-------------------+--------------------------------------------------+

Noise due to current noisy biasing current coupled to the qubit via flux. The assumed spectral density reads

.. math::

    S(\omega) = \frac{M^{2} \omega \hbar}{R} \left(1 + \coth \frac{\hbar |\omega|}{2 k_B T} \right),

where :math:`M` is the mutual inductance between qubit and the flux line.

To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`ZeroPi <qubit_zeropi>`.

The parameters that determine what transitions are taken into account during the calculation of :math:`T_1` due to this channel, 
are ``i``, ``j`` and ``total``. Their properties are described below. 

+----------------+---------------+----------------------------------------------------------------------------------+
| Parameter name | Default value | Description                                                                      |
+================+===============+==================================================================================+
| i              | 1             | Index of the first state involved in the transition                              |
+----------------+---------------+----------------------------------------------------------------------------------+
| j              | 0             | Index of the second state involved in the transition                             |
+----------------+---------------+----------------------------------------------------------------------------------+
| total          | True          | Determines how the :math:`T_1` time (or rate) is calculated.                     |
|                |               |                                                                                  |
|                |               | If ``total=False`` then a transition from state ``i`` to state ``j`` is assumed. |
|                |               | Depending on whether :math:`i>j` or :math:`i<j`, the resulting :math:`T_1`       |
|                |               | time (or rate) corresponds to a relaxation or excitation process, respectively.  |
|                |               |                                                                                  |
|                |               | If ``total=True`` then both transition rates from ``j`` to ``i``                 |
|                |               | and ``i`` to ``j`` are combined to give  total effective depolarization          |
|                |               | time (or rate).                                                                  |
+----------------+---------------+----------------------------------------------------------------------------------+


.. warning::

    By default, ``total=True`` is used when calculating the :math:`T_1` coherence time for this channel.
    This means that both the excitation and relaxation rates are combined to give an effective :math:`T_1` 
    depolarization time (or rate). See table above for details. 

Other parameters that could be used for further customization are:

+----------------+---------------+---------------------------------------------------------------------+
| Parameter name | Default value | Description                                                         |
+================+===============+=====================================================================+
| M              | 400           | Mutual inductance between qubit and flux line (in :math:`\Phi_0/A`) |
+----------------+---------------+---------------------------------------------------------------------+
| Z              | 50            | Complex impedance of bias flux line (:math:`\Omega`)                |
|                |               |                                                                     |
|                |               | Can be function of :math:`\omega`, or a number                      |
+----------------+---------------+---------------------------------------------------------------------+
| T              | 0.015         | Temperature (in K)                                                  |
+----------------+---------------+---------------------------------------------------------------------+
| get_rate       | False         | Return rate instead of time                                         |
+----------------+---------------+---------------------------------------------------------------------+


References: [Koch2007]_, [Groszkowski2018]_, 

Quasiparticle-tunneling noise
----------------------------------

+-------------------+--------------------------------------------------+
| Noise operator    | ``t1_quasiparticle_tunneling``                   |
+===================+==================================================+
| :math:`B_\lambda` | :math:`\sin(\hat{\phi}/2)`  (see note ** below)  |
+-------------------+--------------------------------------------------+

Noise due to quasiparticle tunelling. The assumed spectral density reads

.. math::

    S(\omega) = \hbar \omega {\rm Re} Y_{\rm qp}(\omega) \left(1 + \coth \frac{\hbar |\omega|}{2 k_B T} \right)

where :math:`L_J` (with :math:`E_J = \phi_0^2/L_J` ) is the relevant inductance or superinductance, and :math:`Q_{\rm ind}` the corresponding inductive
quality factor. The default value of the frequency-dependent quality factor is assumed to be

The default real part of admittance is assumed to be 

.. math::

    {\rm Re} Y_{\rm qp}(\omega) = \sqrt{\frac{2}{\pi}} \frac{8 E_J}{R_k \Delta} \
    \left(\frac{2 \Delta}{\hbar \omega} \right)^{3/2}  x_{\rm qp} \
    K_{0} \left( \frac{\hbar |\omega|}{2 k_B T} \right) \sinh \left( \frac{\hbar \omega }{2 k_B T} \right).

** This form assumes that the external flux is grouped with the inductive term of the Hamiltonian. In qubits where the flux is grouped with the Josephson term, the noise operator is appropriately transformed.  

To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`ZeroPi <qubit_zeropi>`.

The parameters that determine what transitions are taken into account during the calculation of :math:`T_1` due to this channel, 
are ``i``, ``j`` and ``total``. Their properties are described below. 

+----------------+---------------+----------------------------------------------------------------------------------+
| Parameter name | Default value | Description                                                                      |
+================+===============+==================================================================================+
| i              | 1             | Index of the first state involved in the transition                              |
+----------------+---------------+----------------------------------------------------------------------------------+
| j              | 0             | Index of the second state involved in the transition                             |
+----------------+---------------+----------------------------------------------------------------------------------+
| total          | True          | Determines how the :math:`T_1` time (or rate) is calculated.                     |
|                |               |                                                                                  |
|                |               | If ``total=False`` then a transition from state ``i`` to state ``j`` is assumed. |
|                |               | Depending on whether :math:`i>j` or :math:`i<j`, the resulting :math:`T_1`       |
|                |               | time (or rate) corresponds to a relaxation or excitation process, respectively.  |
|                |               |                                                                                  |
|                |               | If ``total=True`` then both transition rates from ``j`` to ``i``                 |
|                |               | and ``i`` to ``j`` are combined to give  total effective depolarization          |
|                |               | time (or rate).                                                                  |
+----------------+---------------+----------------------------------------------------------------------------------+


.. warning::

    By default, ``total=True`` is used when calculating the :math:`T_1` coherence time for this channel.
    This means that both the excitation and relaxation rates are combined to give an effective :math:`T_1` 
    depolarization time (or rate). See table above for details. 

Other parameters that could be used for further customization are:

+----------------+-------------------------------------+------------------------------------------------+
| Parameter name | Default value                       | Description                                    |
+================+=====================================+================================================+
| Y_qp           | :math:`Y_{\rm qp}`                  | Complex admittance (:math:`\Omega`)            |
|                |                                     |                                                |
|                |                                     | Can be function of :math:`\omega`, or a number |
+----------------+-------------------------------------+------------------------------------------------+
| x_qp           | :math:`3 \times 10^{-6}`            | Quasiparticle density                          |
+----------------+-------------------------------------+------------------------------------------------+
| T              | 0.015                               | Temperature (in K)                             |
+----------------+-------------------------------------+------------------------------------------------+
| Delta          | :math:`3.4 \times 10^{-4}` (for Al) | Superconducting gap (eV)                       |
+----------------+-------------------------------------+------------------------------------------------+
| get_rate       | False                               | Return rate instead of time                    |
+----------------+-------------------------------------+------------------------------------------------+


References: [Catelani2011]_, [Nguyen2019]_, [Pop2014]_, [Smith2020]_

User-defined noise
-----------------------

+--------------------------------------------+-----------------------------------------+
| Noise operator                             | ``t1``                                  |
+--------------------------------------------+-----------------------------------------+
| :math:`B_\lambda`                          | user defined                            |
+--------------------------------------------+-----------------------------------------+

All qubits support user defined noise, where both the noise operator as well as an arbitrary spectral density can be provided. 
To see a detailed signature of this method, see the API description of qubits that support this particular noise channel. These are
:ref:`Fluxonium <qubit_fluxonium>`, 
:ref:`FluxQubit <qubit_flux_qubit>`, 
:ref:`FullZeroPi <qubit_fullzeropi>`, 
:ref:`Transmon <qubit_tunable_transmon>`, 
:ref:`TunableTransmon <qubit_tunable_transmon>`, 
:ref:`ZeroPi <qubit_zeropi>`.

