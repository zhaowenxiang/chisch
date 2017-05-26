class C:
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def __setattr__(self,name,value):
        print "__setattr__"
        if  name=="square":
            self.width = value
            self.height = value
        else:
        #    self.name = value
            self.__dict__[name] = value

    def area(self):
        return self.width * self.height


c=C(4,5)
print(c.area())
print "-------------------------------------------------------------------"
c.square=10
print(c.area())