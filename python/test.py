from NFWdist import *

# Just a quick main routine to test things
def main():

  # These libraries are only required for testing
  import time
  import numpy as np
  import matplotlib.pyplot as plt
  from scipy import integrate

  #Both the PDF (dnfw) integrated up to x, and CDF at q should be the same:
  print "Checking CDF and integral of PDF, should be the same:"
  for con in [1,5,10,20]:
    print str(r'con = %d: ' % con), integrate.quad(dnfw, 0, 0.5, args=(con))[0], pnfw(0.5, con=con)

  #Both the qnfw should be the inverse of pnfw
  print "Checking qnfw inverts pnfw, should return input vector [1:9]/10"
  con = [1, 5, 10, 20]
  prob = pnfw(np.arange(1,10)/10.0,con=con)
  for i, j in enumerate(con):
    print "con = ", j, ":", qnfw(prob[0:,i], con=j)

  # First some simple timing tests
  print "Timing tests in seconds"
  print "Average of 1000 iterations of nsamples=10,000:"
  start = time.time()
  for i in range(1000):
    np.random.randn(10000)
  print "Uniform: ", (time.time()-start)/1000.0

  for con in [1,5,10,20]:
    start = time.time()
    for i in range(1000):
      rnfw(1e4,con=con)
    print str(r'con = %d: ' % con), (time.time()-start)/1000.0


  # Some plots of the analytic and randomly-drawn NFW PDF
  print "Plotting random draws against PDF for nsamples=100,000:"
  nsamples = 1e6
  for con in [1,5,10,20]:

      hist = np.histogram(rnfw(nsamples,con=con), bins=100, density=True)

      fig = plt.figure(con)
      ax1=fig.add_axes([0.13,0.13,0.82,0.82])
      ax1.plot(hist[1][1:], hist[0], color='k', linewidth=1.5, ls='steps')
      ax1.plot(np.linspace(0,1,1e3), dnfw(np.linspace(0,1,1e3),con=con), color='r', ls='-')
      ax1.set_xlabel(r'$q$', fontsize=16)
      ax1.set_ylabel(r'$\rho(q)$', fontsize=16)
      ax1.text(0.8, 0.8, str(r'con = %d' % con), transform=ax1.transAxes, fontsize='16')

  plt.show()

if __name__ == "__main__":
  main()