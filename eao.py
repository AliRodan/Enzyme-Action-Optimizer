# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:20:20 2025

@author: aliro
"""

import numpy as np

def EAO(EnzymeCount, MaxIter, LB, UB, ActiveSiteDimension, EvaluateCatalysis):
    """
    Enzymes' Active Optimization (EAO) optimizer in Python.
    """

    # Convert LB, UB to numpy arrays (in case they are scalars or lists)
    LB = np.array(LB, dtype=float)
    UB = np.array(UB, dtype=float)

    # --- 1) Initialization ---
    # SubstratePool is EnzymeCount x ActiveSiteDimension
    # Each row is a substrate solution vector
    SubstratePool = LB + (UB - LB) * np.random.rand(EnzymeCount, ActiveSiteDimension)

    # Evaluate each substrate
    ReactionRate = np.array([EvaluateCatalysis(SubstratePool[i, :]) for i in range(EnzymeCount)])
    
    # Find the global best
    OptimalCatalysis = np.min(ReactionRate)
    idx = np.argmin(ReactionRate)
    BestSubstrate = SubstratePool[idx, :].copy()

    # Convergence curve
    conv_curve = np.zeros(MaxIter)

    # EAO parameter (Enzyme Concentration, EC)
    EC = 0.1

    for t in range(MaxIter):
        # AF = sqrt(t / MaxIter), here t+1 for iteration indexing
        AF = np.sqrt((t + 1) / MaxIter)

        for i in range(EnzymeCount):
            # --- 1) Update FirstSubstratePosition ---
            FirstSubstratePosition = (BestSubstrate - SubstratePool[i, :]) + \
                                     np.random.rand(ActiveSiteDimension) * \
                                     np.sin(AF * SubstratePool[i, :])
            # Enforce bounds
            FirstSubstratePosition = np.minimum(FirstSubstratePosition, UB)
            FirstSubstratePosition = np.maximum(FirstSubstratePosition, LB)

            FirstEvaluation = EvaluateCatalysis(FirstSubstratePosition)

            # --- 2) Pick two random distinct Substrates (none equals i) ---
            while True:
                rand_idx = np.random.choice(EnzymeCount, 2, replace=False)
                if i not in rand_idx:
                    break
            S1 = SubstratePool[rand_idx[0], :]
            S2 = SubstratePool[rand_idx[1], :]

            # --- 2.1) Vector-valued random factors for each dimension ---
            scA1 = EC + (1 - EC) * np.random.rand(ActiveSiteDimension)
            exA = (EC + (1 - EC) * np.random.rand(ActiveSiteDimension)) * AF

            CandidateA = SubstratePool[i, :] + scA1 * (S1 - S2) + \
                         exA * (BestSubstrate - SubstratePool[i, :])
            # Enforce bounds
            CandidateA = np.minimum(CandidateA, UB)
            CandidateA = np.maximum(CandidateA, LB)
            CandidateAFitness = EvaluateCatalysis(CandidateA)

            # --- 2.2) Scalar random factors for all dimensions ---
            scB1 = EC + (1 - EC) * np.random.rand()
            exB = (EC + (1 - EC) * np.random.rand()) * AF

            CandidateB = SubstratePool[i, :] + scB1 * (S1 - S2) + \
                         exB * (BestSubstrate - SubstratePool[i, :])
            # Enforce bounds
            CandidateB = np.minimum(CandidateB, UB)
            CandidateB = np.maximum(CandidateB, LB)
            CandidateBFitness = EvaluateCatalysis(CandidateB)

            # --- 2.3) Pick better candidate (Update SecondSubstratePosition) ---
            if CandidateAFitness < CandidateBFitness:
                SecondSubstratePosition = CandidateA
                SecondEvaluation = CandidateAFitness
            else:
                SecondSubstratePosition = CandidateB
                SecondEvaluation = CandidateBFitness

            # --- 3) Compare FirstSubstratePosition vs. SecondSubstratePosition ---
            if FirstEvaluation < SecondEvaluation:
                UpdatedPosition = FirstSubstratePosition
                UpdatedFitness = FirstEvaluation
            else:
                UpdatedPosition = SecondSubstratePosition
                UpdatedFitness = SecondEvaluation

            # --- 4) Update SubstratePool & Global Best ---
            if UpdatedFitness < ReactionRate[i]:
                SubstratePool[i, :] = UpdatedPosition
                ReactionRate[i] = UpdatedFitness
                if UpdatedFitness < OptimalCatalysis:
                    OptimalCatalysis = UpdatedFitness
                    BestSubstrate = UpdatedPosition.copy()

        conv_curve[t] = OptimalCatalysis

    return OptimalCatalysis, BestSubstrate, conv_curve
