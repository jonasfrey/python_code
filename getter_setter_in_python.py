class Getter_Setter_In_Python:

    def __init__(self, value_a_is_based_on):
        ## initializing the attribute
        #self.a = a
        self.value_a_is_based_on = value_a_is_based_on
        print("class spawned")

    @property
    def a(self):
        if( hasattr(self,"__a") == False ):
            self.a = self.value_a_is_based_on
        return self.__a

    ## the attribute name and the method name must be same which is used to set the value for the attribute
    @a.setter
    def a(self, var):
        self.__a = "a was set to:"+str(var)




gsip = Getter_Setter_In_Python(555)

print(gsip.a)