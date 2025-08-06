function xenoneuronmodel()
%model for xenopus spinal neurons
t = 1:0.1:60;
V = zeros(length(t));
Cm = 1;
gleak = 1e-9;
V = 1;
Erev = -70e-3;
Iinf = 1;
INa = 1;
ICa = 1;
IKf = 1;
IKs = 1;
IKNa = 1;
Ileak = gleak*(V-Erev);
I syn
for i=0:length(t)
    %update currents
    %check for Vm reaching threshold
    %do threshold activity (e.g spiking)
