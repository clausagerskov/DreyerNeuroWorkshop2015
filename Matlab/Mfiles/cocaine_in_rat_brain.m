function c2 = cocaine_in_rat_brain(t, t0, Dose)
%modellerer coke i hjernen over tiden t i sekunder.... t0 er infusionstid og D er dosis i
%mg/kg; Data fra PAN et al 1991, Differences in the Pharmacokinetics of Cocaine, J. Neurochem. Modellen er for IV dosering!!!

if nargin < 3
    Dose = 7.5;
end
if nargin < 2
    t0 = 0;
end


d_v2 = 124*Dose/7.5;
k12 = 0.332/60;
k21 = 0.182/60;%min^-1 omregnet til s^-1
kel = 0.468/60;
 %\muM ratio of dose and distributopn volume

sumk = k12+k21+kel;
D = sqrt(sumk^2 - 4*k21*kel);



a = 0.5*(sumk + D);
b = 0.5*(sumk - D);



C= d_v2*k12/(a-b)*( exp(-b*(t-t0) ) - exp(-a*(t-t0)) );

tcoc = (t >= t0);

c2 = C.*tcoc;
