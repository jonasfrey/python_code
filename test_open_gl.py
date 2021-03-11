import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

def var_dump(obj):
  '''return a printable representation of an object for debugging'''
  newobj=obj
  if '__dict__' in dir(obj):
    newobj=obj.__dict__
    if ' object at ' in str(obj) and not newobj.has_key('__type__'):
      newobj['__type__']=str(obj)
    for attr in newobj:
      newobj[attr]=var_dump(newobj[attr])
  return newobj


def main():


    if not glfw.init():
        return


    window = glfw.create_window(720, 600, "Opengl GLFW Triangle", None, None)

    if not window:
        glfw.terminate()
        return


    glfw.make_context_current(window)



    triangle = [-0.5,-0.5,0.0,
                 0.5,-0.5,0.0,
                 0.0,0.5,0.0]



    # convert to 32bit float


    triangle = np.array(triangle, dtype = np.float32)

   


    VERTEX_SHADER = """

        #version 330

        in vec4 position;
        void main() {
        gl_Position = position;

    }


    """


    FRAGMENT_SHADER = """
        #version 330

        void main() {

        gl_FragColor = 

        vec4(0.0f, 1.0f,0.0f,1.0f);

        }

    """


    # Compile The Program and shaders

    shader =  OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))



    #Create Buffer object in gpu
    VBO = glGenBuffers(1)

    #Bind the buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_STATIC_DRAW)



    #get the position from vertex shader
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    glUseProgram(shader)






    glClearColor(0.0,1.0,1.0,1.0)



    t = 0

    while not glfw.window_should_close(window):
        t+=1
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        #Draw Triangle
        #print("asdf")
        var_dump(GL_TRIANGLES)
        # exit()
        glDrawArrays(GL_TRIANGLES, 0, 10)


        glfw.swap_buffers(window)


    glfw.terminate()







if __name__ == "__main__":
    main()