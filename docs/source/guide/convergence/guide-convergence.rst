.. scqubits
   Copyright (C) 2019, Jens Koch & Peter Groszkowski

.. _guide_convergence:

**************************
Convergence Diagnostics
**************************

Every qubit in scqubits is modeled by a Hamiltonian that, in general, acts on an
infinite-dimensional Hilbert space; scqubits represents it numerically as a finite
matrix by truncating the basis it is expressed in. The transmon, for example, is
represented in a finite charge basis controlled by ``ncut``; fluxonium in a
harmonic-oscillator basis controlled by ``cutoff``; the grid-based qubits
discretize a flux coordinate on a finite box. The numbers scqubits returns --
energies, wavefunctions, matrix elements, coherence times -- are only as accurate
as that truncated representation allows. If the cutoff is too small, results are
silently wrong; if it is far too large, calculations are needlessly slow.

The convergence-diagnostics framework answers a single practical question: *for
the cutoff I have chosen, is there any reason to distrust the result, and what
should I do if there is?*

**A convergence test can only ever dismiss convergence.** This is the central
idea, and it shapes every verdict the framework returns. A test refines the
cutoff and looks for the spectrum still moving, for an eigenstate spilling over
the basis boundary, for a refinement series that refuses to contract. When it
finds one of these, it has *caught a clearly-wrong result* -- a strong, useful,
negative statement. When it finds none of them, all it can honestly say is *"I
failed to dismiss this"*; that is never a proof that the true error is small. A
more rigorous mode simply applies sharper dismissal tests, so a result that
survives it has survived more. The most actionable signal the framework can give
you is therefore a ``distrust`` verdict: it means a check actively caught a
result you should not rely on at the current cutoff.

.. note::

   Convergence diagnostics are available for :class:`.Transmon`,
   :class:`.TunableTransmon`, :class:`.Fluxonium`, :class:`.FluxQubit`,
   :class:`.ZeroPi`, :class:`.FullZeroPi`, and :class:`.Cos2PhiQubit`, covering the
   energy spectrum and -- on request -- the wavefunctions, matrix elements, and
   coherence rates. Coupled :class:`.HilbertSpace` systems are supported as well
   (see :ref:`guide_convergence_composite`), as are custom :class:`.Circuit`
   instances, including hierarchically diagonalized ones (see
   :ref:`guide_convergence_circuit`), and precomputed :class:`.ParameterSweep`
   grids (see :ref:`guide_convergence_paramvals`). Calling the top-level
   ``scq.check_convergence(obj)`` on anything else raises :class:`TypeError`.


Quick start
===========

The shortest path to "is my qubit converged?" is the :func:`scqubits.csc`
convenience (**c**\ onvergence **s**\ anity **c**\ heck), which picks sensible
defaults and returns a pretty-printable verdict with no further input::

   >>> import scqubits as scq
   >>> q = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=31, truncated_dim=4)
   >>> print(scq.csc(q))

prints a header, a one-line ``VERDICT:``, a plain-English explanation, an
optional next-step tip, and the full underlying
:class:`~scqubits.core.convergence_report.ConvergenceReport`. If the verdict
is anything but a clean pass, the recommendations name *which* cutoff to grow.

**Calling** ``csc`` **on the same object twice escalates the check from**
``mode="moderate"`` **to** ``mode="strict"`` -- if you doubt the first
answer, just ask again. The default precision target (``1e-4`` GHz, i.e.
0.1 MHz) and the auto-chosen ``n_levels`` cap are tunable as
``settings.CSC_DEFAULT_TARGET_ABS_GHZ`` and
``settings.CSC_DEFAULT_NLEVELS_CAP``; see :ref:`settings-params` for the full
list of scqubits settings.

``csc`` is a zero-input wrapper around the full
:meth:`~scqubits.core.convergence.ConvergenceCheckable.check_convergence`
API documented below; use the full API when you need to control ``n_levels``,
``target_abs_GHz``, ``mode``, ``scope``, derived quantities, or
parameter-sweep checks.


The verdicts
============

Every level is assigned one of five verdicts, ordered from best (left) to worst
(right)::

    likely_converged  >  maybe_converged  >  marginal  >  unverified  >  distrust

``likely_converged``
    Passed the ``strict`` two-step ratio/asymptoticity test -- the strongest
    statement the framework makes, and still not an outright guarantee.

``maybe_converged``
    Passed the ``moderate`` one-step refinement check: a larger cutoff was tried
    and the spectrum did not move appreciably.

``marginal``
    The estimated error sits close to the requested target -- a borderline
    result that may or may not meet your needs.

``unverified``
    Neither dismissed nor verified: a ``cheap`` pass, or a level that could not
    be assessed (for example, no target was supplied).

``distrust``
    A test *actively dismissed* convergence. The result is not trustworthy at
    this cutoff. This includes the strict-mode ratio test failing
    (:math:`R \ge 1`), a kept eigenstate reaching the basis boundary, and a
    charge-basis energy that *rises* under refinement (a variational-monotonicity
    violation -- see :ref:`guide_convergence_monotonicity`).

