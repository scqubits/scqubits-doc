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
discretize a flux coordinate on a finite box. The numbers scqubits returns --
energies, wavefunctions, matrix elements, coherence times -- are only as accurate
as that truncation allows. If the cutoff is too small, results are silently
wrong; if it is far too large, calculations are needlessly slow.

The convergence-diagnostics framework answers a single practical question: *for
the cutoff I have chosen, how accurate is the result, and what should I do if it
is not accurate enough?* The recommended way to get a trustworthy answer is
**verified refinement**: scqubits re-runs your calculation at a larger cutoff and
compares. Cheap estimates are also available for fast feedback, but they are
labeled as such and are never presented as a substitute for an actual comparison.

.. note::

   Convergence diagnostics are available for :class:`.Transmon`,
   :class:`.TunableTransmon`, :class:`.Fluxonium`, :class:`.FluxQubit`, and
   :class:`.ZeroPi`, covering the energy spectrum and -- on request -- the
   wavefunctions, matrix elements, and coherence rates. Calling
   ``estimate_convergence`` on a qubit class that does not support it raises
   :class:`TypeError`.


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

3. **Read the verdict.** The report prints itself::

       print(report)                  # human-readable summary of every level
       print(report.aggregate_status) # e.g. 'converged'
       worst = report.level(report.worst_level)   # the driving level's verdict

4. **Act on the recommendation.** If the result is not converged, the report
   tells you what to change::

       for line in report.recommendations:
           print(line)
       # e.g. "charge-basis tail dominates: increase ncut from 6 to at least 10
       #       (charge cutoff) and re-run"

   Apply the suggestion and repeat from step 2. A typical loop converges in one
   or two iterations.

The default mode (``mode='verify'``) performs one extra diagonalization at a
larger cutoff and compares the two spectra level by level. This is the
recommended setting for any result you intend to publish or rely on.


Notation
========

Let :math:`N` be the cutoff parameter and :math:`E_{k,N}` the :math:`k`-th
computed eigenvalue. The (unknown) true error of a level is
:math:`\Delta E_{k,N} = |E_{k,N} - E_k|`; every diagnostic reports an *estimate*
:math:`\widehat{\mathrm{err}}_{k,N} \approx \Delta E_{k,N}`, never the true error
itself, and attaches an evidence label saying how the estimate was obtained. A
refinement bumps the cutoff to :math:`N_1 > N_0` (and, in strict mode, a second
:math:`N_2 > N_1`); the per-level movements are

.. math::

   d_{0,k} = |E_{k,N_1} - E_{k,N_0}|, \qquad
   d_{1,k} = |E_{k,N_2} - E_{k,N_1}|.

A safety factor :math:`S` (default :math:`2`, ``settings.CONVERGENCE_SAFETY_FACTOR``)
multiplies one-step estimates.


Setting a target
================

A convergence verdict only means something relative to a target accuracy. In the
default **absolute** scope you say how accurate you need the energies to be, in
GHz, via ``target_abs_GHz`` :math:`\equiv \Delta_\star`. With
:math:`\widehat{\mathrm{err}}_{k}` the per-level estimate the status is

.. math::

   \begin{aligned}
   \widehat{\mathrm{err}}_{k} < \Delta_\star &\;\Rightarrow\; \texttt{converged}, \\
   \Delta_\star \le \widehat{\mathrm{err}}_{k} < 10\,\Delta_\star &\;\Rightarrow\; \texttt{marginal}, \\
   \widehat{\mathrm{err}}_{k} \ge 10\,\Delta_\star &\;\Rightarrow\; \texttt{underconverged}.
   \end{aligned}

If you omit ``target_abs_GHz``, scqubits still computes and reports the per-level
estimate ``abs_err_est_GHz``, but it does not convert that into a pass/fail
status -- the status is ``unverified`` and a recommendation reminds you to supply
a target.

If you care about error *relative to the qubit's own spectrum* rather than an
absolute energy, choose the observed-gap scope::

    report = tmon.estimate_convergence(
        n_levels=5, scope="observed_gap_scale", target_gap_rel=1e-3
    )

Here the per-level error is divided by the local isolation gap

.. math::

   g_{\rm iso}(k) =
   \begin{cases}
     E_{1,N}-E_{0,N}, & k=0,\\
     \min\{E_{k,N}-E_{k-1,N},\, E_{k+1,N}-E_{k,N}\}, & 0 < k < n_{\rm levels}-1,
   \end{cases}

