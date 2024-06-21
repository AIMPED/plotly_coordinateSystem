import plotly.graph_objects as go
import numpy as np


class CoordinateSystem:
    # define axis colors
    axs_color = {
        1: 'red',
        2: 'green',
        3: 'blue'
    }

    def __init__(self, points_coordinates):
        self.points_coordinates = points_coordinates
        self.points = self.__check_input(points_coordinates)
        self.origin, self.vectors = self.__create_system()
        self.traces = self.__plot()
        self.X = self.vectors[:, 0]
        self.Y = self.vectors[:, 1]
        self.Z = self.vectors[:, 2]

    @staticmethod
    def __check_input(to_check):
        # check if input is of type list and convert into np.ndarray
        if isinstance(to_check, list):
            to_check = np.asarray(to_check)

        # convert dtype into float
        to_check = to_check.astype(float)
        return to_check

    def __create_system(self):
        """
        function calculates a coordinate system defined by three points

        Returns:
            tuple, coordinates of origin and vectors of axis system
        """
        origin = self.points[0, :]
        point1 = self.points[1, :]
        point2 = self.points[2, :]

        # calculate x-vector and amount
        x = point1 - origin
        x_am = np.linalg.norm(x, axis=0)
        if x_am != 0:
            x /= x_am

        # calculate z-vector and amount
        z = np.cross(x, (point2 - origin))
        z_am = np.linalg.norm(z, axis=0)
        if z_am != 0:
            z /= z_am

        # calculate y-vector
        y = np.cross(z, x)

        # axis=0 --> xyz columns, vectors row
        return origin, np.stack([x, y, z], axis=0)

    def __plot(self):
        """
        function creates a coordinate system representation with plotly graph_objects.
        Each axis is stored in a separate trace.

        Returns:
            plotly.graph_objects traces
        """
        # define scaling factor for axis scaling (visibility on coordinate system)
        scaling_factor = 1  #self.points.max() / 10

        # create four points for displaying the coordinate system
        four_points = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]) * scaling_factor

        # convert points into coordinate system
        converted_points = np.dot(four_points, self.vectors)

        # move points into coordinate system origin
        converted_points = converted_points + self.origin

        # create traces for input points and axes
        traces = [
            go.Scatter3d(
                x=converted_points[:, 0],
                y=converted_points[:, 1],
                z=converted_points[:, 2],
                mode='markers',
                marker={'size': [10, 0, 0, 0], 'symbol': 'circle-open', 'color': 'black'},
                name='points-axis',
                showlegend=False
            )
        ]

        for axis, axis_name in enumerate(['x-axis', 'y-axis', 'z-axis'], start=1):
            traces.append(
                go.Scatter3d(
                    x=converted_points[[0, axis], 0],
                    y=converted_points[[0, axis], 1],
                    z=converted_points[[0, axis], 2],
                    mode='lines+markers',
                    marker={
                        'size': [0, 6],
                        'symbol': 'circle',
                        'color': self.axs_color[axis],
                        'line': {'color': self.axs_color[axis]}
                    },
                    name=axis_name
                )
            )
        return traces
