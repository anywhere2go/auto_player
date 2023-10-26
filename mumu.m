clear; close all; clc;

x=[0 0.3 0.5 0.75 0.8 1];
y=[1 1.1796875 1.3 1.65 1.71875 2];

figure; plot(x,y,'-o'); xlabel('Mumu input'); ylabel('Actual scaling')

%before 0.5
%y=0.6*x+1

%after 0.5
%y=1.4*x+0.6