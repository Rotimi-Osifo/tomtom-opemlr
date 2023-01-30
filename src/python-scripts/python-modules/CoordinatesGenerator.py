from typing import List

import Coordinate
import  ConnectedLine

class CoordinatesGenerator:
    def __init__(self, start: Coordinate, epsilon:float):
        self.__start: Coordinate = start
        self.__epsilon: float = epsilon

    def get_connected_lines(self, n_coordinates: int) -> List:
        connected_lines: List = []
        idx: int = 0

        while (idx <= n_coordinates):
            startLoc: Coordinate.Coordinate = self.__start
            end: Coordinate.Coordinate = Coordinate.Coordinate((startLoc.lat + self.__epsilon), (startLoc.lng + self.__epsilon))
            line: ConnectedLine.ConnectedLine = ConnectedLine.ConnectedLine(startLoc, end)
            connected_lines.append(line)
            idx = idx + 1

        return connected_lines
