% CGLsim1D.m
% Copyright David M. Winterbottom 2005

% ************************************************************
% Simulating the complex Ginzburg-Landau equation in 1D using
% pseudo-spectral code and ETD2 exponential time-stepping (See
% Matthews and Cox, J. Comp. Phys., 176 430-455, 2002)
% ************************************************************

disp('*** 1D CGL SIMULATION ***');

% Set equation coefficients
a = -2;
b = 0.7;

% Set system parameters
L    = 200;       % Domain size
Tmax = 200;       % Simulation time
N    = 512;       % Number of grid points
dT   = 0.05;      % Timestep (choose between 0.01 and 0.05)
dps  = 1000;      % Number of stored times
ic   = 'pulse';   % Initial condition: choose 'zero', 'tw', 'uniform' or 'pulse'
n    = 0;         % Winding number for 'tw' initial condition
co   = 0;         % Whether to continue simulation from final values of previous

% Calculate some further parameters
nmax = round(Tmax/dT);
q    = n*2*pi/L; 
X    = (L/N)*(-N/2:N/2-1)'; 
nplt = floor(nmax/dps);

% Define initial conditions
if co == 0 
	Tdata = zeros(1,dps+1);
	if strcmp(ic, 'zero')
		A = zeros(size(X)) + 10^(-2)*randn(size(X));
	elseif strcmp(ic, 'tw')
		A 	= sqrt(1-q^2)*exp(i*q*X) + 10^(-2)*randn(size(X));
	elseif strcmp(ic, 'uniform')
		A 	= ones(size(X)) + 0.01*randn(size(X));
	elseif strcmp(ic, 'pulse')
		A 	= sech((X+10).^2) + 0.8*sech((X-30).^2) + 10^(-2)*randn(size(X));
	else
		error('invalid initial condition selected')
	end
	Tdata(1) = 0;
else
	A         = Adata(:,end);
	starttime = Tdata(end);
	Tdata     = zeros(1,dps+1);
	Tdata(1)  = starttime;
	disp('    CARRYING OVER...')
end	

% Set wavenumbers and data arrays
k = [0:N/2-1 0 -N/2+1:-1]'*(2*pi/L);
k2 = k.*k; k2(N/2+1) = ((N/2)*(2*pi/L))^2;
Adata     = zeros(N,dps+1);
A_hatdata = zeros(N,dps+1);
A_hat          = fft(A);
Adata(:,1)     = A;
A_hatdata(:,1) = A_hat;

% Compute exponentials and nonlinear factors for ETD2 method
cA 	    	= 1-k2*(1+i*a);
expA 	  	= exp(dT*cA);
nlfacA  	= (exp(dT*cA).*(1+1./cA/dT)-1./cA/dT-2)./cA;
nlfacAp 	= (exp(dT*cA).*(-1./cA/dT)+1./cA/dT+1)./cA;

% Solve PDE
dataindex = 2;
for n = 1:nmax
	T = Tdata(1) + n*dT;
	A = ifft(A_hat);
	
	% Find nonlinear component in Fourier space
	nlA	= -(1+i*b)*fft(A.*abs(A).^2);
	
	% Setting the first values of the previous nonlinear coefficients
	if n == 1
		nlAp = nlA;
	end
	
	% Time-stepping
	A_hat = A_hat.*expA + nlfacA.*nlA + nlfacAp.*nlAp;
	nlAp  = nlA;
	
	% Saving data
	if mod(n,nplt) == 0 
		A = ifft(A_hat);
		Adata(:,dataindex)     = A; 
		A_hatdata(:,dataindex) = A_hat; 
		Tdata(dataindex)       = T;
		dataindex              = dataindex + 1;
	end
	
	% Commenting on time elapsed
	if mod(n,floor(nmax/10)) == 0
		outp = strcat('  n= ', num2str(n), ' completed'); disp(outp);
	end
end

% Plot evolution
figure('position', [200 200 300 350])
surf(X,Tdata,real(Adata).')
view(0,90), shading interp, axis tight
set(gca,'position', [0 0 1 1])
set(gca,...
	'xcolor',		[0.6 0.6 0.6],...
	'ycolor',		[0.6 0.6 0.6],...
	'fontsize',	6,...
	'fontname', 'courier')
xlabel('X',...
	'fontname', 'courier',...
	'fontsize', 6,...
	'color',		[0.6 0.6 0.6])
ylabel('T',...
	'fontname', 'courier',...
	'fontsize', 6,...
	'color',		[0.6 0.6 0.6],...
	'rotation', 0)
title('evolution of |A|',...
	'fontname', 'courier',...
	'fontsize', 6,...
	'color', 		[0.6 0.6 0.6])
