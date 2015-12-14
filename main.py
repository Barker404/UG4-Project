import showing
import sharing
from output import plot_simulations
from simulation import Simulation

ROWS = 20
COLUMNS = 20
K = 1
Q = 2

ROUND_COUNT = 20
MESSAGE_COUNT = 100

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


def main():
    show_model = showing.OnlyBestShowModel(20)
    share_model = sharing.BasicShareModel(5)

    sims = []
    x_vals = []

    for i in range(1, 7):
        message_count = 250 * i
        simulation = Simulation(show_model, share_model,
                                ROWS, COLUMNS, K, Q,
                                ROUND_COUNT, message_count)
        sims.append(simulation)
        x_vals.append(message_count)

    plot_simulations(sims, x_vals, 'message count', 1)

if __name__ == "__main__":
    main()
