import numpy as np

# Fungsi quicksort yang diubah sedikit algoritma dari quicksort biasa agar lebih efisien


def quicksort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    pivot = key(arr[0])
    left = [x for x in arr[1:] if key(x) <= pivot]
    right = [x for x in arr[1:] if key(x) >= pivot]
    return quicksort(left, key) + [arr[0]] + quicksort(right, key)

# Fungsi untuk mencari jarak antar 2 point


def get_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Predikat untuk menentukan apakah point di atas atau dibawah garis yang dibentuk ref1,ref2
# Ref1[0] selalu lebih kecil daripada Ref2[0]


def isAboveOrBelow(ref1, ref2, point):
    # Jika garis referensi perfectly vertical
    if (ref1[0] - ref2[0] == 0):
        if (point[0] < ref1[0]):
            return "Above"
        elif (point[0] > ref1[0]):
            return "Below"
        else:
            return "On"
    grad = (ref1[1] - ref2[1]) / (ref1[0] - ref2[0])
    # Merupakan nilai x yang di dalam garis
    yline = ref1[1] + grad * (point[0] - ref1[0])
    if point[1] > yline:
        return "Above"
    elif point[1] < yline:
        return "Below"
    else:
        return "On"

# Kelas ConvexHull yang dapat di gunakan untuk mendapatkan convex hull dari data


class ConvexHull:
    # Constructor, dengan anggapan points merupakan array dari points (array of (X, Y))
    def __init__(self, points):
        self.points = np.array(points)
        self.hull = np.array(ConvexHull.get_hull(self.points))

    @staticmethod
    # Dianggap points yang sudah masuk telah di sort oleh fungsi get_hull
    def __get_top_hull(points):
        if len(points) <= 2:
            return points
        first = points[0]
        last = points[-1]
        # Mencari titik yang paling atas

        top = max(points, key=lambda x: get_distance(
            x, first) + get_distance(x, last))

        # Left Top merupakan titik yang di atas titik first, dan top
        # Right Top merupakan titik yang di atas titik top, dan last
        left_top = [first]
        right_top = [top]
        for i in range(1, len(points) - 1):
            if (isAboveOrBelow(top, first, points[i]) == "Above"):
                left_top.append(points[i])
            if (isAboveOrBelow(top, last, points[i]) == "Above"):
                right_top.append(points[i])
        left_top.append(top)
        right_top.append(last)

        # Mengembalikan hull dari kiri dan kanan
        return ConvexHull.__get_top_hull(left_top) + ConvexHull.__get_top_hull(right_top)

    @staticmethod
    # Dianggap points yang sudah masuk telah di sort oleh fungsi get_hull
    def __get_bottom_hull(points):
        if len(points) <= 2:
            return points
        first = points[0]
        last = points[-1]
        # Mencari titik yang paling atas

        bot = max(points, key=lambda x: get_distance(
            x, first) + get_distance(x, last))

        # Left Bot merupakan titik yang di bawah titik first, dan bot
        # Right Bot merupakan titik yang di bawah titik bot, dan last
        left_bot = [first]
        right_bot = [bot]
        for i in range(1, len(points) - 1):
            if (isAboveOrBelow(bot, first, points[i]) == "Below"):
                left_bot.append(points[i])
            if (isAboveOrBelow(bot, last, points[i]) == "Below"):
                right_bot.append(points[i])
        left_bot.append(bot)
        right_bot.append(last)

        # Mengembalikan hull dari kiri dan kanan
        return ConvexHull.__get_bottom_hull(left_bot) + ConvexHull.__get_bottom_hull(right_bot)

    @staticmethod
    # Merupakan fungsi utama yang mencari hull dari points
    def get_hull(points):
        # Mengurutkan points berdasarkan x
        points = quicksort(points, key=lambda x: (x[0], x[1]))

        # Mendapatkan titik pertama dan terakhi sebagai acuan
        first = points[0]
        last = points[-1]

        # Mendapatkan Hull atas dan Bawah secara Divide and Conquer
        top = [first] + [x for x in points[1:-1]
                         if isAboveOrBelow(first, last, x) == "Above"] + [last]
        bottom = [first] + [x for x in points[1:-1]
                            if isAboveOrBelow(first, last, x) == "Below"] + [last]
        res = (ConvexHull.__get_top_hull(
            top))[::-1] + ConvexHull.__get_bottom_hull(bottom)

        # Merapihkan Hull menjadi bentuk simplices agar lebih mudah untuk di gambarkan
        hull_points = [x for idx, x in enumerate(res) if idx % 2 == 0]
        simplices = []
        for i in range(len(hull_points)):
            simplices.append([hull_points[i-1], hull_points[i]])
        return simplices
