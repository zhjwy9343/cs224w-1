import matplotlib.pyplot as plt
import snap

g1 = snap.LoadEdgeList(snap.PUNGraph, './data/g1.edgelist.txt', 0, 1)
g2 = snap.LoadEdgeList(snap.PUNGraph, './data/g2.edgelist.txt', 0, 1)

A, B          = 0, 1
N_DAYS        = 7
N_VOTERS      = 10 * 1000
SPEND_AMOUNTS = [i * 1000 for i in range(0, 10)]

def count_up_friends(curr_state, g, voter):
    num_A_friends = 0
    num_B_friends = 0
    for connection in g.GetNI(voter).GetInEdges():
        if curr_state[connection] == A:      num_A_friends += 1
        if curr_state[connection] == B:      num_B_friends += 1
    return num_A_friends, num_B_friends

def initialize(k, g):
    C = A

    state = (N_VOTERS / 10) * (4 * [B] + 4 * [A] + 2 * [None])
    sorted_degrees = []
    for i in range(0, N_VOTERS):    sorted_degrees += [(g.GetNI(i).GetDeg(), i)]
    sorted_degrees.sort(reverse = True)
    for x in range(0, k / 1000):    state[sorted_degrees[x][1]] = A

    return C, state

def simulation(g, label):
    results = []
    for k in SPEND_AMOUNTS:
        C, initial_state = initialize(k, g)
        curr_state       = initial_state

        for day in range(0, N_DAYS):
            for voter in range(0, N_VOTERS):
                if initial_state[voter] is None:
                    num_A_friends, num_B_friends = count_up_friends(curr_state, g, voter)
                    if   num_A_friends > num_B_friends:     curr_state[voter] = A
                    elif num_A_friends < num_B_friends:     curr_state[voter] = B
                    else:
                        curr_state[voter] = C
                        C = 1 - C

        margin   = curr_state.count(A) - curr_state.count(B)
        winner   = 'A' if margin >= 0 else 'B'
        results += [margin]

        # print 'The election winner is %s, wins by a margin of %d votes' % (winner, abs(margin))

    for k in range(0, len(results)):
        if results[k] > 0:
            print 'min required to win %s = $%s' % (label, SPEND_AMOUNTS[k])
            break
        if k == len(results) - 1:
            print 'No amount of spending will let you win %s :(' % label

    plt.plot(SPEND_AMOUNTS, results, label = label)
    # plt.show()

print '\n--- Simulation #3 -------------------------------------------------------------\n'
simulation(g1, 'G1')
simulation(g2, 'G2')
# Add horizontal line at `y (margin) = 0`, indicating the boundary between A winning and B winning.
plt.axhline(y = 0, xmin = 0, xmax = 1, linewidth = 1, color = 'grey', linestyle = 'dotted')
plt.legend()
plt.savefig('./images/3-3-simulations.png')
print