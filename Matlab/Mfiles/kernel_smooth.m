function smX= kernel_smooth(X, w)
%smX = kernel_smooth(X, w)
%Udglatter signalet X ved en Gaussisk kernel af bredde w. Det udglattede
%signal er normaliseret

if w == 0
    smX = X;
    return
end

L = 3; %Antal standardafvigelser i kernel

i = -(L*w):(L*w);
f = 1/sqrt(2*pi*w^2)*exp(-i.^2/(2*w^2));

smX = zeros(size(X));
paddedX = [zeros(L*w,1); X(:); zeros(L*w,1)];

for k = 1:length(X)  
    smX(k) = f*paddedX(i+L*w+k);
end

