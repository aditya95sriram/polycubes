from typing import Set, Tuple
# from main import Point2D
import svgwrite
from svgwrite import cm, mm


scale = 100


def draw_panel(points: Set[Tuple[float, float]], fname: str):
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dwg = svgwrite.Drawing(fname, profile='tiny')
    for x, y in points:
        for offx, offy in offsets:
            if (x+offx, y+offy) not in points:
                midx, midy = x + 0.5*offx + 0.5, y + 0.5*offy + 0.5
                start = (midx + 0.5*offy, midy + 0.5*offx)
                stop = (midx - 0.5*offy, midy - 0.5*offx)
                print(list(map(lambda a: a*scale, start)), list(map(lambda a: a*scale, stop)))
                line = dwg.line(start=map(lambda a: a*scale, start),
                                end=map(lambda a: a*scale, stop),
                                stroke=svgwrite.rgb(0, 0, 0))
                dwg.add(line)
        # rect = svgwrite.shapes.Rect(insert=(x*scale, y*scale), size=(scale, scale),
        #                             rx=None, ry=None,
        #                             stroke=svgwrite.rgb(0, 0, 0), fill=svgwrite.rgb(255, 255, 255))
        # dwg.add(rect)
    dwg.save()


if __name__ == "__main__":
    draw_panel({(0, 1), (1, 0), (2, 0), (1, 1)}, 'test.svg')
