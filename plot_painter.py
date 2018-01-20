"""Module drawing plot from given source files."""
import sys
import json
import matplotlib.pyplot as pl

def main():
    """Plot painter entry point."""
    if len(sys.argv) < 2:
        print("At least one input file have to be specified!")
        return

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    styles = ['-', '--', '-.', ':']
    color = 0
    style = 0

    for i in range(1, len(sys.argv)):
        file = sys.argv[i]
        try:
            data_json = json.load(open(file, 'r'))
            for s in data_json.keys():
                values = []
                for value in data_json[s]:
                    values.append([value["X"], value["Y"]])
                values.sort(key=lambda val: val[0])
                pl.plot([value_xy[0] for value_xy in values], [value_xy[1] for value_xy in values], colors[color] + styles[style], label=s)
                color += 1
                if color >= len(colors):
                    style += 1
                    color = 0
                if style >= len(styles):
                    print("Too many plots!")
                    return
        except FileNotFoundError:
            print("Cannot open {} file!".format(file))
            return

    pl.title("Algorithms comparison")
    pl.legend()
    pl.xlabel("Evaluations")
    pl.ylabel("Average goal function")
    pl.show()

if __name__ == "__main__":
    main()
