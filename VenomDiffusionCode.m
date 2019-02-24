%==========================
% Forward-Euler Simulation of Venom-Antivenom Model in 1D
%
% Author: Nathan Holt
%==========================

numx = 201;   %number of grid points in x
numt = 200000;  %number of time steps to be iterated
dx = 1/(numx - 1);
dt = 0.00001;

x = 0:dx:1;   %vector of x values, to be used for plotting

A = zeros(numx,numt);   %initialize everything to zero
V = zeros(numx,numt);   %initialize everything to zero

%specify initial conditions
t(1) = 0;      %t=0
mu = 0.5;      
sigma = 0.05;
for i=1:numx
   A(i:round(numx/2),1)=0;
   A(round(numx/2):numx,1)=1;
   V(i:round(numx/2),1) = 1;
   V(round(numx/2):numx,1) = 0;
   %C(i,1) = exp(-(x(i)-mu)^2/(2*sigma^2)) / sqrt(2*pi*sigma^2);
end

%{
Da = 2.01*10^(-8); %Diffusion coefficient for A
Dv = 6.00 * 10^(-8); %Diffusion coefficient for V
Rv = 1.1 * 10^(-8); %Reaction coefficient for V
Ra = 10^(-6); %Reaction coefficient for A
k = 1;
%}

Da = (60^4)*2.01*10^(-8); %Diffusion coefficient for A
Dv = (60^4)*6.00 * 10^(-8); %Diffusion coefficient for V
Rv = (60^2)*1.1 * 10^(-8); %Reaction coefficient for V
Ra = (60^2)*10^(-6); %Reaction coefficient for A
k = 1; %Interaction rate


%iterate difference equations
for j=1:numt
   t(j+1) = t(j) + dt;
   for i=2:numx-1
      A(i,j+1) = A(i,j) - Ra*k*A(i,j)*V(i,j)+((60^2)/450000)*log(1/2)*A(i,j)*dt + Da*(dt/dx^2)*(A(i+1,j) - 2*A(i,j) + A(i-1,j)); 
      V(i,j+1) = V(i,j) - Rv*k*A(i,j)*V(i,j)+((60^2)/54000)*log(1/2)*V(i,j)*dt + Dv*(dt/dx^2)*(V(i+1,j) - 2*V(i,j) + V(i-1,j)); 
   end
   A(1,j+1) = A(2,j+1);          %C(1,j+1) found from no-flux condition
   A(numx,j+1) = A(numx-1,j+1);  %C(numx,j+1) found from no-flux condition
   V(1,j+1) = V(2,j+1);          %C(1,j+1) found from no-flux condition
   V(numx,j+1) = V(numx-1,j+1);  %C(numx,j+1) found from no-flux condition
end

%{
h=figure(2);
hold on;
   ylim([0 1])
   xlabel('x');
    ylabel('concentration');
       plot(x,V(:,1000),'blue')
       plot(x,A(:,1000),'red')
       plot(x,V(:,5000),'blue')
       plot(x,A(:,5000),'red')
       plot(x,V(:,10000),'blue')
       plot(x,A(:,10000),'red')
       legend('venom','antivenom')
       title('Space profiles over time')
hold off;
%}

%{
h=figure(2);
for t = 1:10:numt
   hold on;
   plot(x,V(:,t))
   plot(x,A(:,t))
   ylim([0 1])
   xlabel('x');
    ylabel('concentration');
    legend('venom','antivenom')
    title(['t = ',num2str(t*dt*60),' hours'])
   pause(0.01)
   
   % Capture the plot as an image 
      frame = getframe(h); 
      im = frame2im(frame); 
      [imind,cm] = rgb2ind(im,256); 
      filename = 'sim2.gif';

      % Write to the GIF File 
      if t == 1 
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
      else 
          imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',0.001); 
      end
   
   hold off;
   clf;
end
%}

h = figure(1);
for t = 1:numt
    
    hold on;
    plot(x,V(:,t));
    plot(x,A(:,t));
    hold off;
    xlabel('x');
    ylabel('concentration');
    legend('venom','antivenom')
    title(['t = ',num2str(t*dt*60),' hours'])

pause(0.001)
        %{
      % Capture the plot as an image 
      frame = getframe(h); 
      im = frame2im(frame); 
      [imind,cm] = rgb2ind(im,256); 
      filename = 'sim1.gif';

      % Write to the GIF File 
      if t == 1 
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
      else 
          imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',0.001); 
      end 
    %}
    clf;

end
