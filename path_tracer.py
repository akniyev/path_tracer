import sys

from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy

counter = 0

def pressed():
    global counter
    if (counter >= 5):
        QCoreApplication.instance().quit()
    else:
        counter += 1

groupId = -1

colors = []
parentGroups = []
groups = []
groupCenters = []

def breakIntoComponents(a):
    if (len(colors) == 0 or len(a) == 0):
        return []

    canvas = [[0 for x in range(len(colors[0]))] for y in range(len(colors))]

    for i in a:
        canvas[i[0]][i[1]] = 1

    def flood(canvas, x, y):
        if (canvas[x][y] != 1):
            return []

        component = []
        canvas[x][y] = 2
        component.append((x, y))

        while True:
            newcomp = []
            for i in component:
                xx = i[0]
                yy = i[1]
                if (canvas[xx+1][yy] == 1):
                    newcomp.append((xx+1, yy))
                    canvas[xx+1][yy] = 2

                if (canvas[xx][yy+1] == 1):
                    newcomp.append((xx, yy+1))
                    canvas[xx][yy+1] = 2

                if (canvas[xx+1][yy+1] == 1):
                    newcomp.append((xx+1, yy+1))
                    canvas[xx+1][yy+1] = 2

                if (canvas[xx-1][yy] == 1):
                    newcomp.append((xx-1, yy))
                    canvas[xx-1][yy] = 2

                if (canvas[xx+1][yy-1] == 1):
                    newcomp.append((xx+1, yy-1))
                    canvas[xx+1][yy-1] = 2

                if (canvas[xx-1][yy+1] == 1):
                    newcomp.append((xx-1, yy+1))
                    canvas[xx-1][yy+1] = 2

                if (canvas[xx-1][yy-1] == 1):
                    newcomp.append((xx-1, yy-1))
                    canvas[xx-1][yy-1] = 2

                if (canvas[xx][yy-1] == 1):
                    newcomp.append((xx, yy-1))
                    canvas[xx][yy-1] = 2

            component.extend(newcomp)
            if len(newcomp) == 0:
                return component

    result = []
    for i in a:
        r = flood(canvas, i[0], i[1])
        if r != []:
            result.append(r)
    return result

# def breakIntoComponents(a):
#     def tearOneComponent(a, component=[]):
#         if component == []:
#             component = [a[0]]
#             del a[0]
#             return tearOneComponent(a, component)
#
#         newels = []
#
#         for el in component:
#             el_tr = (el[0] + 1, el[1] - 1)
#             el_br = (el[0] + 1, el[1] + 1)
#             el_tl = (el[0] - 1, el[1] - 1)
#             el_bl = (el[0] - 1, el[1] + 1)
#
#             el_r = (el[0] + 1, el[1])
#             el_l = (el[0] - 1, el[1])
#             el_t = (el[0], el[1] - 1)
#             el_b = (el[0], el[1] + 1)
#
#             for i in [el_tr, el_br, el_tl, el_bl, el_r, el_l, el_t, el_b]:
#                 if i in a:
#                     a.remove(i)
#                     compo
#
#     if (a == []):
#         return []
#     result = []
#     current = [a[0]]
#
#     del a[0]
#
#     while a.count() > 0:
#         newa = []
#         for i in a:
#             if

def traceImage(imgPath):
    im = Image.open(imgPath)
    width = im.size[0]
    height = im.size[1]

    global colors
    global parentGroups
    global groups
    global groupCenters

    groupCenters = [(-1,-1) for x in range(10000)]

    colors = [[0 for x in range(height)] for y in range(width)]
    parentGroups = [[0 for x in range(height)] for y in range(width)]
    groups = [[0 for x in range(height)] for y in range(width)]

    def getGroupId():
        global groupId
        groupId = groupId + 1
        return groupId

    pixels = im.load()

    coords = (-1,-1)

    for x in range(width):
        for y in range(height):
            if pixels[x, y] == (0, 0, 0):
                colors[x][y] = 1
                coords = (x, y)
            else:
                colors[x][y] = 0
            parentGroups[x][y] = -1


    def f(group, groupId, depth = -1):
        if (depth > 0):
            depth -= 1
        if (depth == 0):
            return

        global colors
        global parentGroups
        global groups

        newElements = []

        for i in group:
            x = i[0]
            y = i[1]
            colors[x][y] = 3;
            if colors[x + 1][y] == 1:
                newElements.append((x + 1, y))
                colors[x + 1][y] = 2
            if colors[x - 1][y] == 1:
                newElements.append((x - 1, y))
                colors[x - 1][y] = 2
            if colors[x][y + 1] == 1:
                newElements.append((x, y + 1))
                colors[x][y + 1] = 2
            if colors[x][y - 1] == 1:
                newElements.append((x, y - 1))
                colors[x][y - 1] = 2

            if colors[x + 1][y + 1] == 1:
                newElements.append((x + 1, y + 1))
                colors[x + 1][y + 1] = 2
            if colors[x - 1][y - 1] == 1:
                newElements.append((x - 1, y - 1))
                colors[x - 1][y - 1] = 2
            if colors[x + 1][y - 1] == 1:
                newElements.append((x + 1, y - 1))
                colors[x + 1][y - 1] = 2
            if colors[x - 1][y + 1] == 1:
                newElements.append((x - 1, y + 1))
                colors[x - 1][y + 1] = 2

        components = breakIntoComponents(newElements)

        for c in components:
            gid = getGroupId()
            for el in c:
                groups[el[0]][el[1]] = gid

            avx = 0
            avy = 0
            count = 0

            for el in c:
                avx += el[0]
                avy += el[1]
                count += 1

            if (count > 0):
                avx /= count
                avy /= count

                groupCenters[gid] = (avx, avy)

            f(c, gid, depth-1)

    if coords != (-1 ,-1):
        gid = getGroupId()
        colors[coords[0]][coords[1]] = 2
        groups[coords[0]][coords[1]] = gid
        f([coords], gid)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(600, 600)

    b = QPushButton()
    b.resize(100, 20)
    b.setText("Press me!")

    b.setParent(w)
    b.clicked.connect(pressed)

    pic = QLabel(w)

    pic.setGeometry(10, 30, 255, 255)

    im = Image.open('cracks.png')

    traceImage('cracks.png')
    #
    # im_sharp = im.filter(ImageFilter.CONTOUR)
    #
    # pixmap = im_sharp.toqpixmap()
    #
    # pic.setPixmap(pixmap.scaled(pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    #
    # img = im.load()

    pixels = im.load()

    # for i in range(im.size[0]):
    #     for j in range(im.size[1]):
    #         if colors[i][j] == 0:
    #             pixels[i,j] = (255, 255, 255)
    #
    #         if colors[i][j] == 1:
    #             pixels[i,j] = (0, 0, 0)
    #
    #         if colors[i][j] == 2:
    #             pixels[i,j] = (255, 0, 0)
    #
    #         if colors[i][j] == 3:
    #             pixels[i,j] = (0, 0, 255)

    for c in groupCenters:
        if c != (-1, -1):
            pixels[c[0], c[1]] = (255, 0, 0)

    pic.setGeometry(10, 30, im.width, im.height)

    pic.setPixmap(im.toqpixmap().scaled(pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())
