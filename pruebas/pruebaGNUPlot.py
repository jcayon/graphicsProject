#! /usr/bin/env python

import Gnuplot

from numpy import *

a = [[1,2],[3,4],[5,6]]
gp = Gnuplot.Gnuplot()
gp.plot(a)
gp.hardcopy("prueba1.svg", terminal='svg', size=[800,400])


a = [[1,2],[3,4],[5,6]]
gp = Gnuplot.Gnuplot()
gp("set style data lines")
gp.plot(a)
gp.hardcopy("prueba2.svg", terminal='svg', size=[800,400])

