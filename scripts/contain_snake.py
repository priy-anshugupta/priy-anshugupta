"""Render a bounded snake tour over Platane/snk's real contribution cells.

Only the route/presentation changes. Cell coordinates and original contribution
levels come from the upstream GitHub calendar SVG, without inventing counts.
Python stdlib only; run after Platane/snk and before publishing dist/.
"""
from html import escape
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

NS = '{http://www.w3.org/2000/svg}'


def bounded_tour(columns, rows=7):
    if rows != 7 or columns < 4:
        raise ValueError('Expected a seven-row GitHub calendar with at least four columns')
    even_columns = columns if columns % 2 == 0 else columns - 1
    route = [(x, 0) for x in range(even_columns)]
    route += [(even_columns - 1, y) for y in range(1, rows)]
    for x in range(even_columns - 2, -1, -1):
        route += [(x, y) for y in (range(rows - 1, 0, -1) if x % 2 == 0 else range(1, rows))]
    if columns % 2:
        # Extend the even-width circuit into the final column. The final square
        # uses a four-step loop to cover the odd corner without reversing into
        # the snake's body. Revisited nodes are at least four moves apart.
        expanded = []
        x = even_columns - 1
        for point in route:
            expanded.append(point)
            if point[0] == x and point[1] in (0, 2):
                y = point[1]
                expanded += [(x + 1, y), (x + 1, y + 1)]
            elif point == (x, 4):
                expanded += [(x + 1, 4), (x + 1, 5), (x + 1, 6),
                             (x, 6), (x, 5), (x + 1, 5), (x + 1, 4), (x, 4)]
        route = expanded
    validate_tour(route, columns, rows)
    return route


def validate_tour(route, columns, rows):
    assert set(route) == {(x, y) for x in range(columns) for y in range(rows)}, 'Calendar coverage'
    for i, (x, y) in enumerate(route):
        assert 0 <= x < columns and 0 <= y < rows, 'Out-of-grid route'
        prev = route[(i - 1) % len(route)]
        assert abs(x - prev[0]) + abs(y - prev[1]) == 1, 'Non-adjacent step'
        assert (x, y) not in [route[(i - d) % len(route)] for d in range(1, 4)], 'Body collision'


def render(raw, dark):
    original = ET.fromstring(raw)
    style = original.find(NS + 'style').text
    cells = [node for node in original.findall(NS + 'rect') if node.get('class', '').split()[:1] == ['c']]
    if not cells:
        raise ValueError('No upstream contribution cells')
    # Upstream cell classes preserve the original calendar colour level.
    levels = {}
    for node in cells:
        classes = node.get('class').split()
        if len(classes) == 1:
            level = 0
        else:
            match = re.search(r'\.c\.' + re.escape(classes[1]) + r'\{fill:var\(--c(\d)\)', style)
            if not match:
                raise ValueError('Unrecognised upstream contribution level')
            level = int(match.group(1))
        x = round((float(node.get('x')) - 2) / 16)
        y = round((float(node.get('y')) - 2) / 16)
        levels[(x, y)] = level
    columns = max(x for x, y in levels) + 1
    route = bounded_tour(columns)
    steps = len(route)
    duration = round(steps * .085, 3)
    grid_width = columns * 16
    width = grid_width + 32
    palette = (['#202b38', '#245b4a', '#32836a', '#55b794', '#8be0ba'] if dark else
               ['#e1e6e3', '#bbdeca', '#78ba98', '#3b956c', '#206647'])
    border = '#354556' if dark else '#c3d0c8'
    snake = '#ffb185' if dark else '#c4512f'
    first_visit = {}
    for i, point in enumerate(route):
        first_visit.setdefault(point, i / steps * 100)
    rules = [f'.cell{{width:12px;height:12px;stroke:{border};stroke-width:.65px}}',
             f'.body{{fill:{snake};stroke:{"#17212c" if dark else "#ffffff"};stroke-width:.6px}}']
    shapes = []
    for i, ((x, y), level) in enumerate(sorted(levels.items())):
        if level:
            hit = max(.02, first_visit[(x, y)])
            rules.append(f'@keyframes cell{i}'+'{'+f'0%,{max(0,hit-.01):.4f}%'+f'{{fill:{palette[level]}}}'
                         +f'{hit:.4f}%,100%'+f'{{fill:{palette[0]}}}'+'}'
                         f'.cell{i}{{fill:{palette[level]};animation:cell{i} {duration}s linear infinite}}')
        shapes.append(f'<rect class="cell cell{i}" x="{16*x+2}" y="{16*y+2}" rx="2" fill="{palette[level]}"/>')
    for segment in range(3, -1, -1):
        positions = [route[(i - segment) % steps] for i in range(steps)]
        frames = ''.join(f'{i/steps*100:.5f}%{{transform:translate({16*x}px,{16*y}px)}}' for i,(x,y) in enumerate(positions))
        x0,y0 = positions[0]
        frames += f'100%{{transform:translate({16*x0}px,{16*y0}px)}}'
        rules.append(f'@keyframes snake{segment}{{{frames}}}.snake{segment}{{transform:translate({16*x0}px,{16*y0}px);animation:snake{segment} {duration}s linear infinite}}')
        size = 12 if segment == 0 else 10.5 - segment*.8
        offset = (16 - size)/2
        shapes.append(f'<g class="snake{segment}"><rect class="body" x="{offset}" y="{offset}" width="{size}" height="{size}" rx="3"/></g>')
    rules.append('@media(prefers-reduced-motion:reduce){rect,g{animation:none!important}}')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="136" viewBox="-16 -12 {width} 136" role="img">'
            '<title>GitHub contributions — snake contained inside the calendar</title>'
            f'<desc>{len(cells)} actual GitHub contribution cells. Original intensity levels retained. Four-segment snake follows a bounded route with no body collisions.</desc>'
            '<style>'+''.join(rules)+'</style>'+''.join(shapes)+'</svg>')


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
    for file in target.glob('github-contribution-grid-snake*.svg'):
        raw = file.read_text(encoding='utf-8')
        if 'Generated with https://github.com/Platane/snk' not in raw:
            raise ValueError('Expected the original Platane/snk SVG as input')
        file.write_text(render(raw, 'dark' in file.stem), encoding='utf-8')
        print('Rendered contained snake:', file.name)


if __name__ == '__main__':
    main()
