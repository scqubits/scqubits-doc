.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide_units:

***************
Units
***************

scqubits provides a means to set default units for the assumed energies of the quantum systems. These units play a key
role in :ref:`guide_noise` calculations. They are also used to set axes labels in some plot types.

The currently supported units can be shown in a list using the function ``show_supported_units``. These are: ``GHz`` (default), ``MHz``, ``kHz`` and ``Hz``. The package also sets Plank's constant $h = 1$, meaning energy and linear frequency have the same units. 

The current units setting can be obtained with the ``get_units`` function. A new setting can be established with the
``set_units`` function::
    
    import scqubits as scq
    scq.get_units()
    scq.set_units('MHz')

scqubits also includes several helper functions for convenient conversion from the current system units to and
from `Hz`. This is accomplished with functions ``to_standard_units`` and ``from_standard_units``.


Examples
--------

Let's start by creating a Transmon from a given $E_J, E_C$. Written in code looks like::

   scqubits.set_units('GHz')
   
   tmon = scqubits.Transmon(EJ=30.02,       # Linear GHz
                            EC=1.2,         # Linear GHz
                            ng=0.3,
                            ncut=31)
   energies = tmon.eigenvals(evals_count=3) # Outputs in Linear GHz

Now let's do the inverse. For a given qubit's resonsant frequency $f_{01}$ and anharmonicity $\\alpha$$, determine $E_J, E_C$. Written in code looks like::

   qubit_01_freq = 3.882           # Linear GHz
   qubit_anharmonicity = -0.180    # Linear GHz
   
   EJ, EC = TunableTransmon.find_EJ_EC(E01=qubit_01_freq, anharmonicity=qubit_anharmonicity) # Outputs in Linear GHz
