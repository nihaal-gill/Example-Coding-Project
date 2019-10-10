class Box():
    def __init__(self, centerX = 0.0, centerY = 0.0, centerZ = 0.0, width = 1.0, height = 1.0, depth = 1.0):
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.width = width
        self.height = height
        self.depth = depth

    def setCenter(self, x, y, z):
        self.centerX = x
        self.centerY = y
        self.centerZ = z


    def setWidth(self, width):
        self.width = width
        return self.width

    def setHeight(self, height):
        self.height = height
        return self.height

    def setDepth(self, depth):
        self.depth = depth
        return self.depth

    def volume(self):
        self.volume = self.height * self.width * self.depth
        return self.volume

    def surfaceArea(self):
        self.surfaceArea = 2 * ((self.depth * self.width) + (self.depth * self.height)+ (self.width *self.height))
        return self.surfaceArea

    def overlaps(self, otherBox):
        if(abs(self.centerX - otherBox.centerX) <= (self.width/2) +(otherBox.width/2)):
            if (abs(self.centerY - otherBox.centerY) <= (self.height / 2) + (otherBox.height/2)):
                if (abs(self.centerZ - otherBox.centerZ) <= (self.depth / 2) + (otherBox.depth/2)):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    def contains(self, otherBox):
        # checks to see if the first box 1 is inside of otherBox
        box1PosXdirection = self.centerX + (self.width / 2)
        box1NegXdirection = self.centerX - (self.width / 2)
        box1PosYdirection = self.centerY + (self.height / 2)
        box1NegYdirection = self.centerY - (self.height / 2)
        box1PosZdirection = self.centerZ + (self.depth / 2)
        box1NegZdirection = self.centerZ - (self.depth / 2)

        box2NegXdirection = otherBox.centerX - (otherBox.width / 2)
        box2PosXdirection = otherBox.centerX + (otherBox.width / 2)
        box2NegYdirection = otherBox.centerY - (otherBox.height / 2)
        box2PosYdirection = otherBox.centerY + (otherBox.height / 2)
        box2PosZdirection = otherBox.centerZ + (otherBox.depth / 2)
        box2NegZdirection = otherBox.centerZ - (otherBox.depth / 2)

        # checks to see if the first box 1 is inside of otherBox
        # checks to make sure that the x coordinates are within range of each other
        if ((box1PosXdirection >= box2NegXdirection and box1PosXdirection >= box2PosXdirection) and
                (box1NegXdirection <= box2PosXdirection and box1NegXdirection <= box2NegXdirection)):
            # checks to make sure that the y coordinates are within range of each other
            if ((box1PosYdirection >= box2NegYdirection and box1PosYdirection >= box2PosYdirection) and
                    (box1NegYdirection <= box2PosYdirection and box1NegYdirection <= box2NegYdirection)):
                # checks to make sure that the z coordinates are the same
                if ((box1PosZdirection >= box2NegZdirection and box1PosZdirection >= box2PosZdirection) and
                        (box1NegZdirection <= box2PosZdirection and box1NegZdirection <= box2NegZdirection)):
                    return True
        else:
            return False

    def __repr__(self):
        return ('< {}-by-{}-by-{} 3D box with center at ({},{},{}) >'.format(self.width, self.height, self.depth,self.centerX,self.centerY,self.centerZ))

