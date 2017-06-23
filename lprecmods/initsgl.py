from numpy import *

class Pgl:
	def __init__(self, Nspan,N,proj,s,thsp,rhosp,aR,beta,B3com,am,g):
		self.Nspan=Nspan
		self.N=N
		self.Nproj=size(proj)
		self.Ntheta=size(thsp)
		self.Nrho=size(rhosp)

		self.proj=proj
		self.s=s
		self.thsp=thsp
		self.rhosp=rhosp

		self.aR=aR
		self.beta=beta
		self.B3com=B3com
		self.am=am
		self.g=g

def create_gl(N,Nproj):
	"initialize global parameters for the log-polar-based method and save to file"
	Nspan=3
	proj=linspace(0,pi,Nproj+1)
	proj=proj[0:-1]
	s=linspace(-1,1,N)
	beta=pi/Nspan
	#log-polar space
	(Nrho,Ntheta,dtheta,drho,aR,am,g)=getparameters(beta,proj[1]-proj[0],s[1]-s[0],N,Nproj)
	thsp=arange(-Ntheta/2,Ntheta/2)*dtheta
	rhosp=arange(-Nrho,0)*drho
	proj=proj-beta/2

	#compensation for cubic interpolation
	B3th=splineB3(thsp,1)
	B3th=fft.fft(fft.ifftshift(B3th))
	B3rho=splineB3(rhosp,1)
	B3rho=(fft.fft(fft.ifftshift(B3rho)))
	B3com=array(transpose(matrix(B3rho))*B3th)

	Pgl0=Pgl(Nspan,N,proj,s,thsp,rhosp,aR,beta,B3com,am,g)
	return Pgl0

def getparameters(beta,dtheta,ds,N,Nproj):
	aR=sin(beta/2)/(1+sin(beta/2))
	am=(cos(beta/2)-sin(beta/2))/(1+sin(beta/2))
	g=osg(aR,beta/2)#wrapping
	Ntheta=N
	Nrho=2*N
	dtheta=(2*beta)/Ntheta
	drho=(g-log(am))/Nrho
	return (Nrho,Ntheta,dtheta,drho,aR,am,g)

def osg(aR,theta):
	t=linspace(-pi/2,pi/2,100000)
	w=aR*cos(t)+(1-aR)+1j*aR*sin(t)
	g=max(log(abs(w))+log(cos(theta-arctan2(imag(w),real(w)))))	
	return g

def splineB3(x2,r):
	sizex=size(x2)
	x2=x2-(x2[-1]+x2[0])/2
	stepx=x2[1]-x2[0]
	ri=int32(ceil(2*r)) 

	r=r*stepx
	x2c=x2[int32(ceil((sizex+1)/2.0))-1]
	x=x2[range(int32(ceil((sizex+1)/2.0)-ri-1),int32(ceil((sizex+1)/2.0)+ri))]
	d=abs(x-x2c)/r
	B3=x*0
	for ix in range(-ri,ri+1):
		id=ix+ri
		if d[id]<1: #use the first polynomial  
			B3[id]=(3*d[id]**3-6*d[id]**2+4)/6  
		else:
			if(d[id]<2):
				B3[id]=(-d[id]**3+6*d[id]**2-12*d[id]+8)/6
	B3f=x2*0
	B3f[range(int32(ceil((sizex+1)/2.0)-ri-1),int32(ceil((sizex+1)/2.0)+ri))]=B3
	return B3f