floored at ``g_floor_GHz`` (default :math:`10^{-3}` GHz = 1 MHz) to avoid
dividing by an accidentally tiny gap, giving
:math:`\widetilde\epsilon_{{\rm gap},k} = \widehat{\mathrm{err}}_{k}/\max\{g_{\rm iso}(k), g_{\rm floor}\}`.
The same ``< target`` / ``< 10\,target`` thresholds apply, with a default
relative target :math:`10^{-3}`. A buffer level is diagonalized automatically so
the highest requested level still has an upper gap; if it is unavailable the
level carries an ``upper_gap_unavailable`` warning.

.. note::

   The observed-gap scope normalizes by an *observed* spectral gap, never by a
   basis-set frequency scale. A basis parameter such as the fluxonium LC
   frequency is useful internally but is not a physical low-energy scale, so it
   is deliberately not used as a reporting denominator.


Choosing a mode
===============

The ``mode`` argument trades cost for confidence; the next section gives the
estimator equations behind each.

``mode='quick'``
    A cheap per-level estimate with **no extra diagonalization**, computed from
    the eigenvectors you already have (the charge finite-tail estimate for charge
    bases, the harmonic-oscillator finite-window estimate for fluxonium). It
    carries ``perturbative`` evidence and never returns an unqualified
    ``converged``: the best status it assigns is ``likely_converged``. Use it for
    rapid feedback while exploring parameters.

``mode='verify'`` (default)
    One refinement diagonalization at a larger cutoff, compared against the
    current one -- an actual measurement of how much the spectrum is still
    moving. Evidence is ``verified_empirical``.

``mode='strict'``
    Two refinement diagonalizations, used to run an asymptoticity test (a
    geometric ratio test, or Richardson extrapolation for finite-difference
    grids) before trusting a tail-extrapolated error estimate. A level that
    passes is ``verified_empirical``; one whose movements are not shrinking is
    reported ``underconverged`` rather than softened to ``marginal``.

::

    quick   = tmon.estimate_convergence(n_levels=5, mode="quick")
    verify  = tmon.estimate_convergence(n_levels=5, mode="verify",
                                        target_abs_GHz=1e-4)
    strict  = tmon.estimate_convergence(n_levels=5, mode="strict",
                                        target_abs_GHz=1e-4)


How each check works
====================

This section gives the estimator used by each mode and truncation channel,
together with its equation. Every estimate is empirical or perturbative; none is
a theorem-level bound.

Refinement estimators (energies)
--------------------------------

**One-step (verify mode).** The estimate is the safety-scaled one-step movement,

.. math::

   \widehat{\mathrm{err}}_{k} = S\, d_{0,k},

reported as ``verified_empirical`` (the safety factor is calibrated so that
:math:`S\,d_{0,k}` bounds the residual tail in the validated regimes).

**Two-step geometric ratio test (strict mode, charge / HO channels).** With both
movements available, the per-level ratio and geometric-tail estimate are

.. math::

   R_k = \frac{d_{1,k}}{d_{0,k}}, \qquad
   \widehat{\mathrm{err}}_{k} = \frac{d_{0,k}}{1 - R_k}\quad (R_k < 1).

A cluster with :math:`R_k < 1` is in the asymptotic regime and the geometric tail
is reported as ``verified_empirical``. If :math:`R_k \ge 1` on a non-negligible
movement the series is not contracting: the level is forced to ``underconverged``
(evidence ``unverified``) rather than ``marginal``, and carries a
``ratio_test_not_asymptotic`` warning.

**Richardson extrapolation (strict mode, finite-difference stencil).** For an FD
grid the discretization error scales as :math:`h^p` with spacing
:math:`h \propto 1/(N-1)` at a fixed box, where :math:`p` is the stencil order
(``settings.STENCIL`` :math:`-\,1`; the default 7-point stencil gives
:math:`p=6`). With :math:`g_i = 1/(N_i-1)^p` the coarse-grid error and the
model-predicted movement ratio are

.. math::

   \widehat{\mathrm{err}}_{k} = \frac{d_{0,k}}{1 - g_1/g_0}, \qquad
   \rho_{\rm expected} = \frac{g_1 - g_2}{g_0 - g_1}.

The level is asymptotic (and the estimate ``verified_empirical``) when the
observed ratio :math:`d_{1,k}/d_{0,k}` matches :math:`\rho_{\rm expected}` to
within a relative tolerance; otherwise it falls back to the one-step bound.

