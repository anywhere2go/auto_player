clear; close all;

a=2.4; b=3; n=5;
pd1 = makedist('Uniform','lower',a,'upper',b);
dx = 0.0001; % to ensure constant spacing
x = a:dx:b; % Could include some of the region where
pdfx = pdf(pd1,x);

for i=1:n
    if i==1
        y=linspace(x(1)+x(1), x(end)+x(end), length(x)+length(x)-1);
        pdfy = conv(pdfx,pdfx)*dx;
    else
        y=linspace(x(1)+y(1), x(end)+y(end), length(x)+length(y)-1);
        pdfy = conv(pdfx,pdfy)*dx;
    end
    
end

plot(y,pdfy); grid on;
xlabel('Speed'); ylabel('PDF');

sum(pdfy(find((y>=17.5))).*dx)
sum(pdfy(find((y<=17.5) & (y>=16.5))).*dx)
sum(pdfy(find((y<=16.5) & (y>=15.5))).*dx)
sum(pdfy(find((y<=15.5) & (y>=14.5))).*dx)
sum(pdfy(find((y<=14.5))).*dx)

y(find(y==max(pdfy)))