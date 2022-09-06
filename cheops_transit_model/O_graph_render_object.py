
class O_graph_render_object:
    def __init__(
        self, 
        s_type, 
        n_size_x, 
        n_size_y,
        n_x, 
        n_y,
        n_thickness,
        s_text,
        a_color
        # n_alpha
    ):
        self.s_type = s_type # rectangle circle text
        self.n_size_x = n_size_x
        self.n_size_y = n_size_y
        self.n_x = n_x
        self.n_y = n_y
        self.n_thickness = n_thickness
        self.s_text = s_text
        self.a_color = a_color
        # self.n_alpha = n_alpha

    def f_render_function(self):
        pass
        # example below
        # if(self.n_x % 10 < 5 ):
        #     self.a_color = (255,0,0)
        # else: 
        #     self.a_color = (0, 255, 0)

        # if(self.n_x % 1 == 0):
        #     self.o_cv2_text_x.s = str(int(self.n_x))
        # else: 
        #     self.o_cv2_text_x.s = ''