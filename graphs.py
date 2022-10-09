import data
import constants

from utils import extract_keys
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt


# TODO: Implement a function to recreate figure 1
def wins_graphs():
    pass


# TODO: Implement a function to recreate figure 2
def feature_graphs():
    pass


def rel_kword_graphs(get_data, min_score, num_of_rounds, y_ticks, y_label):

    """
    rel_kword_graphs is the function used to plot the relevance and keyword graphs
    :param get_data: a function to get a relevance/keyword data structure
    :type get_data: func
    :param min_score: the minimum possible score for relevance/keywords
    :type min_score: int
    :param num_of_rounds: the number of rounds in the competition
    :type num_of_rounds: int
    :param y_ticks: the ticks to be plotted on the y axis
    :type y_ticks: list
    :param y_label: the label to put on the y axis
    :type y_label: str
    :return: NULL
    """

    scores = get_data()
    round_counter = defaultdict(lambda: defaultdict(int))

    # Count score per round
    for key in scores:
        _, round, _ = extract_keys(key)
        if round != 0:
            if scores[key] != 0:
                # At least x = x to min x (min_score)
                for i in range(int(scores[key]), min_score - 1, -1):
                    round_counter[round][i] += 1

    # Normalize the scores and sort them for plotting
    graph_score = defaultdict(list)
    for round in round_counter:
        for score in [1, 2, 3]:
            graph_score[round].append(round_counter[round][score] / 156)
    graph_score = OrderedDict(sorted(graph_score.items()))

    # Plot the scores
    plt.plot(range(1, num_of_rounds + 1), [graph_score[round][0] * 100 for round in graph_score if round != '00'],
             color='k', marker='+')
    plt.plot(range(1, num_of_rounds + 1), [graph_score[round][1] * 100 for round in graph_score if round != '00'],
             color='tab:orange', marker='v')
    plt.plot(range(1, num_of_rounds + 1), [graph_score[round][2] * 100 for round in graph_score if round != '00'],
             color='b', marker='^')
    plt.yticks(y_ticks)
    plt.ylabel(y_label)
    plt.xlabel("round")
    plt.show()


# TODO: Implement a function to recreate figure 4
def metrics_graphs():
    pass


def main():
    # TODO: Fill missing function arguments
    wins_graphs()
    feature_graphs()
    rel_kword_graphs(data.get_keywords, constants.MIN_KEYWORD_SCORE, constants.NUM_OF_ROUNDS, [0, 4, 8, 12], "% of keyword stuffed documents")
    rel_kword_graphs(data.get_relevance, constants.MIN_RELEVANCE_SCORE, constants.NUM_OF_ROUNDS, [25, 50, 75, 100], "% of relevant documents")
    metrics_graphs()


if __name__ == "__main__":
    main()
