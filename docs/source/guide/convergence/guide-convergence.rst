.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide_convergence:

**************************
Convergence Diagnostics
**************************

Every qubit in scqubits is represented by a finite matrix obtained by truncating
an underlying infinite-dimensional Hamiltonian. The transmon, for example, is
truncated to a finite charge basis controlled by ``ncut``; fluxonium uses a
harmonic-oscillator basis controlled by ``cutoff``; the grid-based qubits
discretize a flux coordinate. The numbers scqubits returns -- energies,
wavefunctions, matrix elements, coherence times -- are only as accurate as that
truncation allows. If the cutoff is too small, results are silently wrong; if it
is far too large, calculations are needlessly slow.

The convergence-diagnostics framework answers a single practical question: *for
the cutoff I have chosen, how accurate is the result, and what should I do if it
is not accurate enough?* The recommended way to get a trustworthy answer is
**verified refinement**: scqubits re-runs your calculation at a larger cutoff and
compares. Cheap estimates are also available for fast feedback, but they are
labeled as such and are never presented as a substitute for an actual
comparison.

.. note::

   Convergence diagnostics are available for the :class:`.Transmon`, covering
   the energy spectrum, wavefunctions, matrix elements, and coherence rates.
   Calling ``estimate_convergence`` on a qubit class that does not support it
   raises :class:`TypeError`.


The basic workflow
==================

Achieving a converged result is a short loop: estimate, read the verdict, and --
if necessary -- increase the cutoff and repeat.

1. **Build the qubit** at an initial cutoff::

       import scqubits as scq

       tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=31, truncated_dim=6)

2. **Estimate convergence** for the levels you care about. You either call the
   method on the qubit or use the top-level shim; they are equivalent::

       report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-4)
       # identical to:
       report = scq.estimate_convergence(tmon, n_levels=5, target_abs_GHz=1e-4)

3. **Read the verdict**::

       print(report.aggregate_status)        # e.g. 'converged'
       print(report.worst_level)             # the level driving the verdict
       for verdict in report.per_level:
           print(verdict.level_index, verdict.status, verdict.abs_err_est_GHz)

4. **Act on the recommendation.** If the result is not converged, the report
   tells you what to change::

       if report.aggregate_status != "converged":
           for line in report.recommendations:
               print(line)
       # e.g. "increase ncut from 6 to at least 10 and re-run; the worst-level
       #       estimate exceeded the target threshold"

   Apply the suggestion and repeat from step 2. A typical loop converges in one
   or two iterations.

The default mode (``mode='verify'``) performs one extra diagonalization at a
larger cutoff and compares the two spectra level by level. This is the
recommended setting for any result you intend to publish or rely on.


Setting a target
================

A convergence verdict only means something relative to a target accuracy. In the
default **absolute** scope you must say how accurate you need the energies to be,
in GHz, via ``target_abs_GHz``::

    report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-4)

The thresholds are then:

* ``abs_err_est_GHz < target_abs_GHz``                    -> ``converged``
* ``target_abs_GHz <= abs_err_est_GHz < 10 * target``     -> ``marginal``
* ``abs_err_est_GHz >= 10 * target_abs_GHz``              -> ``underconverged``

If you omit ``target_abs_GHz``, scqubits will still compute and report the
per-level error estimate ``abs_err_est_GHz``, but it will not convert that into a
pass/fail status -- the status is reported as ``unverified``, and a
recommendation reminds you to supply a target. This lets you inspect the raw
error before committing to a threshold::

    report = tmon.estimate_convergence(n_levels=5)   # no target
    for v in report.per_level:
        print(v.level_index, v.abs_err_est_GHz)      # estimates, no verdict

If you care about error *relative to the qubit's own spectrum* rather than an
absolute energy, choose the observed-gap scope::

    report = tmon.estimate_convergence(
        n_levels=5, scope="observed_gap_scale", target_gap_rel=1e-3
    )

