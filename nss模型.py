import numpy as np
import matplotlib.pyplot as plt

LONG_TERM_FACTOR = 0.05
# ADJ_MID_TERM_FACTOR = -0.01
M1 = 3
M2 = 0.3


def NS_R(s, SHORT_TERM_FACTOR, MID_TERM_FACTOR):
    long_term = LONG_TERM_FACTOR
    short_term = SHORT_TERM_FACTOR * ((1 - np.e**(-s / M1)) / (s / M1))
    mid_term = MID_TERM_FACTOR * \
        ((1 - np.e**(-s / M1)) / (s / M1) - np.e**(-s / M1))
    r = long_term + short_term + mid_term
    return r


def NSS_R(s, SHORT_TERM_FACTOR, MID_TERM_FACTOR, ADJ_MID_TERM_FACTOR):
    long_term = LONG_TERM_FACTOR
    short_term = SHORT_TERM_FACTOR * ((1 - np.e**(-s / M1)) / (s / M1))
    mid_term = MID_TERM_FACTOR * \
        ((1 - np.e**(-s / M1)) / (s / M1) - np.e**(-s / M1))
    adj_mid_term = ADJ_MID_TERM_FACTOR * \
        ((1 - np.e**(-s / M2)) / (s / M2) - np.e**(-s / M2))
    r = long_term + short_term + mid_term + adj_mid_term
    return r


t = np.linspace(0.5, 30, 60)


#result_b1 = np.zeros([60,13])
# result_b2 = np.zeros([60,13])

# b1为子图变化标准
fig, axes = plt.subplots(3, 5)
for b1 in range(-6, 7):
    for b2 in range(-6, 7):
        ns_r = NS_R(t, b1 / 100, b2 / 100)
        axes[(b1 + 6) % 3][(b1 + 6) // 3].plot(t, ns_r, label='%d%%' % b2)
        axes[(b1 + 6) % 3][(b1 + 6) // 3].set_title('B1=%1d%%' % (b1))
    axes[(b1 + 6) % 3][(b1 + 6) // 3].legend(prop={'size': 6}, ncol=2)
    # axes[(b1 + 6) % 3][(b1 + 6) // 3].


# b2为子图变化标准
fig3, axes3 = plt.subplots(3, 5)
for b2 in range(-6, 7):
    for b1 in range(-6, 7):
        ns_r = NS_R(t, b1 / 100, b2 / 100)
        axes3[(b2 + 6) % 3][(b2 + 6) // 3].plot(t, ns_r, label='%d%%' % b1)
        axes3[(b2 + 6) % 3][(b2 + 6) // 3].set_title('B2=%1d%%' % (b2))
    axes3[(b2 + 6) % 3][(b2 + 6) // 3].legend(prop={'size': 6}, ncol=2)
    # axes[(b1 + 6) % 3][(b1 + 6) // 3].


# nss

# 取若干特殊值
b1_list = [-1, 0, 1]
b2_list = [-1, 0, 1]

fig2, axes2 = plt.subplots(3, 3)
for b1 in b1_list:
    for b2 in b2_list:
        for b3 in range(-6, 7):
            nss_r = NSS_R(t, b1 / 100, b2 / 100, b3 / 100)
            axes2[b1 + 1][b2 + 1].plot(t, nss_r, label='%d%%' % b3)
            axes2[b1 + 1][b2 + 1].set_title('B1=%1d%%,B2=%d%%' % (b1, b2))
        axes2[b1 + 1][b2 + 1].legend(prop={'size': 6}, ncol=2)