Read these the right way round. ``likely_converged`` and ``maybe_converged``
both mean *"we failed to dismiss this level"*, with the former having survived a
harder test; neither is a certificate. ``distrust`` is the one verdict that
states a fact with confidence -- we caught a result you should not use as is.

The verdict name carries the confidence directly. To see *why* a level earned
its verdict -- which falsification tests ran and how they fared -- read its
structured ``checks`` record together with the ``estimator_method`` and any
``warnings`` (see :ref:`guide_convergence_checks`); there is no separate
evidence-tier field.


The basic workflow
==================

Reaching a trustworthy result is a short loop: estimate, read the verdict, and --
if necessary -- increase the cutoff and repeat.

1. **Build the qubit** at an initial cutoff::

       import scqubits as scq

       tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=31, truncated_dim=6)

2. **Check convergence** for the levels you care about. You either call the
   method on the qubit or use the top-level shim; they are equivalent::

       report = tmon.check_convergence(n_levels=5, target_abs_GHz=1e-4)
       # identical to:
       report = scq.check_convergence(tmon, n_levels=5, target_abs_GHz=1e-4)

3. **Read the verdict.** The report prints itself::

       print(report)                  # human-readable summary of every level
       print(report.aggregate_status) # e.g. 'maybe_converged'
       worst = report.level(report.worst_level)   # the driving level's verdict

   For the ``ncut=31`` transmon above, ``print(report)`` produces::

       aggregate: maybe_converged   (worst: level 0)

         lvl   status            channel       err (GHz)   via
           0   maybe_converged   charge_tail    7.11e-15   one_step
           1   maybe_converged   charge_tail    1.85e-13   one_step
           2   maybe_converged   charge_tail    2.47e-13   one_step
           3   maybe_converged   charge_tail    4.97e-14   one_step
           4   maybe_converged   charge_tail    4.44e-14   one_step

         error by channel (GHz): charge_tail=2.47e-13

   Every estimated error sits far below the ``1e-4`` GHz target and the default
   moderate refinement found no movement, so each level is ``maybe_converged``:
   ``ncut=31`` was not dismissed for these parameters. (Exact digits depend on
   the platform and diagonalization backend; a passing level prints no per-check
   line -- those appear only under a dismissed or borderline level.)

4. **Act on the recommendation.** When a level is dismissed, the printed report
   ends with a plain-language fix for each problem channel. For an under-resolved
   transmon it reads::

       recommendation: charge-basis tail dominates: increase ncut from 6 to at least 10 (charge cutoff) and re-run

   The same lines are also available as a list of strings in
   ``report.recommendations``. Apply the suggested change and repeat from step 2;
   a typical loop settles in one or two iterations.

The default mode (``mode='moderate'``) performs one extra diagonalization at a
larger cutoff and compares the two spectra level by level. It is the recommended
setting: cheap enough for routine use, and it actually tries a larger cutoff
rather than reasoning about one.


Notation
========

Let :math:`N` be the cutoff parameter and :math:`E_{k,N}` the :math:`k`-th
computed eigenvalue. The (unknown) true error of a level is
:math:`\Delta E_{k,N} = |E_{k,N} - E_k|`; every diagnostic reports an *estimate*
:math:`\widehat{\mathrm{err}}_{k,N} \approx \Delta E_{k,N}`, never the true error
itself. A refinement bumps the cutoff to :math:`N_1 > N_0` (and, in strict mode,
a second :math:`N_2 > N_1`); the per-level refinement differences are

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
:math:`\widehat{\mathrm{err}}_{k}` the per-level estimate, before the mode
ceiling is applied (see below), the verdict is

.. math::

   \begin{aligned}
   \widehat{\mathrm{err}}_{k} < \Delta_\star &\;\Rightarrow\; \texttt{(pass)}, \\
   \Delta_\star \le \widehat{\mathrm{err}}_{k} < 10\,\Delta_\star &\;\Rightarrow\; \texttt{marginal}, \\
   \widehat{\mathrm{err}}_{k} \ge 10\,\Delta_\star &\;\Rightarrow\; \texttt{distrust}.
   \end{aligned}

A pass is then capped at the best verdict the mode is entitled to claim --
``maybe_converged`` for moderate, ``likely_converged`` for strict (see
:ref:`guide_convergence_modes`). A ``marginal`` or ``distrust`` dismissal is
never softened or raised.

If you omit ``target_abs_GHz``, scqubits still computes and reports the per-level
estimate ``abs_err_est_GHz``, but it does not convert that into a pass/fail
verdict -- the verdict is ``unverified`` and a recommendation reminds you to
supply a target.