Here the per-level error is divided by the local spectral gap (the smaller of the
gaps to the neighboring levels), floored at ``g_floor_GHz`` (default
:math:`10^{-3}` GHz = 1 MHz) to avoid dividing by an accidentally tiny gap. The
default relative target is :math:`10^{-3}`.

.. note::

   The observed-gap scope normalizes by an *observed* spectral gap, never by a
   basis-set frequency scale. A basis parameter such as the fluxonium LC
   frequency is useful internally but is not a physical low-energy scale, so it
   is deliberately not used as a reporting denominator.


Choosing a mode
===============

The ``mode`` argument trades cost for confidence.

``mode='quick'``
    Cheap diagnostic only -- **no extra diagonalization**. For the transmon, this
    inspects the boundary amplitudes of the eigenvectors you already have
    (:math:`|c_{-n_{\rm cut}}|^2 + |c_{+n_{\rm cut}}|^2`). A small boundary
    amplitude is a good sign, but it is not a measurement of the error, so quick
    mode never returns ``converged``: the best status it can assign is
    ``likely_converged``. Use it for rapid at-a-glance feedback while exploring
    parameters.

``mode='verify'`` (default)
    One refinement diagonalization at a larger cutoff, compared against the
    current one. This is an actual measurement of how much the spectrum is still
    moving, and it is the recommended setting for results you rely on. Evidence
    is reported as ``verified_empirical``.

``mode='strict'``
    Two refinement diagonalizations, used to run a ratio test that checks the
    spectrum is in the asymptotic (geometrically converging) regime before
    trusting a tail-extrapolated error estimate. When the ratio test succeeds the
    evidence is upgraded to ``calibrated``; when it cannot confirm asymptotic
    behavior it falls back to the one-step ``verified_empirical`` estimate and
    records a warning. Use it for publication-grade or automated workflows.

::

    quick   = tmon.estimate_convergence(n_levels=5, mode="quick")
    verify  = tmon.estimate_convergence(n_levels=5, mode="verify",
                                        target_abs_GHz=1e-4)
    strict  = tmon.estimate_convergence(n_levels=5, mode="strict",
                                        target_abs_GHz=1e-4)


Reading the report
==================

:meth:`.Transmon.estimate_convergence` returns a :class:`.ConvergenceReport`. Its
most useful fields are:

``aggregate_status``
    The overall verdict, equal to the worst per-level status. One of
    ``converged``, ``likely_converged``, ``marginal``, ``underconverged``,
    ``unverified``.

``per_level``
    A list of :class:`.LevelVerdict`, one per requested level. A failure of a
    high-lying level never hides the convergence of the lower levels -- inspect
    the list to see which levels are reliable.

``worst_level``
    The index of the level that determined the aggregate status.

``recommendations``
    Human-readable next steps (e.g. which cutoff to increase, by how much).

``clusters``
    Groups of near-degenerate levels. The diagnostic compares such levels as a
    set rather than by index, so an eigenvalue ordering swap between cutoffs does
    not produce a spurious convergence failure.

``implementation_audit``
    A record of exactly what was diagnosed: scqubits version, qubit class, basis,
    diagonalization method, cutoff parameters, the number of requested and buffer
    levels, and the mode/refinement used. This keeps a verdict tied to the
    backend it was produced with.

``derived``
    When derived quantities are requested (see below), a mapping from each
    requested quantity name to its own :class:`.ConvergenceReport`; ``None``
    otherwise.

Each :class:`.LevelVerdict` carries a ``status``, a ``status_scope``
(``absolute`` or ``observed_gap_scale``), an ``abs_err_est_GHz`` estimate, an
optional ``eps_gap_est``, a ``truncation_channel`` (the physical source of the
error, e.g. ``charge``), an ``estimator_method`` (how the estimate was obtained,
e.g. ``one_step`` or ``ratio_test``), any ``warnings``, and an ``evidence``
label.


Derived quantities
------------------

