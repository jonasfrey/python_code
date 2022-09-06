import cv2
import time


class O_cv2_text:
    def __init__(
        self,
        a_color, 
        s,
        n_font_size, 
        n_thickness, 
        n_font_type,
    ):
        self.a_color = a_color
        self._s = s
        self._n_font_size = n_font_size
        self._n_thickness = n_thickness
        self._n_font_type = n_font_type
        self.f_update_text_size()


    def f_update_text_size(
        self
    ):
        self.a_text_size = cv2.getTextSize(
            self._s,
            self._n_font_type,
            self._n_font_size,
            self._n_thickness
        )
        self.n_width_px = self.a_text_size[0][0]
        self.n_height_px = self.a_text_size[0][1]

    @property
    def s(self):
        return self._s
    @s.setter
    def s(self, value):
        self._s = value
        self.f_update_text_size()
    @property
    def n_font_size(self):
        return self._n_font_size
    @n_font_size.setter
    def n_font_size(self, value):
        self._n_font_size = value
        self.f_update_text_size()

    @property
    def n_thickness(self):
        return self._n_thickness
    @n_thickness.setter
    def n_thickness(self, value):
        self._n_thickness = value
        self.f_update_text_size()

    @property
    def n_font_type(self):
        return self._n_font_type
    @n_font_type.setter
    def n_font_type(self, value):
        self._n_font_type = value
        self.f_update_text_size()


# test
o_cv2_text = O_cv2_text( 
    a_color=(0,255,0), 
    s=str(time.time()),
    n_font_size= 1,
    n_thickness= 1,
    n_font_type= cv2.FONT_HERSHEY_SIMPLEX
)    
print(o_cv2_text.n_width_px)
print(o_cv2_text.n_height_px)