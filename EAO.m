function [OptimalCatalysis, BestSubstrate, conv_curve] = EAO(EnzymeCount, MaxIter, LB, UB, ...
    ActiveSiteDimension, EvaluateCatalysis)

% --- 1) Initialization ---
SubstratePool = LB + (UB - LB) .* rand(EnzymeCount, ActiveSiteDimension);
ReactionRate = arrayfun(@(i) EvaluateCatalysis(SubstratePool(i,:)),1:EnzymeCount)';
[OptimalCatalysis, idx] = min(ReactionRate);
BestSubstrate = SubstratePool(idx,:);
conv_curve = zeros(1, MaxIter);

%EAO parameter (Enzyme Concentration EC)
EC = 0.1;


for t = 1:MaxIter
   
    AF = sqrt(t / MaxIter);
    
    for i = 1:EnzymeCount
        
        % 1) Update FirstSubstratePosition
        FirstSubstratePosition = (BestSubstrate - SubstratePool(i,:)) + rand(1, ActiveSiteDimension) ...
                                 .* sin(AF * SubstratePool(i,:));
        FirstSubstratePosition = max(min(FirstSubstratePosition, UB),LB);
        FirstEvaluation = EvaluateCatalysis(FirstSubstratePosition);
        
        % 2) Pick two random distinct Substrates
        Substrates = randperm(EnzymeCount, 2);
        while any(Substrates == i)
            Substrates = randperm(EnzymeCount, 2);
        end
        S1 = SubstratePool(Substrates(1), :);
        S2 = SubstratePool(Substrates(2), :);

        % 2.1) vector-valued random factors for each dimension
        scA1 = EC + (1-EC)*rand(1, ActiveSiteDimension);
        exA  = (EC + (1-EC)*rand(1, ActiveSiteDimension)) .* AF;
        CandidateA = SubstratePool(i,:) + scA1 .* (S1 - S2) + exA  .* (BestSubstrate - SubstratePool(i,:));
        CandidateA = max(min(CandidateA, UB), LB);
        CandidateAFitness = EvaluateCatalysis(CandidateA);

        % 2.2) scalar random factors for all dimensions
        scB1 = EC + (1-EC)*rand();
        exB  = (EC + (1-EC)*rand()) * AF;
        CandidateB = SubstratePool(i,:) + scB1 .* (S1 - S2) + exB  .* (BestSubstrate - SubstratePool(i,:));
        CandidateB = max(min(CandidateB, UB), LB);
        CandidateBFitness = EvaluateCatalysis(CandidateB);

        % 2.3) Pick better candidate (Update SecondSubstratePosition)
        if CandidateAFitness < CandidateBFitness
            SecondSubstratePosition = CandidateA;
            SecondEvaluation      = CandidateAFitness;
        else
            SecondSubstratePosition = CandidateB;
            SecondEvaluation      = CandidateBFitness;
        end

        % 3) Compare FirstSubstratePosition vs. SecondSubstratePosition
        if FirstEvaluation < SecondEvaluation
            UpdatedPosition = FirstSubstratePosition;
            UpdatedFitness  = FirstEvaluation;
        else
            UpdatedPosition = SecondSubstratePosition;
            UpdatedFitness  = SecondEvaluation;
        end

        % 4) Update SubstratePool & Global Best
        if UpdatedFitness < ReactionRate(i)
            SubstratePool(i, :) = UpdatedPosition;
            ReactionRate(i)     = UpdatedFitness;
            if UpdatedFitness < OptimalCatalysis
                OptimalCatalysis = UpdatedFitness;
                BestSubstrate    = UpdatedPosition;
            end
        end
    end
    conv_curve(t) = OptimalCatalysis;
end
end