%function izhikevich()
%excitatory neurons         %inhibitory neurons
Ne = 800;                   Ni = 200;
re = rand(Ne, 1);           ri = rand(Ni,1);
%a = time scale of recovery variable u
%smaller values = slower recovery
a = [0.02*ones(Ne,1);       0.02+0.08*ri];
%influences membrane resting potential
%specifically the sensitivity of 
%recovery variable u to subthreshold v
%fluctuations
b = [0.2*ones(Ne,1);        0.25-0.05*ri];
%c = after-spike reset value of v
%because of fast high-threshold K+ conductance
c = [-65+15*re.^2;          -65*ones(Ni,1)];
%after-spike reset of recov var u
%caused by slow high-threshold K+ and Na+ conductances
d = [8-6*re.^2;             2*ones(Ni,1)];
S = [0.5*rand(Ne+Ni,Ne),    -rand(Ne+Ni,Ni)];

v = -65*ones(Ne+Ni,1); %initial vals of v
%u = membrane recovery variable
u = b.*v;              %initial vals of b
firings = [];          %spike timings

for t = 1:1000
    I = [5*randn(Ne,1); 2*randn(Ni,1)]; %thalamic input 
                                       %(5 and 2 hz for ex and in)    
    fired = find(v>= 30); %indiced of neurons that spiked
    firings = [firings; t+0*fired,fired];
    v(fired) = c(fired);
    u(fired) = u(fired) + d(fired);
    I = I + sum(S(:,fired),2);
    v = v + 0.5*(0.04*v.^2 + 5*v + 140 - u + I);
    v = v + 0.5*(0.04*v.^2 + 5*v + 140 - u + I);
    u = u + a.*(b.*v - u);
end;
plot(firings(:,1), firings(:,2),'.');




