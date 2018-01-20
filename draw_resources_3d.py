import json

import numpy as np
import sys
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from evaluator import Evaluator
from location import Location2D
from resource import ResourceRequirement, Resource


def draw_3d_plot(resources):
    evaluator = Evaluator(resources)
    x_coords = range(100)
    y_coords = range(100)
    z_coords = [evaluator.evaluate(Location2D(x, y)) for x in x_coords for y in y_coords]
    fig = pyplot.figure()
    ax = Axes3D(fig)

    max_sc = min([(evaluator.evaluate(Location2D(x, y)), x, y) for x in x_coords for y in y_coords])
    print("[{}] ({}, {})".format(max_sc[0], max_sc[1], max_sc[2]))

    X, Y = np.meshgrid(x_coords, y_coords)
    array = np.array(z_coords)
    Z = np.reshape(array, (100, 100))
    # ax.set_zlim3d(top=1000, bottom=600)
    # ax.view_init(azim=20., elev=45.)
    # ax.view_init(azim=0., elev=90.)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel("X", fontsize=20)
    ax.set_ylabel("Y", fontsize=20)
    ax.set_zlabel("cost", rotation=90, fontsize=20)
    pyplot.show()


def main():
    resources = []
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'Out.json'
    try:
        resources_json = json.load(open(file_name, 'r'))
        for res in resources_json["Resources"]:
            func_dict = dict()
            exec(res["Transport_cost_func"], func_dict)
            resources.append(
                ResourceRequirement(Resource(Location2D(res["Position"][0], res["Position"][1]), func_dict["f"]),
                                    res["Required_units"]))
    except FileNotFoundError:
        print("Cannot open file!")
    else:
        draw_3d_plot(resources)


if __name__ == "__main__":
    main()
