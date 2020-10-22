import frag_pele.Analysis.Helpers.reports_to_dataframe as r2d
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse


def parse_arguments():
    """
            Parse user arguments

            Output: list with all the user arguments
        """
    # All the docstrings are very provisional and some of them are old, they would be changed in further steps!!
    parser = argparse.ArgumentParser(description="""Script to draw scatter plots from report files. """)
    required_named = parser.add_argument_group('required named arguments')
    # Growing related arguments
    required_named.add_argument("reports", nargs='+',
                                help="List of report paths.")

    parser.add_argument("-x",  default='sasaLig',
                        help="Column of the report to be used as X axis.")
    parser.add_argument("-y", default='Binding Energy',
                        help="Column of the report to be used as Y axis.")
    parser.add_argument("-c", default=None,
                        help="Single color code or array to set colorbars.")
    parser.add_argument("-z", default=None,
                        help="Column of the report to be used as Z axis (3D plot).")
    parser.add_argument("-hl", "--hline", default=None,
                        help="Draws an horizontal line parallel to X axis in the assigned Y position.")
    parser.add_argument("-vl", "--vline", default=None,
                        help="Draws a vertical line parallel to X axis in the assigned Y position.")
    parser.add_argument("-t", "--title", default=None,
                        help="Title of the plot. It it is not set it will assign a default one.")
    parser.add_argument("-xl", "--xlabel", default=None,
                        help="X label of the plot. It it is not set it will assign a default one.")
    parser.add_argument("-yl", "--ylabel", default=None,
                        help="Y label of the plot. It it is not set it will assign a default one.")

    args = parser.parse_args()

    return args.reports, args.x, args.y, args.c, args.z, args.hline, args.vline, args.title, args.xlabel, args.ylabel


def plot_scatter(report_lists, x, y, c=None, z=None, hline=None, vline=None, title=None, xlab=None, ylab=None):
    dataframe = r2d.report_to_df(report_lists)
    print(dataframe)
    if not c:
        plt.scatter(dataframe[x], dataframe[y])
    elif c and not z:
        dataframe.plot.scatter(x, y, c=c, colormap='jet')
    elif c and z:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        col = ax.scatter(xs=dataframe[x], ys=dataframe[y], zs=dataframe[z], c=dataframe[c], cmap=cm.coolwarm)
        fig.colorbar(col, shrink=0.5, aspect=5)
    if not title:
        plt.title("{} vs {}".format(x, y))
    else:
        plt.title(title)
    if not xlab:
        plt.xlabel(x)
    else:
        plt.xlabel(xlab)
    if not ylab:
        plt.ylabel(y)
    else:
        plt.ylabel(ylab)
    if vline:
        plt.axvline(x=float(vline), color='red')
    if hline:
        plt.axhline(y=float(hline), color='red')
    if title:
        plt.savefig("{}.png".format(title))
    else:
        plt.savefig("{}_{}.png".format(x, y))
    plt.show()


if __name__ == '__main__':
    reports, x, y, c, z, hline, vline, title, xlabel, ylabel = parse_arguments()
    plot_scatter(reports, x, y, c, z, hline, vline, title, xlabel, ylabel)


