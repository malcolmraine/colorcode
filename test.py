import colorcode

start = colorcode.Color(255, 255, 255)
end = colorcode.Color(0, 255, 255)
g = colorcode.gradient.Gradient(start, end, curve=colorcode.gradient.gr)

for i in range(0, 100):
    print(g.get_color(i / 100))
