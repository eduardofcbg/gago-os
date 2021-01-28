import cairo

with cairo.SVGSurface("example.svg", 500, 300) as surface:
    context = cairo.Context(surface)

    context.rectangle(0, 200, 100, 100)
    context.set_source_rgb(0.3, 0.2, 0.5)
    context.fill()

    x, y, x1, y1 = 0.1, 0.5, 0.4, 0.9
    x2, y2, x3, y3 = 0.6, 0.1, 0.9, 0.5
    # context.scale(300, 200)
    # context.set_line_width(0.04)
    # context.move_to(x, y)
    # context.curve_to(x1, y1, x2, y2, x3, y3)
    # context.stroke()
    # context.set_source_rgba(1, 0.2, 0.2, 0.6)
    # context.set_line_width(0.04)
    # context.move_to(x, y)
    # context.line_to(x1, y1)
    # context.move_to(x2, y2)
    # context.line_to(x3, y3)
    # context.stroke()

    surface.write_to_png("example.png")
