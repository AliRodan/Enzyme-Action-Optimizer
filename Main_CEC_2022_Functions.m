%______________________________________________________________________________________________%
%  Enzyme Action Optimizer (EAO) source codes (version 1.1)                              %
%                                                                                              %
%  Developed in MATLAB R2018a (7.13)                                                           %
%  Author and programmer: Ali Rodan                                                            %
%                         e-Mail: alirodan@gmail.com                                           %
%                         Homepages:                                                           %
%                         1- https://scholar.google.co.uk/citations?user=n8Z3RMwAAAAJ&hl=en    %
%                         2- https://www.researchgate.net/profile/Ali-Rodan                    %
%                                                                                              %
%   Paper Title:Enzyme Action Optimizer: A Novel Bio-inspired Optimization Algorithm.   %
%                   A. Rodan, L. Alnemer, A. Al-Tamimi, S. Mirjalili. Peter Tino (2024)                                  %
%          Enzyme Action Optimizer: A Novel Bio-inspired Optimization Algorithm.       %
%                                                                                 %
%______________________________________________________________________________________________%
clear all 
clc

% Initialize parameters
EnzymeCount = 50;
MaxIter = 1000; 
lb = -100;             
ub = 100;              
dim = 10;

% Define IEEE CEC2022 Function (F1-F12)
Fun = 1;

display(['Optimizing: ', num2str(Fun)]);

% Objective function for IEEE CEC2022 Function
fobj = @(x) cec22_test_func(x', Fun);


% Call the optimizer
[OptimalCatalysis, BestSubstrate, conv_curve] = EAO(EnzymeCount, MaxIter, lb, ub, ...
    dim, fobj);

display(['The best optimal value of the objective funciton found by EAO is : ', num2str(OptimalCatalysis)]);