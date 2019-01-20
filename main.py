import enum
from typing import List, Union, Tuple, Dict


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

    def __add__(self, other: Union['Point', Tuple[int, int, int], list]):
        res = Point(self.x, self.y, self.z)
        if isinstance(other, Point):
            nx, ny, nz = other.x, other.y, other.z
        else:
            nx, ny, nz = other
        res.x += nx
        res.y += ny
        res.z += nz
        return res

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other):
        return (self.x, self.y, self.z) != (other.x, other.y, other.z)

    def __str__(self):
        # return "Point:({x}, {y}, {z})".format(**self.__dict__)
        return "Point({0.x}, {0.y}, {0.z})".format(self)

    def __repr__(self):
        return "Pt:({0.x}, {0.y}, {0.z})".format(self)


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
    def __init__(self):
        self.center = Point(0, 0, 0)

        panels = {d: Panel(d, self.center) for d in Dir}

        self.points = {self.center}
        self.panels = {self.center: panels}

    def add(self, point: Point):
        offsets = {Dir.XPOS: (1, 0, 0), Dir.XNEG: (-1, 0, 0),
                   Dir.YPOS: (0, 1, 0), Dir.YNEG: (0, -1, 0),
                   Dir.ZPOS: (0, 0, 1), Dir.ZNEG: (0, 0, -1)}

        self.panels[point] = dict()
        for d, offset in offsets.items():
            neighbor = point + offset
            if neighbor in self.points:
                # common_panel = self.panels[neighbor][-d]
                common_panel = self.panel_find(neighbor, -d)
                common_panel.points.remove(neighbor)
                self.panels[neighbor][-d] = None
                self.panels[point][d] = None
                self.all_panels.remove(common_panel)
            else:
                self.panels[point][d] = Panel(d, point)
                self.all_panels.append(self.panels[point][d])
                for merge_dir in Dir:
                    if merge_dir != d and merge_dir != -d:
                        co_neighbor = point + offsets[merge_dir]
                        if co_neighbor in self.points:
                            self.panel_union(point, co_neighbor, d)


if __name__ == '__main__':
    p = Polycube()
    p.add(Point(1, 0, 0))
    p.add(Point(0, 1, 0))
    for pt in p.panels:
        print(pt, p.panels[pt])
    print(p.all_panels)
    print(len(p.all_panels))