If you care about error *relative to the qubit's own spectrum* rather than an
absolute energy, choose the observed-gap scope::

    report = tmon.check_convergence(
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
relative target :math:`10^{-3}`. One eigenvalue beyond the requested levels is
computed automatically (in the same diagonalization) so the highest requested
level still has an upper neighbor for the gap; if it is unavailable the level
carries an ``upper_gap_unavailable`` warning.

.. note::

   The observed-gap scope normalizes by an *observed* spectral gap, never by a
   basis-set frequency scale. A basis parameter such as the fluxonium LC
   frequency is useful internally but is not a physical low-energy scale, so it
   is deliberately not used as a reporting denominator.


.. _guide_convergence_modes:

Choosing a mode
===============

The ``mode`` argument trades cost for the rigor of the dismissal test. Because a
test can only dismiss convergence -- never prove it -- each mode also **caps** the
best verdict it can return: a stronger claim demands more work. The next section
gives the estimator equations behind each.

``mode='cheap'``
    Cheap per-level diagnostics with **no extra diagonalization**, computed from
    the eigenvectors you already have (the charge finite-tail estimate for charge
    bases, the harmonic-oscillator finite-window estimate for fluxonium). It can
    still *dismiss* a level -- a kept state reaching the basis boundary is caught
    here -- but a level it fails to dismiss earns at best ``unverified``: cheap
    mode makes no verification claim. Use it for rapid feedback while exploring
    parameters.

``mode='moderate'`` (default)
    One refinement diagonalization at a larger cutoff, compared against the
    current one -- an actual measurement of how much the spectrum is still
    moving. A level it fails to dismiss caps at ``maybe_converged``.

``mode='strict'``
    Two refinement diagonalizations, used to run an asymptoticity test (a
    geometric ratio test, or Richardson extrapolation for finite-difference
    grids) before trusting a tail-extrapolated error estimate. A level that
    passes caps at ``likely_converged`` -- the strongest verdict available; a
    level whose refinement differences are not shrinking (:math:`R \ge 1`) is
    dismissed to ``distrust`` rather than softened to ``marginal``.

::

    cheap    = tmon.check_convergence(n_levels=5, mode="cheap")
    moderate = tmon.check_convergence(n_levels=5, mode="moderate",
                                         target_abs_GHz=1e-4)
    strict   = tmon.check_convergence(n_levels=5, mode="strict",
                                         target_abs_GHz=1e-4)


How each check works
====================

This section gives the estimator used by each mode and truncation channel,
together with its equation. Every estimate is empirical or perturbative; none is
a theorem-level bound, and a passing estimate is always a failure to dismiss
rather than a guarantee.

Refinement estimators (energies)
--------------------------------

**One-step (moderate mode).** The estimate is the safety-scaled one-step
refinement difference,

.. math::

   \widehat{\mathrm{err}}_{k} = S\, d_{0,k},

a direct measurement of how the spectrum responds to a larger cutoff, scaled by
the conservative safety factor :math:`S`. This is an observed refinement
difference, not a proof that the sequence has reached its asymptotic regime --
for that, use ``mode='strict'``, which adds a second refinement and tests whether
the refinement differences are contracting.

**Two-step geometric ratio test (strict mode, charge / HO channels).** With both
refinement differences available, the per-level ratio and geometric-tail estimate are

.. math::

   R_k = \frac{d_{1,k}}{d_{0,k}}, \qquad
   \widehat{\mathrm{err}}_{k} = \frac{S\,d_{0,k}}{1 - R_k}\quad (R_k < 1).

A cluster with :math:`R_k < 1` is in the asymptotic regime and the geometric tail
is reported (capped at ``likely_converged`` for a passing level). If
:math:`R_k \ge 1` on a non-negligible refinement difference the series is not
contracting: the level is dismissed to ``distrust`` rather than ``marginal``, and
carries a ``ratio_test_not_asymptotic`` warning.

**Richardson extrapolation (strict mode, finite-difference stencil).** For an FD
grid the discretization error scales as :math:`h^p` with spacing
:math:`h \propto 1/(N-1)` at a fixed box, where :math:`p` is the stencil order
(``settings.STENCIL`` :math:`-\,1`; the default 7-point stencil gives
:math:`p=6`). With :math:`g_i = 1/(N_i-1)^p` the coarse-grid error and the
model-predicted refinement-difference ratio are

.. math::

   \widehat{\mathrm{err}}_{k} = \frac{d_{0,k}}{1 - g_1/g_0}, \qquad
   \rho_{\rm expected} = \frac{g_1 - g_2}{g_0 - g_1}.

The level is asymptotic when the observed ratio :math:`d_{1,k}/d_{0,k}` matches
:math:`\rho_{\rm expected}` to within a relative tolerance; otherwise it falls
back to the one-step estimate.

.. note::

   How well the :math:`h^p` regime is realized is parameter-, box-, and
   grid-dependent. A lower-order stencil (e.g. 5-point, :math:`p=4`) tends to
   realize its order over a wider usable grid range, whereas the higher-order
   default reaches the round-off floor sooner. Where the regime is not realized
   the asymptoticity test rejects and the engine falls back to the one-step
   estimate -- a safe outcome (no false convergence).

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

.. _guide_convergence_monotonicity:

Variational monotonicity
------------------------

For an *exactly nested* basis truncation, enlarging the basis cannot raise an
ordered eigenvalue (the Rayleigh--Ritz min--max theorem):
:math:`E_{k,N_1} \le E_{k,N_0}` for :math:`N_1 > N_0`. In scqubits this holds for
the **charge basis** -- growing ``ncut`` borders the kept block with additional
charge states, so the smaller Hamiltonian is an exact principal submatrix of the
larger. Every refinement therefore carries a near-free falsification test: a
charge-basis energy that *rises* by more than the eigensolver noise floor
violates the variational bound, and the level is dismissed to ``distrust`` in any
mode -- such a rise signals an operator-construction or backend problem rather
than mere truncation. The check is silent on healthy results and is restricted to
the charge basis: harmonic-oscillator bases build the potential from matrix
functions of the *truncated* quadratures (so the truncation is not nested), and
finite-difference grids are non-variational, so a rise there is legitimate and
those channels are excluded.

Cheap estimators (cheap mode)
-----------------------------

**Charge finite tail (Transmon and TunableTransmon).** For the transmon's
nearest-neighbor (single-cosine) Josephson Hamiltonian -- tridiagonal in the
charge basis -- the dropped charge states couple to the kept space only through
the two boundary charges, so a second-order (resolvent) estimate uses the boundary
amplitudes :math:`c_{R,k}=\langle n_{\rm cut}|u_k\rangle`,
:math:`c_{L,k}=\langle -n_{\rm cut}|u_k\rangle`,

.. math::

   \widehat{\mathrm{err}}^{\rm ch}_{k}
   = \left| \frac{E_J^2}{4}\Bigl( |c_{R,k}|^2\, G_R + |c_{L,k}|^2\, G_L \Bigr) \right|,
   \qquad G_{R/L} = \bigl[(T^{(d)}_{R/L} - E_{k} I)^{-1}\bigr]_{11},

where :math:`T^{(d)}` is the depth-:math:`d` tridiagonal block of the dropped
tail (diagonal :math:`4E_C(n-n_g)^2`, hopping :math:`-E_J/2`); :math:`d` is grown
until the estimate stabilizes. At :math:`d=1` this reduces to the familiar
boundary-denominator estimate with denominators
:math:`4E_C(n_{\rm cut}+1\mp n_g)^2 - E_{k}`. It is reliable only when the tail
is perturbative: if a tail eigenvalue lies at or below :math:`E_k` the level is
``unverified``, and if the boundary probability :math:`|c_{R,k}|^2+|c_{L,k}|^2`
is large the level is dismissed to ``distrust`` with a
``boundary_probability_large`` warning regardless of the estimate. A
multi-dimensional charge basis (such as :class:`.FluxQubit`, which has several
boundary faces and a coupling structure not captured by the 1D formula) does not
use this estimator; its cheap mode falls back to a boundary diagnostic and it is
moderate-recommended.

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
compared with :math:`\|r_W\|^2`, or a window eigenvalue lies at or below
:math:`E_k`, the estimate is flagged unreliable. The result is a perturbative
estimate with an omitted-tail diagnostic, **not a bound** -- a finite dropped
window omits both the far-dropped residual and the Schur self-energy of the rest
of the dropped space, so it is not sign-definite. If :math:`\rho_{\rm tail}` is
not small the level is reported ``unverified`` in cheap mode; moderate mode
remains authoritative. The dismissal-triggering boundary probability is a separate
quantity -- the occupation of the top few kept Fock states, the oscillator analog
of the charge-edge probability -- whose large value raises
``boundary_probability_large`` independently of the window estimate.

Finite-difference grids: two channels
-------------------------------------

A discretized (finite-difference) extended variable on a box :math:`[-L,L]` with
spacing :math:`h` has **two independent truncation channels** that require
different tests, and a check must verify both.

* **Finite box** (``FD_box``). A small endpoint amplitude is not a bound on the
  error from the wall at :math:`\pm L`. The cheap diagnostic is the edge-band
  probability over :math:`q=\max\{5,\lceil w_{\rm edge}/h\rceil\}` points at each
  end (with :math:`w_{\rm edge}` a few percent of the window -- at least a few
  stencil half-widths -- and :math:`q` capped at half the grid),

  .. math::

     P_{\rm edge}(k) = \sum_{i=0}^{q-1} |c_{i,k}|^2
                     + \sum_{i=N_{\rm grid}-q}^{N_{\rm grid}-1} |c_{i,k}|^2 .

  A large :math:`P_{\rm edge}` is a reliable warning that the box is too small.
  The box is verified by an expanded-box calculation at comparable spacing
  (increase :math:`L`, hold :math:`h`); adding grid points at fixed :math:`L`
  cannot fix a box error.

* **Finite spacing** (``FD_stencil``). At fixed box, stencil error is tested by
  grid refinement and the Richardson estimate above.

For ZeroPi these are exposed as separate refinement axes (``grid_box`` widens the
window at fixed :math:`h`; ``grid_spacing`` adds points at a fixed window),
alongside the ``charge_tail`` of the theta basis.

Multi-coordinate qubits (composite)
-----------------------------------

When several truncation channels contribute, their absolute estimates are
combined by the triangle inequality, and the *sum* (not the maximum) sets the
verdict:

.. math::

   \widehat{\mathrm{err}}^{\rm total}_{k} \le \sum_c \widehat{\mathrm{err}}^{(c)}_{k}.

The per-level ``truncation_channel`` is then the dominant physical channel, while
``channel_breakdown_GHz`` retains the per-channel contributions for display.

Transition frequencies
----------------------

Each level verdict also carries ``transition_err_est_GHz``, the triangle-inequality
bound on a transition error,

.. math::

   \widehat{\Delta\omega}_{ij} \le \widehat{\mathrm{err}}_{i} + \widehat{\mathrm{err}}_{j}.


Reading the report
==================

``check_convergence`` returns a :class:`.ConvergenceReport`. Printing it (or
calling :meth:`~.ConvergenceReport.summary`) gives a readable rundown; the fields
are also available programmatically:

``aggregate_status``
    The overall verdict, equal to the worst per-level verdict: one of
    ``likely_converged``, ``maybe_converged``, ``marginal``, ``unverified``, or
    ``distrust``.

``per_level`` / :meth:`~.ConvergenceReport.level`
    A list of :class:`.LevelVerdict`, one per requested level;
    ``report.level(k)`` looks one up by level index. A dismissed high-lying
    level never hides the standing of the lower levels.

``worst_level``
    The index of the level that determined the aggregate verdict;
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

Each :class:`.LevelVerdict` carries a ``status`` (the verdict), a ``status_scope``
(``absolute`` or ``observed_gap_scale``), an ``abs_err_est_GHz`` estimate, an
optional ``eps_gap_est``, the ``transition_err_est_GHz`` map, a
``truncation_channel`` (``charge_tail``, ``HO_tail``, ``FD_box``, ``FD_stencil``,
or ``composite_coupling``), an ``estimator_method`` (e.g. ``one_step``,
``ratio_test``, ``finite_tail_resolvent``), any ``warnings``, and a structured
``checks`` record (below). The verdict name itself records the confidence --
there is no separate evidence-tier field.


.. _guide_convergence_checks:

Which checks ran: the per-level ``checks`` record
-------------------------------------------------

To make the verdict auditable, each :class:`.LevelVerdict` carries a ``checks``
tuple of :class:`.CheckOutcome` (``name``, ``status``, ``detail``) recording the
falsification tests that applied to the level and how each fared. The status of a
check is ``pass`` (it ran and did not dismiss the level), ``fail`` (it ran and
dismissed the level), or ``not_applicable`` (it does not apply in the chosen mode
or for this channel). The tests recorded are:

* ``asymptoticity`` -- the ``strict`` two-step ratio / Richardson test (recorded
  ``not_applicable`` outside ``strict`` mode, or when the refinement sits at the
  eigensolver noise floor);
* ``boundary`` -- the kept-state amplitude at the basis boundary, where a
  boundary diagnostic exists (``detail`` reports the edge probability);
* ``monotonicity`` -- the charge-basis variational check (present only for a
  charge axis);
* ``perturbative_tail`` -- the reliability of the ``cheap``-mode tail estimator.

For example, the printed report shows the per-check line under each level::

    level 1: distrust   channel=charge_tail   abs_err=1.65e-04  via ratio_test
        checks: asymptoticity=pass  boundary=pass(P_edge=5.4e-05)  monotonicity=pass

and ``report.level(1).checks`` exposes the same record programmatically.

The ``checks`` are the *falsification tests*; they are distinct from the
estimate-vs-target grading. A level can therefore be ``distrust`` with **every
check passing** -- this means no test caught a structural problem, but the
estimated error still exceeded ``target_abs_GHz`` (or ``target_gap_rel``). In
that case the fix is simply a larger cutoff; ``abs_err_est_GHz`` and the target
tell you how far off you are.


Derived quantities
------------------

By default the report covers the energy spectrum. Pass ``include_derived=True``
together with ``derived_quantities`` to additionally assess any of
``"wavefunctions"``, ``"matrix_elements"``, and ``"coherence"``; each comes back
as its own :class:`.ConvergenceReport` under ``report.derived`` and requires
``mode='moderate'`` or ``'strict'`` (a refinement comparison is needed)::

    report = tmon.check_convergence(
        n_levels=5, mode="moderate", target_abs_GHz=1e-4,
        include_derived=True,
        derived_quantities=["wavefunctions", "matrix_elements", "coherence"],
    )
    print(report.derived["wavefunctions"].aggregate_status)

Eigenvectors and matrix elements generally converge no faster than -- and often
slower than -- eigenvalues: for an isolated level the eigenvector rotation scales
like :math:`\|r_k\|/\delta_k` (Davis--Kahan), linear in the residual, whereas the
eigenvalue error of a Ritz pair can scale like :math:`\|r_k\|^2/\delta_k`
(Kato--Temple) under an isolating-gap assumption. scqubits does not compute these
bounds; it measures the refinement change of each quantity directly. Each derived
sub-report stores the dimensionless
change of the quantity in ``rel_change_est``.

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


.. _guide_convergence_paramvals:

Convergence across a parameter sweep
====================================

A single report covers one parameter set. A plot such as
``plot_evals_vs_paramvals`` instead sweeps a parameter at a *fixed* cutoff, and
truncation convergence can vary across that range -- a cutoff that is comfortable
at one flux value can be marginal at another. Use
:meth:`~.ConvergenceCheckable.check_convergence_vs_paramvals` to check the
worst case::

    import numpy as np

    fluxonium = scq.Fluxonium(EJ=10.0, EC=5.0, EL=1.0, flux=0.5, cutoff=35)
    flux_vals = np.linspace(0.0, 0.5, 101)
    sweep = fluxonium.check_convergence_vs_paramvals(
        "flux", flux_vals, sample=5, n_levels=5, target_abs_GHz=1e-4
    )
    print(sweep)                    # per-point verdict, worst marked
    print(sweep.worst_param_val())  # the value where the cutoff is least trusted
    worst = sweep.worst_report()    # the full ConvergenceReport there

Here ``cutoff=35`` is comfortable near zero flux but degrades as the flux
approaches the half-flux point, so ``print(sweep)`` shows a verdict that varies
across the range::

    convergence across sweep of (flux) (5 points): worst = marginal at flux=0.375
      flux=0: maybe_converged
      flux=0.125: maybe_converged
      flux=0.25: maybe_converged
      flux=0.375: marginal  <-- worst
      flux=0.5: marginal

``sweep.worst_param_val()`` then returns ``0.375`` and ``sweep.worst_report()``
hands back the full :class:`.ConvergenceReport` at that point for a closer look.

It runs the per-point check at ``sample`` values spread across the range (always
including both endpoints, the usual worst case; ``sample=None`` checks every
value), restores the swept parameter afterward, and returns a
:class:`.ParameterSweepConvergence` holding every per-point report and the worst case.

For a precomputed :class:`.ParameterSweep` -- which sweeps a coupled
:class:`.HilbertSpace` over an N-dimensional grid through an
``update_hilbertspace`` callback -- call
:meth:`~.ParameterSweep.check_convergence` instead. It applies the callback at
sampled grid points (the grid corners first, then evenly-spread interior points up
to ``sample``; ``sample=None`` checks every point), runs the composite
:meth:`~.HilbertSpace.check_convergence` at each, restores the sweep, and
returns a :class:`.ParameterSweepConvergence`::

    import numpy as np

    qbt = scq.TunableTransmon(
        EJmax=30.0, EC=0.3, d=0.1, flux=0.0, ng=0.0, ncut=31, truncated_dim=5
    )
    osc = scq.Oscillator(E_osc=5.0, truncated_dim=5)
    hs = scq.HilbertSpace([qbt, osc])
    hs.add_interaction(g=0.3, op1=qbt.n_operator, op2=osc.creation_operator,
                       add_hc=True)

    def update_hilbertspace(flux):
        qbt.flux = flux

    sweep = scq.ParameterSweep(
        hs, {"flux": np.linspace(0.0, 0.5, 21)}, update_hilbertspace
    )
    result = sweep.check_convergence(
        n_levels=4, mode="moderate", target_abs_GHz=1e-4
    )
    print(result)

::

    convergence across sweep of (flux) (8 points): worst = marginal at flux=0.375
      flux=0: maybe_converged
      flux=0.5: maybe_converged
      flux=0.25: maybe_converged
      flux=0.175: maybe_converged
      flux=0.325: maybe_converged
      flux=0.125: maybe_converged
      flux=0.375: marginal  <-- worst
      flux=0.1: maybe_converged

Each point is a parameter-name-to-value mapping, so multi-parameter sweeps are
reported by their full coordinates; ``result.worst_point()`` and
``result.worst_report()`` give the least-trustworthy grid point and its full
report. Unlike the single-object helper above, this honors the sweep's
``update_hilbertspace`` callback (which may set several coupled parameters at once)
and handles grids over more than one parameter.


A complete example
==================

Start with a deliberately small cutoff and let the loop guide you to a
trustworthy result::

    import scqubits as scq

    tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=6, truncated_dim=6)

    report = tmon.check_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report)                      # the full diagnostic

