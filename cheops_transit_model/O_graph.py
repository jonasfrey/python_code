
from O_cv2_text import O_cv2_text
import numpy
import cv2

class O_graph_datapoint:
    def __init__(
        self, 
        n_x, 
        n_y,
        o_cv2_text_x,
        o_cv2_text_y
    ):
        self.n_x = n_x
        self.n_y = n_y
        self.o_cv2_text_x = o_cv2_text_x
        self.o_cv2_text_y = o_cv2_text_y
        self.n_radius = 1
        self.n_thickness = 1
        self.a_color = (0,255,0)

    def f_render_function(self):
        if(self.n_x % 10 < 5 ):
            self.a_color = (255,0,0)
        else: 
            self.a_color = (0, 255, 0)

        if(self.n_x % 1 == 0):
            self.o_cv2_text_x.s = str(int(self.n_x))
        else: 
            self.o_cv2_text_x.s = ''

class O_graph:
    def __init__(
        self,
        n_width_px, 
        n_height_px, 
        a_frame, 
        o_cv2_text_axis_x, 
        o_cv2_text_axis_y, 
        n_min_y,
        n_max_y,
        n_min_x,
        n_max_x,
        n_markers_axis_x,
        n_markers_axis_y,
        ):
        self.n_width_px = n_width_px
        self.n_height_px = n_height_px
        self.a_frame = a_frame
        self.o_cv2_text_axis_x = o_cv2_text_axis_x
        self.o_cv2_text_axis_y = o_cv2_text_axis_y
        self._n_min_y = n_min_y
        self._n_max_y = n_max_y
        self._n_min_x = n_min_x
        self._n_max_x = n_max_x
        self.n_range_y = self._n_max_y - self._n_min_y
        self.n_range_x = self._n_max_x - self._n_min_x
        self.a_o_graph_datapoint = []
        self.a_frame = []
        self.o_cv2_text_default = O_cv2_text( 
                a_color=(0,255,0), 
                s='',
                n_font_size= 0.5,
                n_thickness= 1,
                n_font_type= cv2.FONT_HERSHEY_SIMPLEX
        )

        self.f_update_sizes()

    @property
    def n_min_y(self):
        return self._n_min_y
    @n_min_y.setter
    def n_min_y(self, value):
        self._n_min_y = value
        self.f_update_text_sizes()
    @property
    def n_min_x(self):
        return self._n_min_x
    @n_min_x.setter
    def n_min_x(self, value):
        self._n_min_x = value
        self.f_update_text_sizes()
    @property
    def n_max_y(self):
        return self._n_max_y
    @n_max_y.setter
    def n_max_y(self, value):
        self._n_max_y = value
        self.f_update_text_sizes()
    @property
    def n_max_x(self):
        return self._n_max_x
    @n_max_x.setter
    def n_max_x(self, value):
        self._n_max_x = value
        self.f_update_text_sizes()

    def f_update_sizes(
        self
    ):
        self.n_range_y = self.n_max_y - self.n_min_y
        self.n_range_x = self.n_max_x - self.n_min_x


        self.n_scale_graph = 0.8
        self.n_width_downscaled_px = int(self.n_width_px * self.n_scale_graph)
        self.n_height_downscaled_px = int(self.n_height_px * self.n_scale_graph)
        
        self.n_widthdownscaled_pix_per_value = self.n_width_downscaled_px / self.n_range_x
        self.n_heightdownscaled_pix_per_value = self.n_height_downscaled_px / self.n_range_y
        
        self.n_x_offset_downscaled_frame = int((self.n_width_px - self.n_width_downscaled_px) /2)
        self.n_y_offset_downscaled_frame = int((self.n_height_px - self.n_height_downscaled_px) /2)
    def f_clear(
        self
    ):
        pass

    def f_add_data_point(
        self,
        o_graph_datapoint
    ):

        self.a_o_graph_datapoint.append(
            o_graph_datapoint
        )

    def f_a_rendered(
        self
    ):
        # renders the frame and returns it
        self.a_frame = numpy.zeros([self.n_height_px,self.n_width_px,4],dtype=numpy.uint8)

        # n_text_x = 0
        # n_text_y = int(self.n_height_px/2)
        n_text_x = 0
        n_text_y = 0
        # Rotate the image using cv2.warpAffine()
        cv2.putText(
                self.a_frame, 
                self.o_cv2_text_axis_y.s,
                (0,self.o_cv2_text_axis_y.n_height_px),
                self.o_cv2_text_axis_y.n_font_type, 
                self.o_cv2_text_axis_y.n_font_size,
                self.o_cv2_text_axis_y.a_color,
                self.o_cv2_text_axis_y.n_thickness
        )
        
        M = cv2.getRotationMatrix2D((self.o_cv2_text_axis_y.n_height_px,self.o_cv2_text_axis_y.n_height_px), -90, 1)
        self.a_frame = cv2.warpAffine(self.a_frame, M, (self.a_frame.shape[1], self.a_frame.shape[0]))
        n_x_transform = 0
        n_y_transform = int(self.n_height_px/2) - int((self.o_cv2_text_axis_y.n_width_px)/2)
        a_matrix_transform = numpy.float32([
            [1, 0, n_x_transform],
            [0, 1, n_y_transform]
        ])
        self.a_frame = cv2.warpAffine(self.a_frame, a_matrix_transform, (self.a_frame.shape[1], self.a_frame.shape[0]))
        # cv2.imshow("rot", self.a_frame)
        


        n_text_x = int(self.n_width_px/2) - int(self.o_cv2_text_axis_x.n_width_px/2)
        print(self.o_cv2_text_axis_x.n_width_px)
        n_text_y = int(self.n_height_px - self.o_cv2_text_axis_x.n_height_px)


        # render axis
        cv2.putText(
                self.a_frame, 
                self.o_cv2_text_axis_x.s,
                (n_text_x, n_text_y),
                self.o_cv2_text_axis_x.n_font_type, 
                self.o_cv2_text_axis_x.n_font_size,
                self.o_cv2_text_axis_x.a_color,
                self.o_cv2_text_axis_x.n_thickness
        )



        cv2.rectangle(
            self.a_frame, 
            (
                self.n_x_offset_downscaled_frame,
                self.n_y_offset_downscaled_frame
            ),
            (
                int(self.n_x_offset_downscaled_frame+self.n_width_downscaled_px),
                int(self.n_y_offset_downscaled_frame+self.n_height_downscaled_px)
            ),
            (0,255,0,1),
            1
        )

        for (n_i, o_graph_datapoint) in enumerate(self.a_o_graph_datapoint):
            
            o_graph_datapoint.f_render_function()

            n_x_px = int(self.n_widthdownscaled_pix_per_value * o_graph_datapoint.n_x) + self.n_x_offset_downscaled_frame
            n_y_px = int(self.n_heightdownscaled_pix_per_value * o_graph_datapoint.n_y) + self.n_y_offset_downscaled_frame

            cv2.circle(
                self.a_frame,
                (n_x_px, n_y_px),
                o_graph_datapoint.n_radius,
                o_graph_datapoint.a_color,
                o_graph_datapoint.n_thickness
            )
            if(o_graph_datapoint.o_cv2_text_x.s != ''):

                # n_x = int(n_px_per_marker * n_i) + self.n_x_offset_downscaled_frame
                n_y = self.n_y_offset_downscaled_frame + self.n_height_downscaled_px
                self.o_cv2_text_default.s = str(o_graph_datapoint.o_cv2_text_x.s)
                
                cv2.putText(
                        self.a_frame,
                        o_graph_datapoint.o_cv2_text_x.s,
                        (n_x_px, n_y),
                        o_graph_datapoint.o_cv2_text_x.n_font_type, 
                        o_graph_datapoint.o_cv2_text_x.n_font_size,
                        o_graph_datapoint.o_cv2_text_x.a_color,
                        o_graph_datapoint.o_cv2_text_x.n_thickness
                )

        
        # n_px_per_marker = self.n_width_downscaled_px / self.n_markers_axis_x

        # n_marker_val_per_index = self.n_range_x / self.n_markers_axis_x
        # for n_i in range(0,self.n_markers_axis_x):


        return self.a_frame