.. note::

   A 5-point stencil cleanly realizes :math:`h^4` across usable grids, giving the
   most reliable Richardson signal. The default 7-point stencil (and the 9-point)
   converge faster in absolute accuracy, but their :math:`h^p` regime saturates
   near the round-off scale, so on coarse grids the asymptoticity test rejects
   and the engine falls back to the conservative one-step bound -- a safe
   outcome.

Cluster-safe matching
---------------------

Near degeneracies, matching levels by index is unreliable. Consecutive levels
whose internal gaps are small compared with the neighboring external gaps are
grouped into a *cluster*, compared as a sorted set, and assigned a common
error estimate plus a ``cluster_index_ambiguity`` warning. The subspace
diagnostic for a cluster spanned by :math:`U_{N_0}`, :math:`U_{N_1}` is the sine
of the largest principal angle,

.. math::

   \sin\Theta = \bigl\| (I - U_{N_0} U_{N_0}^\dagger)\, U_{N_1} \bigr\|_2,

which is robust to eigenvector rotations within the block.

Cheap estimators (quick mode)
-----------------------------

**Charge finite tail (transmon, flux qubit).** The dropped charge states couple
to the kept space only through the boundary, so a second-order (resolvent)
estimate uses the boundary amplitudes :math:`c_{R,k}=\langle n_{\rm cut}|u_k\rangle`,
:math:`c_{L,k}=\langle -n_{\rm cut}|u_k\rangle`,

.. math::

   \widehat{\mathrm{err}}^{\rm ch}_{k}
   = \left| \frac{E_J^2}{4}\Bigl( |c_{R,k}|^2\, G_R + |c_{L,k}|^2\, G_L \Bigr) \right|,
   \qquad G_{R/L} = \bigl[(T^{(d)}_{R/L} - E_{k} I)^{-1}\bigr]_{11},

where :math:`T^{(d)}` is the depth-:math:`d` tridiagonal block of the dropped
tail (diagonal :math:`4E_C(n-n_g)^2`, hopping :math:`-E_J/2`); :math:`d` is grown
until the estimate stabilizes. At :math:`d=1` this reduces to the familiar
boundary-denominator estimate with denominators
:math:`4E_C(n_{\rm cut}+1\mp n_g)^2 - E_{k}`. The estimate is reported as
``perturbative``. It is reliable only when the tail is perturbative: if a tail
eigenvalue lies at or below :math:`E_k` the level is ``unverified``, and if the
boundary probability :math:`|c_{R,k}|^2+|c_{L,k}|^2` is large the level is
``underconverged`` with a ``boundary_probability_large`` warning regardless of
the estimate.

**Harmonic-oscillator finite window (fluxonium).** The cosine is not banded in
the oscillator basis, so the dropped-space residual must use the full kept
vector. For a dropped window :math:`W=\{N,\dots,N+d-1\}`,

.. math::

   (r_W)_m = \sum_{j=0}^{N-1} \langle m|\hat H|j\rangle\, c_{j,k}, \qquad
   \eta^{\rm HO}_{W,k} = \bigl| \langle r_W,\, (H_{WW} - E_k I)^{-1} r_W\rangle \bigr|,

with the kept-to-dropped coupling :math:`\langle m|\hat H|j\rangle = -E_J\langle
m|\cos(\hat\varphi+\varphi_{\rm ext})|j\rangle` taken from the cosine on an
extended Fock basis (the LC term is diagonal and does not couple kept to
dropped). A further dropped band gives the omitted-residual norm
:math:`\rho_{\rm tail} = \sum_{m \ge N+d} |(r_W)_m|^2`; if it is not small
compared with :math:`\|r_W\|^2`, or a window state is near-resonant with
:math:`E_k`, the estimate is flagged unreliable. The result is a ``perturbative``
*lower bound*: verify mode remains authoritative.

Finite-difference grids: two channels
-------------------------------------

A finite-difference coordinate on a box :math:`[-L,L]` with spacing :math:`h` has
**two independent error channels** that require different tests.

