# plotly_coordinateSystem
coordinate system class. Includes plotting using plotly

example usage:

```python
    points_1 = [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
    points_2 = [[2, 2, 0], [3, 3, 0], [3, 1, 0]]

    csys_1 = CoordinateSystem(points_coordinates=points_1)
    csys_2 = CoordinateSystem(points_coordinates=points_2)

    fig = go.Figure(csys_1.traces + csys_2.traces )
    fig.show()
```