At ``ncut=6`` the moderate refinement catches the offending levels and spells out
the fix::

    aggregate: distrust   (worst: level 1)

      lvl   status     channel       err (GHz)   via
        0   marginal   charge_tail    8.90e-06   one_step
          checks 0: asymptoticity=n/a(strict mode only)  boundary=pass(P_edge=3.2e-06)  monotonicity=pass
        1   distrust   charge_tail    1.65e-04   one_step
          checks 1: asymptoticity=n/a(strict mode only)  boundary=pass(P_edge=5.4e-05)  monotonicity=pass
        2   distrust   charge_tail    1.43e-03   one_step
          checks 2: asymptoticity=n/a(strict mode only)  boundary=pass(P_edge=0.00042)  monotonicity=pass
        3   distrust   charge_tail    7.78e-03   one_step   [boundary_probability_large]
          checks 3: asymptoticity=n/a(strict mode only)  boundary=fail(P_edge=0.002)  monotonicity=pass
        4   distrust   charge_tail    2.92e-02   one_step   [boundary_probability_large]
          checks 4: asymptoticity=n/a(strict mode only)  boundary=fail(P_edge=0.0068)  monotonicity=pass

    error by channel (GHz): charge_tail=2.92e-02
    -> charge-basis tail dominates: increase ncut from 6 to at least 10 (charge cutoff) and re-run
    -> levels [3, 4] carry the 'boundary_probability_large' warning: the kept state reaches the basis boundary, so the dropped tail is non-perturbative -- increase the cutoff aggressively

