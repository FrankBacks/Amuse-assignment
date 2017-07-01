import numpy as np
import matplotlib.pyplot as plt

masses_hot = np.loadtxt("escape_masses_hot")
masses_cool = np.loadtxt("escape_masses_cool")
velocities_hot = np.loadtxt("escape_velocities_hot")
velocities_cool = np.loadtxt("escape_velocities_cool")
escaped_stars_hot = np.loadtxt("number_of_escaped_stars_hot_2d_3d")
escaped_stars_cool = np.loadtxt("number_of_escaped_stars_cool_2d_3d")

print ("The number of escaping stars for cool and structured: %.4g stars with a standard deviation of %.4g"
       % (np.mean(escaped_stars_cool), np.std(escaped_stars_cool)))
print ("The number of escaping stars for virialized and unstructured: %.4g stars with a standard deviation of %.4g"
       % (np.mean(escaped_stars_hot), np.std(escaped_stars_hot)))

print len(masses_cool)
print len(masses_hot)


counts, bins = np.histogram(masses_hot / 2.e30, bins=500, range=(0,2), normed=True)
cdf = np.cumsum(counts) / np.sum(counts)

plt.plot(np.vstack((bins, np.roll(bins, -1))).T.flatten()[:-2],
         np.vstack((cdf, cdf)).T.flatten(),
         label="Q=0.5, D=2.6",
         color="green")

counts, bins = np.histogram(masses_cool / 2.e30, bins=500, range=(0,2), normed=True)
cdf = np.cumsum(counts) / np.sum(counts)

plt.plot(np.vstack((bins, np.roll(bins, -1))).T.flatten()[:-2],
         np.vstack((cdf, cdf)).T.flatten(),
         label="Q=0.3, D=1.6",
         color="red")

# plt.hist(masses_hot / 2.e30, histtype="step", color="green", bins=20, normed=True, label="Q=0.5, D=2.6", cumulative=1)
# plt.hist(masses_cool / 2.e30, histtype="step", color="red", bins=20, normed=True, label="Q=0.3, D=1.6", cumulative=1)
plt.xlabel("Mass ($M_{\odot}$)")
plt.ylabel("Fractional number of the ejected stars")
plt.legend()
plt.show()

counts, bins = np.histogram(velocities_hot / 1000, bins=500, range=(0,2), normed=True)
cdf = np.cumsum(counts) / np.sum(counts)

plt.plot(np.vstack((bins, np.roll(bins, -1))).T.flatten()[:-2],
         np.vstack((cdf, cdf)).T.flatten(),
         label="Q=0.5, D=2.6",
         color="green")

counts, bins = np.histogram(velocities_cool / 1000, bins=500, range=(0,2), normed=True)
cdf = np.cumsum(counts) / np.sum(counts)

plt.plot(np.vstack((bins, np.roll(bins, -1))).T.flatten()[:-2],
         np.vstack((cdf, cdf)).T.flatten(),
         label="Q=0.3, D=1.6",
         color="red")


# plt.hist(velocities_hot / 1000., histtype="step", color="green", bins=20, normed=True, label="Q=0.5, D=2.6", cumulative=1)
# plt.hist(velocities_cool / 1000., histtype="step", color="red", bins=20, normed=True, label="Q=0.3, D=1.6", cumulative=1)
plt.xlabel("Velocity (km s$^{-1}$)")
plt.ylabel("Fractional number of the ejected stars")
plt.legend()
plt.show()


