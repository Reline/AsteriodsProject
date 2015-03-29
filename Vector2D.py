import math

class Vector2D:
    def __init__(self, initX, initY):
        self.x = initX
        self.y = initY

    def Add(self, otherVector):
        newVector = Vector2D(self.x, self.y)
        newVector.x += otherVector.x
        newVector.y += otherVector.y
        return newVector

    def Subtract(self, otherVector):
        newVector = Vector2D(self.x, self.y)
        newVector.x -= otherVector.x
        newVector.y -= otherVector.y
        return newVector

    def Scale(self, scaleFactor):
        newVector = Vector2D(self.x, self.y)
        newVector.x *= scaleFactor
        newVector.y *= scaleFactor
        return newVector

    def Magnitude(self):
        sumOfSquares = (self.x ** 2) + (self.y ** 2)
        magnitude = math.sqrt(sumOfSquares)
        return magnitude

    def Normalize(self):
        length = self.Magnitude()
        return self.Scale(1.0 / length)

    def ToList(self):
        newList = [self.x, self.y]
        return newList

    def Copy(self):
        newVector = Vector2D(self.x, self.y)
        return newVector

    def CreateFromPolarCoordinates(length, angle):
        newVector = Vector2D(0.0, 0.0)
        angleInRadians = math.radians(angle)
        newVector.x = length * math.cos(angleInRadians)
        newVector.y = -length * math.sin(angleInRadians)
        return newVector        

    def Display(self):
        return "( " + str(self.x) + ", " + str(self.y) + " )"

"""vectorA = Vector2D(3, 4)
vectorB = Vector2D(10, 12)

sumAB = vectorA.Add(vectorB)
subAB = vectorA.Subtract(vectorB)
subBA = vectorB.Subtract(vectorA)

print("sumAB = " + sumAB.Display())
print("subAB = " + subAB.Display())
print("subBA = " + subBA.Display())

scale5 = vectorA.Scale(5)
lengthA = vectorA.Magnitude()
unitA = vectorA.Normalize()

print("scale5 = " + scale5.Display())
print("lengthA = " + str(lengthA))
print("unitA = " + unitA.Display())"""

def DistanceBetweenTwoPoints(pointA, pointB):
    vectorBetweenPoints = pointB.Subtract(pointA)
    #print("DistanceBetween Point A and Point B is ", vectorBetweenPoints.Magnitude())
    return vectorBetweenPoints.Magnitude()