* **Finite box** (``FD_box``). A small endpoint amplitude is not a bound on the
  error from the wall at :math:`\pm L`. The cheap diagnostic is the edge-band
  probability over :math:`q=\max\{5,\lceil w_{\rm edge}/h\rceil\}` points at each
  end (with :math:`w_{\rm edge}` a few percent of the window -- at least a few
  stencil half-widths -- and :math:`q` capped at half the grid),

  .. math::

     P_{\rm edge}(k) = \sum_{i=0}^{q-1} |c_{i,k}|^2
                     + \sum_{i=N_{\rm grid}-q}^{N_{\rm grid}-1} |c_{i,k}|^2 .

  A large :math:`P_{\rm edge}` is a reliable warning that the box is too small.
  The box is *verified* by an expanded-box calculation at comparable spacing
  (increase :math:`L`, hold :math:`h`); increasing the number of grid points at
  fixed :math:`L` does not fix a box error.

* **Finite spacing** (``FD_stencil``). At fixed box, stencil error is tested by
  grid refinement and the Richardson estimate above.

For ZeroPi these are exposed as separate refinement axes (``grid_box`` widens the
window at fixed :math:`h`; ``grid_spacing`` adds points at a fixed window),
alongside the ``charge_tail`` of the theta basis.

Multi-coordinate qubits (composite)
-----------------------------------

When several truncation channels contribute, their absolute estimates are
combined by the triangle inequality, and the *sum* (not the maximum) sets the
status:

.. math::

   \widehat{\mathrm{err}}^{\rm total}_{k} \le \sum_c \widehat{\mathrm{err}}^{(c)}_{k}.

The per-level ``truncation_channel`` is then ``composite_coupling``, while
``channel_breakdown_GHz`` retains the per-channel contributions for display.

Transition frequencies
----------------------

Each level verdict also carries ``transition_err_est_GHz``, the triangle-inequality
bound on a transition error,

.. math::

   \widehat{\Delta\omega}_{ij} \le \widehat{\mathrm{err}}_{i} + \widehat{\mathrm{err}}_{j}.


Reading the report
==================

``estimate_convergence`` returns a :class:`.ConvergenceReport`. Printing it (or
calling :meth:`~.ConvergenceReport.summary`) gives a readable rundown; the fields
are also available programmatically:

``aggregate_status``
    The overall verdict, equal to the worst per-level status: ``converged``,
    ``likely_converged``, ``marginal``, ``underconverged``, or ``unverified``.

``per_level`` / :meth:`~.ConvergenceReport.level`
    A list of :class:`.LevelVerdict`, one per requested level;
    ``report.level(k)`` looks one up by level index. A failure of a high-lying
    level never hides the convergence of the lower levels.

``worst_level``
    The index of the level that determined the aggregate status;
    ``report.level(report.worst_level)`` retrieves it.

``channel_breakdown_GHz``
    The per-channel error contributions (in GHz).

``recommendations``
    Channel-specific next steps (which cutoff to grow, whether to enlarge an FD
    box rather than add points, flagged ``boundary_probability_large`` levels).

``clusters``
    Groups of near-degenerate levels, compared as a set rather than by index.

``implementation_audit``
    A record of exactly what was diagnosed: scqubits version, qubit class, basis,
    diagonalization method, cutoff parameters, the requested and buffer level
    counts, and the mode/refinement used.

``derived``
    When derived quantities are requested, a mapping from each name to its own
    :class:`.ConvergenceReport`; ``None`` otherwise.

Each :class:`.LevelVerdict` carries a ``status``, a ``status_scope``
(``absolute`` or ``observed_gap_scale``), an ``abs_err_est_GHz`` estimate, an
optional ``eps_gap_est``, the ``transition_err_est_GHz`` map, a
``truncation_channel`` (``charge_tail``, ``HO_tail``, ``FD_box``, ``FD_stencil``,
or ``composite_coupling``), an ``estimator_method`` (e.g. ``one_step``,
``ratio_test``, ``finite_tail_resolvent``), any ``warnings``, and an ``evidence``
label.


Derived quantities
------------------

By default the report covers the energy spectrum. Pass ``include_derived=True``
together with ``derived_quantities`` to additionally assess any of
``"wavefunctions"``, ``"matrix_elements"``, and ``"coherence"``; each comes back
as its own :class:`.ConvergenceReport` under ``report.derived`` and requires
``mode='verify'`` or ``'strict'`` (a refinement comparison is needed)::

    report = tmon.estimate_convergence(
        n_levels=5, mode="verify", target_abs_GHz=1e-4,
        include_derived=True,
        derived_quantities=["wavefunctions", "matrix_elements", "coherence"],
    )
    print(report.derived["wavefunctions"].aggregate_status)

