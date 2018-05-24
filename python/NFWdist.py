import numpy as np
from scipy import special

r"""  The Standard Distribution Functions for the 3D NFW Profile

      Density, distribution function, quantile function and random generation for the 3D NFW profile

      Usage:
      dnfw(x, con = 5, log = FALSE)
      pnfw(q, con = 5, logp = FALSE)
      qnfw(p, con = 5, logp = FALSE)
      rnfw(n, con = 5)

      dnfw gives the density, pnfw gives the distribution function, qnfw gives the quantile function, and rnfw generates random deviates.

      Arguments:
        x, q: array_like
          Vector of quantiles. This is scaled such that x=R/Rvir for NFW. This means the PDF is only defined between 0 and 1.

        p: array_like
          Vector of probabilities

        n: array_like
          Number of observations. If n has the attribute 'len()', i.e., is not a scalar, the length is taken to be the number required.

        con: scalar, optional
          The NFW profile concentration parameter, where c=Rvir/Rs.

        log, logp: logical, optional
          if True, probabilities/densities p are returned as log(p).

      Examples:
        see test.py

      Notes:
        The novel part of this package is the general solution for the CDF inversion (i.e. qnfw). 
        As far as we can see this has not been published anywhere, and it is a useful function for populating halos in something like an HOD.
        This seems to work at least as efficiently as accept/reject, but it is ultimately much more elegant code in any case.

      Authors:
        Cullan Howlett
"""

def pnfwunorm(q, con=5):
  return np.log(1.0 + q*con)-(con*q)/(1.0 + con*q)

def dnfw(x, con=5, log=False):
  if (log):
    d = np.log(con**2*x/((con*x+1.0)**2*(1.0/(con+1.0)+np.log(con+1.0)-1.0)))
  else:
    d = con**2*x/((con*x+1.0)**2*(1.0/(con+1.0)+np.log(con+1.0)-1.0))
  if hasattr(x, '__len__'):
    d[x>1]=0
  else:
    if (x > 1):
      d = 0
  return d

def pnfw(q, con=5, logp=False):
  if(logp):
    p = np.log(pnfwunorm(q, con=con)/pnfwunorm(1, con=con))
  else:
    p = pnfwunorm(q, con=con)/pnfwunorm(1, con=con)
  return p

def qnfw(p, con=5, logp=False):
  if (logp):
    p = np.exp(p)
  p *= pnfwunorm(1, con=con)
  return (-(1.0/np.real(special.lambertw(-np.exp(-p-1))))-1)/con

def rnfw(n, con=5):
  if hasattr(n, '__len__'):
    n=len(n)
  return qnfw(np.random.rand(int(n)), con=con)