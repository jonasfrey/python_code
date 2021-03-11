from fltk import *

class Drawing(Fl_Widget) :
	def draw(self) :
		global args
		fl_push_clip(self.x(), self.y(), self.w(), self.h())
		fl_color(FL_DARK3)
		fl_rectf(self.x(), self.y(), self.w(), self.h())
		fl_push_matrix()
		if args[5] :
			fl_translate(self.x()+self.w()/2.0, self.y()+self.h()/2.0)
			fl_rotate(args[5])
			fl_translate(-(self.x()+self.w()/2.0), -(self.y()+self.h()/2.0))
		fl_color(FL_WHITE)
		fl_translate(self.x(), self.y())
		fl_begin_complex_polygon()
		fl_arc(args[0], args[1], args[2], args[3], args[4])
		fl_gap()
		fl_arc(140, 140, 20, 0, -360)
		fl_end_complex_polygon()
		fl_color(FL_RED)
		fl_begin_line()
		fl_arc(args[0], args[1], args[2], args[3], args[4])
		fl_end_line()
		fl_pop_matrix()
		fl_pop_clip()


def slider_cb(widget, v) :
	global args, drawing
	args[v] = widget.value()
	drawing.redraw()

# "storage_area" is a storage array for widgets, so that
# they are not deleted if their variable name is deaffected
storage_area = []
args=[140, 140, 50, 0, 360, 0]
name=["X", "Y", "R", "start", "end", "rotate"]
window = Fl_Window(100,100,300,500)
drawing = Drawing(10, 10, 280, 280)
y = 300
for n in range(6) :
	s = Fl_Hor_Value_Slider(50, y, 240,25, name[n])
	y = y+25
	if n < 3 :
		s.minimum(0)
		s.maximum(300)
	elif n==5 :
		pass
		s.minimum(0)
		s.maximum(360)
	else :
		pass
		s.minimum(-360)
		s.maximum(360)
	s.step(1)
	s.value(args[n])
	s.align(FL_ALIGN_LEFT)
	s.callback(slider_cb, n)
	# store s, so that the s widget is not deleted on next loop
	storage_area.append(s)

window.end()
window.show()
Fl.run()