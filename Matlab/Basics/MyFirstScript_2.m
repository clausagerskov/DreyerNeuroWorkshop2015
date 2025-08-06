%%  Signal Processing class 2011
% My first matlab script
% Rune Berg 2011

%  Create an array of 100 random numbers  (hint:  use matlab procedure
%  "randn"  rand(100,1))

x=randn(100,1));

% Plot the numbers

figure
plot(x)

% Make a histogram of the values

figure 
hist(x)

% calculate the mean, standard deviation and variance  (mean, std, var)

mean(x)
std(x)
var(x)


%  Create and plot curves with zero mean of the following two functions.
%  y(t) = exp( - t^2    ) 
%  y(t) = exp( - abs(t) )

t=-5:.1:5;  % this creates an array from -5 to 5 with increments of 0.1

y1=exp(-abs(t));
y2=exp(-t.^2);
plot(t,y1,t,y2)