The lowest level is only borderline (``marginal``); the higher levels reach the
basis boundary and are badly truncated, so they are dismissed to ``distrust``.
This is exactly the signal you want -- the framework caught a clearly-wrong
result. Follow the recommendation and re-run::

    tmon.ncut = 31                     # follow the recommendation
    report = tmon.check_convergence(n_levels=5, target_abs_GHz=1e-6)
    print(report.aggregate_status)

The aggregate verdict is now::

    maybe_converged

Every level passes the moderate one-step check against the ``1e-6`` GHz target.
Note the verdict is ``maybe_converged``, not an unqualified guarantee: the
moderate refinement found no movement, which is the most this single check can
claim.

For a fast scan while exploring parameters, drop the extra diagonalization::

    report = tmon.check_convergence(n_levels=5, mode="cheap", target_abs_GHz=1e-6)
    print(report.aggregate_status)

which prints::

    unverified

Cheap mode skips the refinement diagonalization, so a level it does not dismiss
earns only ``unverified`` -- it can flag a clearly-wrong result, but it never
makes a verification claim.

For the strongest available check, demand the asymptoticity test::

    report = tmon.check_convergence(
        n_levels=5, mode="strict", target_abs_GHz=1e-6
    )
    print(report.level(report.worst_level).status)

which prints::

    likely_converged

