function DA_modeling1

No=3000;%# molecules released pr release
P=0.08;%release prob
alfa=0.2;%DA can be release into 20% of availble volume, thus only in free extracellular space. 
%ie it cannot be released into the cell.
Na=6.022*10^23;%advogrados tal
n=100;
p1=0.001;%density func

% 1um^3=10^15L
gamma0=((No*P)/(alfa*Na))*p1*1E24;% 


G=gamma0*n;%DA in nM if all DA neurons fire one AP simultaniously 
Vmax=n*40;
km=160;%MM.nM. 
kmcoc=1000;%nM.15 mg/kg coc ip
Tmax=10;%s
dt=0.001;%in s
t=0:dt:Tmax;
Nmax=length(t);
cDA=zeros(1,Nmax);
cDAcoc=zeros(1,Nmax);


nu=4*ones(1,Nmax);%Hz

tpause1=3;
tpause2=4;
tburst3=5.5;
tburst4=5.7;
tburst5=7;
tburst6=7.2;

nu(tpause1 < t) = 0;
nu(tpause2 < t) = 4;
nu(tburst3 < t) = 20;
nu(tburst4 < t) = 4;
nu(tburst5 < t) = 20;
nu(tburst6 < t) = 4;

for k=1:n
    RAS(k,:) = poissrnd(nu*dt);
end

F = sum(RAS)/dt;

%figure(1);
%plot(t,F)
%title('summed firing freq of n neurons over time')
%xlabel('time, s')
%ylabel('summed firing freq of n neurons')

for k=2:Nmax
    deltaC=(gamma0*F(k-1)-Vmax*cDA(k-1)/(km+cDA(k-1)))*dt;
    cDA(k)=cDA(k-1)+deltaC;
end

figure(2)
plot(t,cDA)
title('DA conc over time')
xlabel('time, s')
ylabel('DA, nM')

figure(3)
plot(t,nu)
title('DA neuron firing freq over time')
xlabel('time, s')
ylabel('Frequency, Hz')

for k=2:Nmax
    deltaCcoc=(gamma0*F(k-1)-Vmax*cDAcoc(k-1)/(kmcoc+cDAcoc(k-1)))*dt;
    cDAcoc(k)=cDAcoc(k-1)+deltaCcoc;
end



figure(4)
plot(t,cDAcoc)
title('DA conc over time')
xlabel('time, s')
ylabel('DA, nM')


