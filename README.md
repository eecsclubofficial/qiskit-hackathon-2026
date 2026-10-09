# Qiskit Fall Fest Hackathon

**Kick-off:** Oct 9, 2026 · **Venue:** Vatsal · **Duration:** one week · **Hosts:** IISER Bhopal (EECS Club and Physics Club)

You have one week, a laptop, and AI assistants. Pick a quantum problem, build it, test it against a classical alternative, and tell us honestly what worked and what did not.

| Item | Details |
|------|---------|
| Submission deadline | `[SUBMISSION DEADLINE - to be confirmed by organisers]` |
| Team size | `[TEAM SIZE - to be confirmed by organisers]` |
| Where to submit | `[SUBMISSION FORM / CHANNEL LINK]` |
| Questions | `[ORGANISER CONTACT EMAIL]` |

## Contents

- [What we reward](#what-we-reward)
- [How the hackathon works](#how-the-hackathon-works)
- [Tracks and problem overview](#tracks-and-problem-overview)
- [Go beyond: combine tracks or invent your own](#go-beyond-combine-tracks-or-invent-your-own)
- [What to submit](#what-to-submit)
- [Judging criteria](#judging-criteria)
- [Bonus: real hardware](#bonus-real-hardware)
- [Using AI](#using-ai)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)

## What we reward

A project that **works**, that you can **explain line by line**, and that is **honestly compared against a classical alternative**. Using AI to write code is allowed and encouraged; being unable to explain or verify that code is not.

## How the hackathon works

- The ten problem statements are **suggestions, not a menu**. You may pick one, extend one, combine several, or invent something more ambitious. Original, advanced and cross-track projects are judged on the same criteria.
- Each problem has the same parts: background, the problem itself, **core tasks** (the minimum for a complete submission), **stretch goals** (what makes it excellent), and a hint on tools.
- **Simulators first, hardware as a bonus.** Everything can be done on a simulator (Qiskit Aer or the statevector tools). Running a small version on real IBM hardware earns extra credit in any track.
- The full rules are in [`docs/guidelines_and_submission_rules.pdf`](docs/guidelines_and_submission_rules.pdf). Read them before you start.

## Tracks and problem overview

Each track has its own PDF with the complete problem statements (background, problem, core tasks, stretch goals, hints), the combined-project ideas that involve the track, the deliverables and the judging criteria.

| Track | PDF | Problems |
|-------|-----|----------|
| 1. Quantum chemistry | [`track1_quantum_chemistry.pdf`](tracks/track1_quantum_chemistry.pdf) | 1, 2 |
| 2. Quantum machine learning | [`track2_quantum_machine_learning.pdf`](tracks/track2_quantum_machine_learning.pdf) | 3, 4 |
| 3. QAOA and optimisation | [`track3_qaoa_optimisation.pdf`](tracks/track3_qaoa_optimisation.pdf) | 5, 6 |
| 4. Quantum error correction | [`track4_quantum_error_correction.pdf`](tracks/track4_quantum_error_correction.pdf) | 7, 8 |
| 5. Quantum key distribution | [`track5_quantum_key_distribution.pdf`](tracks/track5_quantum_key_distribution.pdf) | 9 |
| 6. Post-quantum cryptography | [`track6_post_quantum_cryptography.pdf`](tracks/track6_post_quantum_cryptography.pdf) | 10 |

### Track 1: Quantum chemistry

**Problem 1: The hydrogen molecule with VQE.** Compute the ground-state energy of H₂ across a range of bond lengths with the Variational Quantum Eigensolver, and decide how trustworthy your answer is.
- *Core:* build and qubit-reduce the STO-3G Hamiltonian; VQE with at least two ansätze and a classical optimiser; bond curve from about 0.3 to 3 Å with equilibrium and dissociation marked; compare against exact diagonalisation and report the error against chemical accuracy (about 1.6 mHa).
- *Stretch:* noise model plus error mitigation; one bond length on IBM hardware; an excited state (e.g. VQD) or the dipole; effect of optimiser and number of circuit evaluations on convergence.

**Problem 2: Cyclohexane with sample-based quantum diagonalisation (SQD).** Estimate the relative energies of cyclohexane conformers with SQD, and measure how well the sampled subspace captures the true ground state.
- *Core:* justified active space; chair plus at least one other conformer; sampling circuit (e.g. LUCJ) and the SQD workflow including configuration recovery; conformer energies and gaps in kcal/mol; comparison with a classical reference such as CASCI.
- *Stretch:* convergence against subspace size and number of samples; ideal vs noisy vs hardware samples; which conformer ordering is and is not reproduced, and why; larger active spaces and where the classical step becomes the bottleneck.

### Track 2: Quantum machine learning

**Problem 3: Build and benchmark a variational quantum classifier.** Build a VQC from scratch, and find out when it helps, when it fails, and why.
- *Core:* a dataset reduced to a few qubits; your own feature map, ansatz and readout; train/test accuracy and a learning curve on a held-out set; at least two classical baselines with a similar number of parameters.
- *Stretch:* feature-map and depth study; comparison with a quantum kernel; shot-noise and hardware-noise robustness; 2D decision boundary.

**Problem 4: A quantum neural network that avoids barren plateaus.** Show a barren plateau, then build and evaluate a network that mitigates it.
- *Core:* gradient variance against qubits (2 to 10) and depth on a log plot; at least one mitigation strategy with the same measurement repeated; train the mitigated network on a small task and compare loss and convergence; explain why the strategy works.
- *Stretch:* compare two or three strategies; show a global cost causes a plateau even when shallow; test whether noise creates its own plateau; combine with another track.

### Track 3: QAOA and optimisation

**Problem 5: MaxCut with QAOA, and how good is good enough.** Measure how answer quality depends on layers, graph and optimiser.
- *Core:* your own cost operator and p-layer circuit; at least three graph types with 6 to 12 nodes for p = 1, 2, 3; approximation ratio and optimal-cut probability against brute force; comparison with greedy, local search or Goemans-Williamson.
- *Stretch:* COBYLA vs SPSA vs gradient-based and smart initial angles; warm-starting or a different mixer; noise and the largest useful p; a small hardware run.

**Problem 6: A routing problem: deliveries on a small map.** Encode a small routing problem as a QUBO or Ising problem, solve it with QAOA, and find where it breaks down.
- *Core:* a TSP with 4 or 5 locations (or vehicle routing with two vehicles) and its distance matrix; the qubit encoding, distance and penalty terms and qubit count; how often valid and best-valid routes appear; comparison with brute force and a classical heuristic, and the effect of the penalty weight.
- *Stretch:* a more qubit-efficient encoding; invalid-route fraction vs penalty weight and layers; scaling and runtime; a validity-preserving mixer.

### Track 4: Quantum error correction

**Problem 7: A logical qubit with the Steane code.** Build, test and use a working Steane-code logical qubit in Qiskit.
- *Core:* encoding circuit and stabilisers; syndrome extraction with ancillas and a lookup table; inject all 21 single-qubit errors and show each is corrected (as a table); at least one transversal logical gate.
- *Stretch:* two-error failure and logical-vs-physical error rate with the break-even point; mid-circuit measurement and feed-forward; flag qubits or repeated syndromes; use the logical qubit in a larger task.

**Problem 8: LDPC decoding from scratch.** Implement an LDPC decoder, measure it against noise, and understand why it works and where it fails.
- *Core:* a sparse parity-check matrix (a few hundred bits) and a drawn Tanner graph; belief propagation (sum-product or min-sum) over a binary symmetric channel; FER and BER against channel error probability with the threshold region identified; one figure of message evolution.
- *Stretch:* compare with bit flipping and an improved decoder; quantum LDPC codes with BP+OSD and why plain BP struggles; fixed-point arithmetic cost; use inside QKD reconciliation.

### Track 5: Quantum key distribution

**Problem 9: BB84 and BBM92 in Qiskit.** Implement both protocols end to end, attack them with an eavesdropper, and extract secure key from noisy, partly compromised data.
- *Core:* BB84 with sifting and the sifted key rate (about half the qubits ideally); BBM92 with Bell pairs; an intercept-and-resend Eve (QBER around 25% when she attacks every qubit) with QBER against attack fraction; channel noise and an abort/keep decision rule.
- *Stretch:* error estimation, reconciliation and privacy amplification with final key rate against QBER; a CHSH test for BBM92; losses and detector imperfections; swap in the LDPC decoder (Problem 8) or a Steane-coded logical qubit (Problem 7).

### Track 6: Post-quantum cryptography

**Problem 10: Lattice-based cryptography from scratch.** Implement a small lattice-based encryption scheme, test its correctness, and explore where its security comes from.
- *Core:* a toy LWE public-key scheme with written-down parameters; decryption failure rate against noise and the noise/correctness trade-off; an attack on tiny parameters (LLL or brute force) with cost against dimension; one figure explaining why noise makes an easy linear-algebra problem hard.
- *Stretch:* NTT-based polynomial arithmetic and a simplified Kyber-style key exchange; Shor's algorithm factoring 15 or 21 in Qiskit; key and ciphertext sizes against RSA and elliptic curves; a timing-leak weakness and its fix.

## Go beyond: combine tracks or invent your own

The most impressive entries will not stop at one box. None of these is required.

| Idea | Tracks combined | What makes it interesting |
|------|-----------------|---------------------------|
| A logical qubit inside a QKD protocol | Steane code and BB84 or BBM92 | Does encoding the transmitted qubits lower the QBER, and at what cost in qubits? |
| LDPC reconciliation in QKD post-processing | LDPC decoding and QKD | Replace a simple error-correction step with your own decoder, and plot final key rate against QBER. |
| A neural-network decoder | QNN and error correction | Train a quantum or classical network to decode Steane syndromes, and compare with the lookup table. |
| Logical qubits inside an optimiser | Steane code and QAOA or VQE | Does error protection improve the answer on a noisy simulator, or does the overhead cancel the gain? |
| Barren-plateau-aware chemistry | VQE and QNN mitigation | Apply identity-block initialisation or layer-wise training to a larger VQE ansatz. |
| Quantum-safe key exchange pipeline | Lattice cryptography and QKD | Compare a lattice-based key exchange with QKD in security assumptions, cost and failure modes. |
| QAOA for code design | QAOA and error correction | Search for good parity-check matrices or qubit layouts as an optimisation problem. |
| Decoder as a hardware design | LDPC decoding and FPGA or fixed-point design | Quantify the accuracy lost by low-precision arithmetic, as a first step toward hardware. |

**Open invitation.** Have your own idea, such as a quantum game, an algorithm tutor, a benchmark of a quantum algorithm from the workshop (Grover, phase estimation, the QFT), or a tool that makes any of the above easier for the next student? Write three sentences on the problem, the method, and how you will know it worked, and check with the organisers early in the week.

**Scoping a combined project.** Get the smallest version of each part working separately first, then connect them. A small, honest, working combination beats an ambitious one that does not run.

## What to submit

Every team submits **a GitHub repository** that contains everything below. Start from [`submission-template/`](submission-template/).

1. **Code repository.** All your code in one GitHub repo that **runs from a clean start**, with the **versions of the packages listed** (`requirements.txt` with pinned versions, plus your Python version in the README).
2. **One write-up PDF** (two to four pages, `WRITEUP.pdf` in the repo root) with these sections:
   - **Problem**
   - **Method**
   - **Results**
   - **Honest limits**
3. **At least one figure** that shows the main result (in the write-up, and saved in `figures/`).
4. **A short AI-use note:** which tools you used, **one thing the AI got wrong**, and **how you caught it**.
5. **A five-minute demo followed by questions.** Every team member must be able to take questions.

How to submit: create a GitHub repository, push all code, the write-up PDF, figures and the AI-use note, then send the repository link through `[SUBMISSION FORM / CHANNEL LINK]` before the deadline. Never commit API tokens or secrets.

The full list of rules, the repo requirements, the write-up outline and a final checklist are in [`docs/guidelines_and_submission_rules.pdf`](docs/guidelines_and_submission_rules.pdf).

## Judging criteria

The same scoring applies to every problem and to original projects alike.

| Criterion | Points | What judges look for |
|-----------|--------|----------------------|
| Correctness and verification | 30 | Results checked against an exact or classical reference, tests, sensible error bars |
| Understanding and insight | 25 | Clear explanation of why the method works or fails, shown in the write-up and in the live questions |
| Honest comparison and limits | 20 | A fair classical baseline, stated assumptions, no unsupported claims of quantum advantage |
| Ambition and originality | 15 | Stretch goals, combined tracks, or a new idea beyond the suggested statements |
| Clarity of demo and code | 10 | Readable, reproducible code and a clear five-minute story |
| **Total** | **100** | |

## Bonus: real hardware

Bonus points are available for a hardware run on a real IBM backend, with a clear comparison against the simulator. Record the backend name, date, job ID, and show the hardware and simulator results side by side.

## Using AI

AI assistants are welcome at every step. The AI-use note and the live questions exist because the person submitting is responsible for the result: you should be able to explain each circuit, formula and plot, and show how you verified it.

## Repository layout

```
.
├── README.md                          <- this file
├── docs/
│   └── guidelines_and_submission_rules.pdf
├── tracks/
│   ├── track1_quantum_chemistry.pdf
│   ├── track2_quantum_machine_learning.pdf
│   ├── track3_qaoa_optimisation.pdf
│   ├── track4_quantum_error_correction.pdf
│   ├── track5_quantum_key_distribution.pdf
│   └── track6_post_quantum_cryptography.pdf
├── submission-template/               <- copy this to start your own repo
│   ├── README.md
│   ├── requirements.txt
│   ├── WRITEUP_TEMPLATE.md
│   ├── AI_USE_NOTE.md
│   ├── SUBMISSION_CHECKLIST.md
│   ├── src/  tests/  figures/
│   └── .gitignore
└── scripts/
    ├── content.py                     <- all hackathon text (edit here)
    ├── build_pdfs.py                  <- regenerates every PDF
    └── check_submission.py            <- self-check for your repo
```

## Getting started

1. Read [`docs/guidelines_and_submission_rules.pdf`](docs/guidelines_and_submission_rules.pdf) and the PDF for your track in [`tracks/`](tracks/).
2. Create a new GitHub repository for your team and copy the contents of [`submission-template/`](submission-template/) into it.
3. Build the smallest working version first, check it against an exact or classical reference, then add stretch goals.
4. Before submitting, run the self-check from this repo against your own repository:

   ```bash
   python scripts/check_submission.py /path/to/your-team-repo
   ```

5. Test a clean install in a fresh virtual environment, then submit your repository link.

### For organisers: regenerating the PDFs

All text lives in `scripts/content.py`. Fill in the placeholders at the top of that file (deadline, team size, contact, submission link), then:

```bash
pip install -r requirements-organisers.txt
python scripts/build_pdfs.py
```
