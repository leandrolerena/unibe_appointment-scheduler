import random

from entities.problem_data import ProblemData

# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt


class PlotUserPerspective:
    def __init__(self, problem_data: ProblemData):
        self.problem_data = problem_data

    def plot_gnt(self):
        colors = color_map(len(self.problem_data.queues))
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, len(self.problem_data.users) * 10)

        # Setting X-axis limits
        gnt.set_xlim(0, 19 * 60)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('User')

        # Setting ticks on y-axis
        gnt.set_yticks([10 * user.index + 10 for user in self.problem_data.users])
        # Labelling tickes of y-axis
        gnt.set_yticklabels([user.index for user in self.problem_data.users])

        # Setting graph attribute
        gnt.grid(True)

        for user in self.problem_data.users:
            for request in user.requests:
                gnt.broken_barh([(request.optimal_visiting_time, request.visiting_duration)],
                                (10 * user.index, 9),
                                facecolors=(colors[request.queue_index]))

        plt.savefig("user_perspective.png")


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def color_map(size: int):
    colors = []
    for i in range(size):
        random_color = random.choices(range(256), k=3)
        colors.append(rgb_to_hex(random_color[0], random_color[1], random_color[2]))

    return colors