import random

from entities.problem_data import ProblemData

# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt


class PlotQueuePerspective:
    def __init__(self, problem_data: ProblemData):
        self.problem_data = problem_data

    def plot_gnt(self, out_dir: str):
        colors = color_map(len(self.problem_data.users))
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        fig.suptitle(f"Scenario: {self.problem_data.scenario_name} [Provider Perspective] ({'{:.2f}'.format(self.problem_data.solution_time)} s)", fontsize=14)

        # Setting Y-axis limits
        gnt.set_ylim(0, len(self.problem_data.queues) * 10)

        # Setting X-axis limits
        gnt.set_xlim(0, 19 * 60)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Service')

        # Setting ticks on y-axis
        gnt.set_yticks([10 * queue.index + 10 for queue in self.problem_data.queues])
        # Labelling tickes of y-axis
        gnt.set_yticklabels([queue.index for queue in self.problem_data.queues])

        # Setting graph attribute
        gnt.grid(True)

        for queue in self.problem_data.queues:
            for request in queue.requests:
                gnt.broken_barh([(request.optimal_visiting_time, request.visiting_duration)],
                                (10 * queue.index, 9),
                                facecolors=(colors[request.user_index]))

        plt.savefig(f"{out_dir}/queue_perspective.png")


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def color_map(size: int):
    colors = []
    for i in range(size):
        random_color = random.choices(range(256), k=3)
        colors.append(rgb_to_hex(random_color[0], random_color[1], random_color[2]))

    return colors