The refinement series contracts and passes the ratio test, so the worst level
reaches ``likely_converged`` -- the strongest verdict the framework makes, and
still a failure to dismiss rather than a proof.


.. _guide_convergence_composite:

Coupled subsystems (HilbertSpace)
=================================

A :class:`.HilbertSpace` truncates in **two layers**, and
``hs.check_convergence(...)`` checks both:

* **Layer 1 -- subsystem-internal.** Each subsystem carries its own basis cutoff
  (``ncut``, ``cutoff``, a grid). Every capable subsystem is checked with its own
  :meth:`~.ConvergenceCheckable.check_convergence` -- at ``truncated_dim`` plus
  the refinement reach, so the extra levels a composite refinement pulls in are
  themselves verified -- and the per-subsystem report is attached under
  ``report.derived["subsystem:<id>"]``. Oscillators have no internal cutoff and
  are skipped. Pass ``assume_subsystems_converged=True`` to skip this layer when
  subsystem convergence has been established separately.

* **Layer 2 -- composite truncation.** Each subsystem's ``truncated_dim`` sets how
  many of its levels enter the product space. This is verified by refining one
  ``truncated_dim`` at a time, re-diagonalizing the *whole* composite, and
  comparing cluster-matched spectra -- a single composite refinement that counts
  subsystem and coupling leakage exactly once, rather than double-counting a
  per-subsystem leakage plus a separate coupling term. The channel is
  ``composite_coupling`` and the dominant subsystem is the one to grow.

