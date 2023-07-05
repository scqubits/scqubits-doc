.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski


.. _install-verify:

Verifying the Install
=====================

scqubits includes a set of tests that can be executed to verify that installation was successful:

.. code-block:: python

   import scqubits.testing as sctest
   sctest.run()

This requires the ``pytest`` package.
