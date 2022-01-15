import os


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


WIDTH_DEC_ORDER = False
HEIGHT_DEC_ORDER = True
AREA_DEC_ORDER = False


with cd("./instancesTxt"):
    for i in range(1, 41):
        file_name = "ins-{}.txt".format(i)
        f = open(file_name, "r")

        # First param is max_width
        max_width = "max_width = " + f.readline().rstrip("\n")
        # Second is number of block n_blocks
        n_blocks = "n_blocks = " + f.readline().rstrip("\n")
        # The last elements are the dimensions of the blocks
        dims = [[int(xi) for xi in x.split()] for x in f]
        # widths = "width = " + str([el[0] for el in dims])
        # heights = "height = " + str(str([el[1] for el in dims]))

        blocks = [(w, h) for w, h in zip([el[0] for el in dims], [el[1] for el in dims])]
        if WIDTH_DEC_ORDER:
            blocks.sort(key=lambda x: (x[1], x[0],), reverse=True)
        elif HEIGHT_DEC_ORDER:
            blocks.sort(key=lambda x: (x[0], x[1],), reverse=True)
        elif AREA_DEC_ORDER:
            blocks.sort(key=lambda x: x[0] * x[1], reverse=True)
        widths = "width = " + str([x[0] for x in blocks])
        heights = "height = " + str([x[1] for x in blocks])

        f.close()

        dir_name = "instancesDzn"
        if WIDTH_DEC_ORDER:
            dir_name += "W"
        elif HEIGHT_DEC_ORDER:
            dir_name += "H"
        elif AREA_DEC_ORDER:
            dir_name += "A"

        with cd("../" + dir_name):
            file_name = "ins-{}".format(i)
            ft = open(file_name + '.dzn', "w")
            ft.write(max_width + ';\n' + n_blocks + ';\n' + widths + ';\n' + heights + ';\n')
            ft.close()
