import numpy
def triangulate(x1, y1, r1, x2, y2, r2, x3, y3, r3):
	A = -2 * x1 + 2 * x2
	B = -2 * y1 + 2 * y2
	C = -2 * x2 + 2 * x3
	D = -2 * y2 + 2 * y3
	E = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
	F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

	det = A * D - B * C
	detX = E * D - B * F
	detY = A * F - E * C

	return [detX/det, detY/det]

print(triangulate(0,0,2**.5,1,0,1,0,1,1))
