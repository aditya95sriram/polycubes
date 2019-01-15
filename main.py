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


class Polycube(object):
    """
    Object to store polycube points as well as constituent faces
    """
    def __init__(self):
        self.center = Point(0, 0, 0)
        # faces = {d: Face(self.center, d) for d in Dir}
        # panels = {d: Panel(face) for d, face in faces.items()}

        panels = {d: Panel(d, self.center) for d in Dir}

        self.points = {self.center}
        # self.panels = {self.center: [[face] for face in faces]}
        # self.panels = {self.center: [Panel(face) for face in faces]}
        self.panels = {self.center: panels}

    def add(self, point: Point):
        offsets = {Dir.XPOS: (1, 0, 0), Dir.XNEG: (-1, 0, 0),
                   Dir.YPOS: (0, 1, 0), Dir.YNEG: (0, -1, 0),
                   Dir.ZPOS: (0, 0, 1), Dir.ZNEG: (0, 0, -1)}

        self.panels[point] = dict()
        new_panels = dict()
        neighbors = {}
        for d, offset in offsets.items():
            neighbor = point + offset
            if neighbor in self.points:
                common_panel = self.panels[neighbor][-d]
                common_panel.points.remove(neighbor)
                self.panels[point][d] = common_panel
            else:
                possible_mergers = []
                for merge_dir in Dir:
                    if merge_dir != d and merge_dir != -d:
                        if point + offsets[merge_dir] in self.points:
                            possible_mergers.append(point + offsets[merge_dir])


        for d, n in neighbors.items():
            facing = -d
            p = self.panels[n][facing]
            p.points.remove(n)  # delete common face
            self.panels[point][d] = p


        p = Panel(Dir.XPOS)
        p = None





