function DA_modeling1

N0=3000;%# molecules released pr release
P=0.08;%release prob
alfa=0.2;%DA can be release into 20% of availble volume, thus only in free extracellular space. 
%ie it cannot be released into the cell.
Na=6.022*10^23;%advogrados tal
n=100;
p1=0.001;%density func

% 1um^3=10^15L
gamma0=((N0*P)/(alfa*Na))*p1*1E24;% 


G=gamma0*n;%DA in nM if all DA neurons fire one AP simultaniously 
Vmax=n*40;
km=160;%MM.nM. 
Tmax=20;%s
dt=0.01;%in s
t=0:dt:Tmax;
Nmax=length(t);
cDA = zeros(1,Nmax);
D2pre = zeros(1,Nmax);
Pr = zeros(1,Nmax); 

k_on = 1e-2;% Presyn AR: On rate in nanomolar! nM^-1 * s^-1
k_off = 0.4;%Presyn AR off rate! s^-1
Pmin = 0.02;
Pmax = 0.15;
Pr(1) = Pmax; 

nu=4*ones(1,Nmax);%Hz






tph = [3 5 7 13];
dtph = [1 0.2 0.2 0.2];
nuph = [0 20 60 20];

for k = 1:length(tph)
    indx = tph(k) < t & t < tph(k) + dtph(k);
    nu(indx) = nuph(k);
end


lam = nu*dt; %poisson intensity for a singel DA neuron

RAS = poissrnd(repmat(lam, n, 1)); %Make raster for all 'n' DA neurons

F = sum(RAS)/dt; %This is the frequency of all release. 

figure(1)
plot(t,nu)
title('DA neuron firing freq over time')
xlabel('time, s')
ylabel('Frequency (Hz)')


figure(2);

plot(t,F, t, kernel_smooth(F, 10))
title('summed firing freq of n neurons over time')
xlabel('time, s')
ylabel('summed firing freq of n neurons')


for k=2:Nmax
    
    dD2pre = (k_on*cDA(k-1)*(1-D2pre(k-1)) -  k_off*D2pre(k-1))*dt;
    D2pre(k) = D2pre(k-1) + dD2pre;
    
    Pr(k) = (Pmin - Pmax)*D2pre(k) + Pmax;
    
    deltaC = (gamma0/P*Pr(k-1)*F(k-1) - (Vmax*cDA(k-1)/(km+cDA(k-1))))*dt;
    
    cDA(k)=cDA(k-1)+deltaC;
end

figure(3)
plot(t,cDA)
title('DA conc over time')
xlabel('time, s')
ylabel('DA, nM')

figure(4)
plot(t,D2pre)
title('Presynaptic D2over time')
xlabel('time, s')
ylabel('D2^{pre} act')

figure(5)
plot(t,100*Pr)
title('Presynaptic D2over time')
xlabel('time, s')
ylabel('D2^{pre} act')