The ``aggregate_status`` is the worst of the composite verdict and every
subsystem verdict: the composite cannot be more converged than its parts.

::

    import scqubits as scq

    tmon = scq.Transmon(EJ=20.0, EC=0.3, ng=0.0, ncut=31, truncated_dim=3)
    osc = scq.Oscillator(E_osc=5.0, truncated_dim=3)
    hs = scq.HilbertSpace([tmon, osc])
    hs.add_interaction(
        g=0.6, op1=tmon.n_operator, op2=osc.creation_operator, add_hc=True
    )

    report = hs.check_convergence(n_levels=3, mode="moderate", target_abs_GHz=1e-5)
    print(report)

With the resonator truncated to only three levels the composite is dismissed. The
report names the subsystem to grow, flags the near-resonance, and attaches the
(undismissed) subsystem report underneath::

    aggregate: distrust   (worst: level 0)

      lvl   status     channel              err (GHz)   via
        0   distrust   composite_coupling    1.14e-04   one_step
          checks 0: asymptoticity=n/a(strict mode only)
        1   distrust   composite_coupling    4.86e-03   one_step
          checks 1: asymptoticity=n/a(strict mode only)
        2   distrust   composite_coupling    3.17e-03   one_step
          checks 2: asymptoticity=n/a(strict mode only)

      error by channel (GHz): composite_coupling=6.43e-03
      -> composite truncation dominates: increase truncated_dim of 'Oscillator_1' from 3 to at least 5 and re-run (it sets how many of that subsystem's levels enter the product space)
      -> hybridization screen: near-resonant coupling (eta ~= 1.1) between bare product states of 'Transmon_1' and 'Oscillator_1'; product-state labels are unreliable -- rely on cluster-safe matching and full composite refinement
      derived [subsystem:Transmon_1]:
        aggregate: maybe_converged   (worst: level 0)

          lvl   status            channel       err (GHz)   via
            0   maybe_converged   charge_tail    7.11e-15   one_step
            1   maybe_converged   charge_tail    1.85e-13   one_step
            2   maybe_converged   charge_tail    2.47e-13   one_step
            3   maybe_converged   charge_tail    4.97e-14   one_step
            4   maybe_converged   charge_tail    4.44e-14   one_step

          error by channel (GHz): charge_tail=2.47e-13

Raising the resonator (and transmon) ``truncated_dim`` -- here to 8 -- clears the
dismissal.

**Hybridization screen.** When subsystems are coupled near resonance, the bare
product-state labels :math:`|a,b\rangle` mix strongly. For each two-body
interaction :math:`g\,A\otimes B` the report computes a dimensionless
hybridization parameter

.. math::

   \eta_{ab\to a'b'} = \frac{|g|\,|\langle a'|A|a\rangle|\,|\langle b'|B|b\rangle|}
        {\max\{|(E_a+E_b)-(E_{a'}+E_{b'})|,\ g_{\rm floor}\}},

and warns when it is large (as above). A large :math:`\eta` means the product
labels are unreliable, so levels are matched as clusters rather than by index; it
is a labeling diagnostic, **not** a truncation-error estimate, and does not by
itself set ``distrust``.

**Modes.** ``moderate`` and ``strict`` perform the full composite refinement and
are authoritative. ``cheap`` skips the composite re-diagonalization: it runs the
hybridization screen and each subsystem's own cheap check, and reports the
composite truncation as moderate-recommended (never a verification claim).

**FullZeroPi.** The hierarchical :class:`.FullZeroPi` -- an interior
:class:`.ZeroPi` coupled to a zeta oscillator -- is checked the same two-layer
way. Layer 1 delegates to the interior ZeroPi's own check (its phi grid box/
spacing and theta charge cutoff, with the FD diagnostics above), attached under
``report.derived["interior_zeropi"]``; layer 2 refines the coupling cutoffs
``zeropi_cutoff`` (how many 0-pi levels enter the coupling, channel
``composite_coupling``) and ``zeta_cutoff`` (the zeta Fock cutoff, channel
``HO_tail``). Pass ``assume_inner_converged=True`` to skip the interior check.


