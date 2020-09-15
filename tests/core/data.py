import pyobs
import numpy

pyobs.set_verbose('data.axpy')

mu=[3.14, 6.14]
cov=numpy.array([[0.01, 0.002], [0.002,0.02]])**2
N=500
tau=0.0

data = pyobs.random.acrandn(mu,cov,tau,N)
mask = [True]*N
mask[1] = False
mask[-1] = False

obsA = pyobs.obs()
obsA.create('test',data[:,0][mask],icnfg=[0]+list(range(2,N-1)))
print(obsA)
[a, da] = obsA.error()

obsB = pyobs.obs()
obsB.create('test',data[:,1],icnfg=range(0,N))
[b, db] = obsB.error()

obsC = obsB/(2.0*obsA)
[c, dc] = obsC.error()
ddc = obsC.error_of_error()

cov = numpy.array(cov)
g = numpy.array([-b/(2.0*a*a), 1/(2.0*a)])
err = numpy.sqrt((g.T @ cov @ g)/N)

assert abs(err-dc) < ddc
