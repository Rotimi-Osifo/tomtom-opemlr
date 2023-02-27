import pygeos
from pygeos import frechet_distance


class similarity_analysis:

    def __init__(self):
        self.similarity = None

    def convert_to_ln_str(self, coordinates):
        start = 'LINESTRING('
        end = ')'
        p_str = ''
        s = len(coordinates)
        cnt = 1
        for point in coordinates:
            if cnt < s:
                p_str = p_str + str(float(point[0])) + ' ' + str(float(point[1])) + ', '
            else:
                p_str = p_str + str(float(point[0])) + ' ' + str(float(point[1]))
            cnt = cnt + 1
        lstr = start + p_str + end
        return lstr

    def compute_similarity(self, first, second):
        #Not that this reutrns values in degrees since coordinate conversion has not been done
        first_as_linestring = pygeos.Geometry(self.convert_to_ln_str(first))
        second_as_linestring = pygeos.Geometry(self.convert_to_ln_str(second))
        fd =frechet_distance(first_as_linestring, second_as_linestring, densify=0.5)
        return fd

