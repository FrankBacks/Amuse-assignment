import matplotlib.pyplot as plt
from main import *

def make_plots():

    positions_hot = main_function(end_time=4.e7 | units.yr, Q=0.5, D=2.6, animate=False, number_of_stars=1000)[0][-1]
    positions_cool = main_function(end_time=4.e7 | units.yr, Q=0.3, D=1.6, animate=False, number_of_stars=1000)[0][-1]

    f, axarr = plt.subplots(2,2, figsize=(6,6))

    axarr[0][0].scatter(positions_hot[:,0].in_(units.parsec).number, positions_hot[:,1].in_(units.parsec).number, s=1, c="black")
    axarr[0][0].set_xlim([-2.5, 2.5])
    axarr[0][0].set_ylim([-2.5, 2.5])
    axarr[0][0].set_xlabel("x (pc)")
    axarr[0][0].set_ylabel("y (pc)")

    axarr[0][1].scatter(positions_hot[:,0].in_(units.parsec).number, positions_hot[:,1].in_(units.parsec).number, s=1, c="black")
    axarr[0][1].set_xlim([-20, 20])
    axarr[0][1].set_ylim([-20, 20])
    axarr[0][1].set_xlabel("x (pc)")
    axarr[0][1].set_ylabel("y (pc)")

    axarr[1][0].scatter(positions_cool[:,0].in_(units.parsec).number, positions_cool[:,1].in_(units.parsec).number, s=1, c="black")
    axarr[1][0].set_xlim([-2.5, 2.5])
    axarr[1][0].set_ylim([-2.5, 2.5])
    axarr[1][0].set_xlabel("x (pc)")
    axarr[1][0].set_ylabel("y (pc)")

    axarr[1][1].scatter(positions_cool[:,0].in_(units.parsec).number, positions_cool[:,1].in_(units.parsec).number, s=1, c="black")
    axarr[1][1].set_xlim([-20, 20])
    axarr[1][1].set_ylim([-20, 20])
    axarr[1][1].set_xlabel("x (pc)")
    axarr[1][1].set_ylabel("y (pc)")
    plt.tight_layout()
    plt.show()

make_plots()