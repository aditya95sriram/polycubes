import enum
from typing import List, Union, Tuple, Dict, Set
import networkx as nx
import matplotlib.pyplot as plt
import svg_tools
import functools
import itertools


class Dir(enum.IntEnum):
    """
    Enumeration used for convenience in denoting directions
    """
    XPOS = +1
    XNEG = -1
    YPOS = +2
    YNEG = -2
    ZPOS = +3
    ZNEG = -3

    def __repr__(self):
        return self.name


class Point(object):

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other: Union['Point', Tuple[float, float, float], list]):
        res = Point(self.x, self.y, self.z)
        if isinstance(other, Point):
            nx, ny, nz = other.x, other.y, other.z
        else:
            nx, ny, nz = other
        res.x += nx
        res.y += ny
        res.z += nz
        return res

    def __mul__(self, other: float):
        return Point(self.x * other, self.y * other, self.z * other)

    def __sub__(self, other):
        return self + other*(-1)

    def __eq__(self, other: 'Point'):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other: 'Point'):
        return (self.x, self.y, self.z) != (other.x, other.y, other.z)

    def __str__(self):
        # return "Point:({x}, {y}, {z})".format(**self.__dict__)
        return "Point({0.x}, {0.y}, {0.z})".format(self)

    def __repr__(self):
        return "Pt:({0.x}, {0.y}, {0.z})".format(self)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def midpoint(self, other: 'Point'):
        return tuple(i/2 for i in self + other)


"""
class Point2D(object):

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __iter__(self):
        yield self.x
        yield self.y
"""


class Face(object):
    """
    Object to represent a single face using a 3d point and a direction
    """
    def __init__(self, point: Point, direction: Dir):
        self.pt = point
        self.direction = direction


class Panel(object):
    """
    Object to represent panel (collection of faces)
    TODO: add validity checks (check if points coplanar + same direction)
    """
    def __init__(self, direction, *args: Point):
        self.points = set(args)
        self.direction = direction

    def add(self, point: Point):
        self.points.add(point)

    def merge(self, other: 'Panel'):
        self.points.update(other.points)

    def isempty(self):
        return len(self.points) == 0

    def __len__(self):
        return len(self.points)

    def __str__(self):
        return "Panel[Direction: {}, Points: {}]".format(self.direction, ",".join(map(str, self.points)))

    def __repr__(self):
        return "<Panel|{0.name} [{1}]>".format(self.direction, ",".join(map(repr, self.points)))


class Polycube(object):
    """
    Object to store polycube points as well as constituent faces
    """
    offsets = {Dir.XPOS: Point(1, 0, 0), Dir.XNEG: Point(-1, 0, 0),
               Dir.YPOS: Point(0, 1, 0), Dir.YNEG: Point(0, -1, 0),
               Dir.ZPOS: Point(0, 0, 1), Dir.ZNEG: Point(0, 0, -1)}

    def __init__(self):
        self.center = Point(0, 0, 0)
        self.points = {self.center}
        self.panels: Dict[Dir, Dict[float, nx.Graph]] = dict()
        for d in Dir:
            label = self.center + Polycube.offsets[d]*0.5
            self.panels[d] = {get_plane(label, d): init_graph(label)}

    def add(self, point: Point):
        self.points.add(point)
        for d, offset in Polycube.offsets.items():
            neighbor = point + offset
            face = point + offset * 0.5
            if neighbor in self.points:
                self.panels[-d][get_plane(face, -d)].remove_node(face)
            else:
                if get_plane(face, d) in self.panels[d]:
                    plane_graph = self.panels[d][get_plane(face, d)]
                    plane_graph.add_node(face)
                    for merge_dir in Dir:
                        if merge_dir != d and merge_dir != -d:
                            neighbor_label = face + Polycube.offsets[merge_dir]
                            if neighbor_label in plane_graph:
                                plane_graph.add_edge(face, neighbor_label)
                else:
                    self.panels[d][get_plane(face, d)] = init_graph(face)


def init_graph(label):
    graph = nx.Graph()
    graph.add_node(label)
    return graph


def get_plane(point: Point, direction: Dir):
    if direction == Dir.XPOS or direction == Dir.XNEG:
        return point.x
    elif direction == Dir.YPOS or direction == Dir.YNEG:
        return point.y
    else:
        return point.z


def ignore_coord(point: Point, direction: Dir):  # -> Tuple[float, float]
    ignore_dir = direction.name[0].lower()
    return tuple(getattr(point, d) for d in 'xyz' if d != ignore_dir)


if __name__ == '__main__':
    p = Polycube()
    p.add(Point(1, 0, 0))
    p.add(Point(0, 1, 0))
    p.add(Point(0, 1, 1))
    for d in p.panels:
        print("Dir:", d)
        mega = nx.Graph()
        for plane in p.panels[d]:
            print("plane:", plane)
            cur_graph = p.panels[d][plane]
            if not cur_graph:
                print("empty graph")
            else:
                # mega.add_node(p.panels[d][plane])
                mega.add_nodes_from(cur_graph.nodes())
                mega.add_edges_from(cur_graph.edges())
                ct = itertools.count(1)
                for component in nx.algorithms.connected_components(cur_graph):
                    filename = "{}-{}-{}.svg".format(d.name, str(plane).replace(".", "_"), next(ct))
                    ignore_func = functools.partial(ignore_coord, direction=d)
                    svg_tools.draw_panel(set(map(ignore_func, component)), filename)
                # nx.draw(p.panels[d][plane], with_labels=True)
                # plt.show()
                # input("press a key:")
    #print(list(nx.algorithms.connected_components(mega)))
    #nx.draw(mega, with_labels=True)
    #plt.show()