.. _guide_convergence_circuit:

Custom circuits
===============

For a custom :class:`.Circuit` that is **not** hierarchically diagonalized, the
Hilbert space is a single product of the per-variable bases, and the refinement
axes are the variable cutoffs (``self.cutoff_names``): a periodic variable's charge
cutoff ``cutoff_n_<i>`` (channel ``charge_tail``) and an extended variable's cutoff
``cutoff_ext_<i>``. A discretized extended variable is a finite-difference grid
with the two truncation channels described above -- ``FD_box`` (the coordinate box
must be wide enough) and ``FD_stencil`` (the grid spacing, Richardson-extrapolated
in strict mode) -- while a harmonic extended variable uses ``HO_tail``. Each
cutoff is refined and the spectrum re-diagonalized; the dominant channel names the
cutoff to grow::

    import scqubits as scq

    circ = scq.Circuit(yaml_string, from_file=False, ext_basis="discretized")
    report = circ.check_convergence(n_levels=4, mode="moderate", target_abs_GHz=1e-4)
    print(report)

As for the other multi-coordinate qubits, cheap mode is moderate-recommended (a
coupled circuit basis has no clean cheap estimator).

**Hierarchical diagonalization.** When the circuit is hierarchically diagonalized,
the check is two-layer, like :class:`.HilbertSpace`: layer 2 refines each top-level
subsystem's ``truncated_dim`` (channel ``composite_coupling``) and re-diagonalizes
the dressed spectrum; layer 1 delegates to each subsystem's own
``check_convergence`` (attached under ``report.derived["subsystem:<id>"]``, and
skipped by ``assume_subsystems_converged=True``). The aggregate is the worse of the
two layers. A *nested* hierarchically diagonalized subsystem is recorded as
unchecked, to be verified separately.

.. note::

   A circuit returns at most ``truncated_dim`` eigenvalues, so ``n_levels`` (plus
   one buffer level in the observed-gap scope) must not exceed ``truncated_dim``;
   otherwise ``check_convergence`` raises :class:`ValueError`.


Settings
========

The defaults that control the diagnostics -- refinement step, cluster threshold,
safety factor :math:`S`, gap floor, rate floor, and default mode -- live in
:mod:`scqubits.settings` under the ``CONVERGENCE_*`` names and can be adjusted
globally; see the :ref:`guide-settings` section.


Worked example
==============

A runnable companion notebook walks through the core workflow end to end:

.. toctree::
   :maxdepth: 1

   Convergence diagnostics: a worked example <ipynb/convergence-workflow.ipynb>
