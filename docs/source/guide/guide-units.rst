.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide_units:

***************
Units
***************

scqubits provides a means to set default units for the assumed energies of the quantum systems. These units play a key
role in :ref:`guide_noise` calculations. They are also used to set axes labels in some plot types.

The currently supported units can be shown in a list using the function ``show_supported_units``. These are: ``GHz`` (default), ``MHz``, ``kHz`` and ``Hz``. The package also assumes Plank's constant $h = 1$, meaning energy and frequency have the same units. 

The current units setting can be obtained with the ``get_units`` function. A new setting can be established with the
``set_units`` function::
    
    import scqubits as scq
    scq.get_units()
    scq.set_units('MHz')

scqubits also includes several helper functions for convenient conversion from the current system units to and
from `Hz`. This is accomplished with functions ``to_standard_units`` and ``from_standard_units``.

***************
Examples
***************
Defining ``EJ`` and ``EC`` would refer to $E_J / 2\\pi$ and $E_C /2\\pi$ in literature. Written in code looks like::

   scqubits.set_units('GHz')
   
   tmon = scqubits.Transmon(EJ=30.02,       # Linear GHz
                            EC=1.2,         # Linear GHz
                            ng=0.3,
                            ncut=31)
   energies = tmon.eigenvals(evals_count=3) # Outputs in Linear GHz

Another example starts with defining ``qubit_01_freq`` and ``qubit_anharmonicity`` which corresponds to $f_{01} = \\omega_{01} / 2 \\pi$ and $\\alpha / 2 \\pi$. Written in code looks like::

   qubit_01_freq = 3.882           # Linear GHz
   qubit_anharmonicity = -0.180    # Linear GHz
   
   EJ, EC = TunableTransmon.find_EJ_EC(E01=qubit_01_freq, anharmonicity=qubit_anharmonicity) # Outputs in Linear GHz