Eigenvectors and matrix elements can converge more slowly than eigenvalues
(Davis--Kahan: an isolated level's eigenvector angle scales like
:math:`\|r_k\|/\delta_k`, linear in the residual, while the Kato--Temple
eigenvalue error is quadratic). Each derived sub-report stores the dimensionless
change of the quantity in ``eps_gap_est``.

**Wavefunctions** -- the overlap deficit :math:`1 - |\langle\psi_{N_0,k}|
\psi_{N_1,k}\rangle|` for an isolated level, or the cluster subspace angle
:math:`\sin\Theta` above for a near-degenerate block.

**Matrix elements** -- per level, the worst relative change of that level's
matrix-element row and column, maximized over the operators named by
``get_operator_names``. Elements are compared by magnitude, since each
eigenvector's global phase is a gauge choice that can differ between cutoffs.

**Coherence** -- one verdict per noise channel (those from
``effective_noise_channels``, plus aggregate :math:`T_1` and :math:`T_2`). Rates
are compared first (converted to Hz),

.. math::

   \frac{|\Gamma_{N_1} - \Gamma_{N_0}|}{\max\{|\Gamma_{N_1}|,\, \Gamma_{\rm floor}\}},

and a channel whose rate falls below ``CONVERGENCE_RATE_FLOOR_HZ`` carries a
``noise_floor`` warning instead of a lifetime claim.


The evidence ladder
-------------------

Every numerical conclusion is tagged with an ``evidence`` label so that you can
tell a refinement-verified result from a cheap heuristic at a glance. From
strongest to weakest:

``verified_empirical``
    A refinement or cross-check with a ratio/asymptoticity/stability test --
    what ``mode='verify'`` and a successful ``mode='strict'`` ratio test produce.
    This is the strongest label; ``converged`` requires it.

``perturbative``
    A perturbation-theory or resolvent estimate with unverified runtime
    hypotheses -- what ``mode='quick'`` produces for the charge and oscillator
    tails.

``diagnostic``
    A signal of possible trouble, not a measurement of the error -- the
    quick-mode fallback when no cheap estimator is available.

``unverified``
    Inputs unavailable, assumptions failed, or no target supplied.

The guiding principle is conservative: a cheap signal is never silently promoted
to a strong claim. ``converged`` is reserved for results backed by
``verified_empirical`` evidence.


Convergence across a parameter sweep
====================================

A single report certifies one parameter set. A plot such as
``plot_evals_vs_paramvals`` instead sweeps a parameter at a *fixed* cutoff, and
truncation convergence can vary across that range -- fluxonium near half flux,
for example, is far harder to converge than away from it. Use
:meth:`~.ConvergenceCheckable.estimate_convergence_vs_paramvals` to check the
worst case::

    import numpy as np

    flux_vals = np.linspace(0.0, 0.5, 101)
    sweep = fluxonium.estimate_convergence_vs_paramvals(
        "flux", flux_vals, sample=5, n_levels=5, target_abs_GHz=1e-4
    )
    print(sweep)                    # per-point status, worst marked
    print(sweep.worst_param_val())  # the value where the cutoff is least trusted
    worst = sweep.worst_report()    # the full ConvergenceReport there

It runs the per-point check at ``sample`` values spread across the range (always
including both endpoints, the usual worst case; ``sample=None`` checks every
value), restores the swept parameter afterward, and returns a
:class:`.ParamSweepConvergence` holding every per-point report and the worst case.


A complete example
==================

Start with a deliberately small cutoff and let the loop guide you to a converged
result::

    import scqubits as scq

    tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=6, truncated_dim=6)

    report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report.aggregate_status)     # 'underconverged'
    print(report.recommendations[0])   # suggests increasing ncut

    tmon.ncut = 31                     # follow the recommendation
    report = tmon.estimate_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report.aggregate_status)     # 'converged'

For a fast check while scanning parameters, drop the extra diagonalization::

    report = tmon.estimate_convergence(n_levels=5, mode="quick", target_abs_GHz=1e-6)
    print(report.aggregate_status)     # 'likely_converged', 'marginal', ...

For a publication-grade check, demand the asymptoticity test::

    report = tmon.estimate_convergence(
        n_levels=5, mode="strict", target_abs_GHz=1e-6
    )
    print(report.per_level[0].evidence)   # 'verified_empirical'


Settings
========

The defaults that control the diagnostics -- refinement step, cluster threshold,
safety factor :math:`S`, gap floor, rate floor, and default mode -- live in
:mod:`scqubits.settings` under the ``CONVERGENCE_*`` names and can be adjusted
globally; see the :ref:`guide-settings` section.