By default the report covers the energy spectrum. Pass ``include_derived=True``
together with ``derived_quantities`` to additionally assess any of
``"wavefunctions"``, ``"matrix_elements"``, and ``"coherence"``; each comes back
as its own :class:`.ConvergenceReport` under ``report.derived``::

    report = tmon.estimate_convergence(
        n_levels=5,
        mode="verify",
        target_abs_GHz=1e-4,
        include_derived=True,
        derived_quantities=["wavefunctions", "matrix_elements", "coherence"],
    )
    print(report.derived["wavefunctions"].aggregate_status)
    print(report.derived["matrix_elements"].aggregate_status)
    print(report.derived["coherence"].aggregate_status)

These reuse the same refinement diagonalization as the energy check, so they add
little cost, and they require ``mode='verify'`` or ``'strict'`` because a
refinement comparison is needed. In each sub-report ``eps_gap_est`` holds the
dimensionless change of the quantity between cutoffs.

**Wavefunctions** -- per level, the overlap deficit (one minus the wavefunction
overlap) for isolated levels, or the subspace angle for a near-degenerate
cluster, which is robust to eigenvector rotations within the block.

**Matrix elements** -- per level, the worst relative change of that level's
matrix-element row and column across every operator named by
``get_operator_names``. Because an operator weights the wavefunction, this can be
a stricter test than the bare overlap: an unbounded operator such as the charge
:math:`\hat n` amplifies a poorly-converged high-charge tail that the overlap
barely notices.

**Coherence** -- one verdict per noise channel (those returned by
``effective_noise_channels``, plus the aggregate :math:`T_1` and :math:`T_2`
rates), with the channel named in ``estimator_method``. Rates are compared first:
a channel whose rate falls below the noise floor carries a ``noise_floor``
warning instead of a lifetime claim.


The evidence ladder
-------------------

Every numerical conclusion is tagged with an ``evidence`` label so that you can
tell a theorem-grade bound from a cheap heuristic at a glance. From strongest to
weakest:

``certified``
    A bound with its hypotheses checked at runtime.

``verified_empirical``
    A refinement or cross-check with a ratio/asymptoticity/stability test --
    this is what ``mode='verify'`` produces.

``calibrated``
    An estimator validated against ground truth across a parameter range -- what
    a successful ``mode='strict'`` ratio test produces.

``perturbative``
    A perturbation-theory or resolvent estimate with unverified runtime
    hypotheses.

``diagnostic``
    A signal of possible trouble, not a measurement of the error -- what
    ``mode='quick'`` produces.

``unverified``
    Inputs unavailable, assumptions failed, or no target supplied.

The guiding principle is conservative: a cheap signal is never silently promoted
to a strong claim. ``converged`` is reserved for results backed by at least
``verified_empirical`` evidence.


A complete example
==================

Start with a deliberately small cutoff and let the loop guide you to a converged
result::

    import scqubits as scq

    tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=6, truncated_dim=6)

    report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report.aggregate_status)     # 'underconverged'
    print(report.recommendations[0])   # suggests increasing ncut

    # follow the recommendation
    tmon.ncut = 31
    report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report.aggregate_status)     # 'converged'

For a fast check while scanning parameters, drop the extra diagonalization::

    report = tmon.estimate_convergence(n_levels=5, mode="quick")
    print(report.aggregate_status)     # 'likely_converged' or 'unverified'

For a publication-grade check, demand the ratio test::

    report = tmon.estimate_convergence(
        n_levels=5, mode="strict", target_abs_GHz=1e-6
    )
    print(report.per_level[0].evidence)   # 'calibrated' if asymptotic


Settings
========

The defaults that control the diagnostics -- refinement step, cluster threshold,
safety factor, gap floor, rate floor, and default mode -- live in
:mod:`scqubits.settings` under the ``CONVERGENCE_*`` names and can be adjusted
globally; see the :ref:`guide-settings` section.
