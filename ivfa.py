import time

import moderngl as mg
import numpy as np
import imageio as ii

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class Watcher(QThread):
    on_modified = pyqtSignal()

    def __init__(self):
        super(Watcher, self).__init__()

    def on_modified_event(self, e):
        self.on_modified.emit()

    def run(self):
        observer = Observer()
        handler = FileSystemEventHandler()
        handler.on_modified = self.on_modified_event
        observer.schedule(handler, "./gl")
        observer.start()
        observer.join()


class Render(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super(Render, self).__init__()
        self.u_width, self.u_height = 400, 400

        self.u_volumesize = (128, 128, 128)
        self.gx, self.gy, self.gz = (
            int(self.u_volumesize[0] / 4),
            int(self.u_volumesize[1] / 4),
            int(self.u_volumesize[2] / 4),
        )

        self.setMinimumSize(self.u_width, self.u_height)
        self.setMaximumSize(self.u_width, self.u_height)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Texture Generator")
        self.setWindowIcon(QtGui.QIcon("./res/icon.png"))

    def read(self, path):
        with open(path, "r") as fp:
            return fp.read()

    def set_uniform(self, program, data):
        for n, v in data.items():
            if n in program:
                program[n].value = v

    @pyqtSlot()
    def setup(self):
        try:
            # build renderer
            self.render_program = self.gl.program(
                vertex_shader=self.read("./gl/verts.glsl"),
                fragment_shader=self.read("./gl/frags.glsl"),
            )

            self.vao = self.gl.vertex_array(self.render_program, self.vbo, self.ibo)

            uniform = {
                "u_width": self.u_width,
                "u_height": self.u_height,
                "u_volumesize": self.u_volumesize,
            }

            self.set_uniform(self.render_program, uniform)

            # build volume compute
            self.cs = self.gl.compute_shader(self.read("./gl/compute_volume.glsl"))

            self.set_uniform(self.cs, uniform)

            print("shaders recompiled.")

        except Exception as e:
            print(e)

    def initializeGL(self):
        self.gl = mg.create_context()

        vbo = [-1.0, -1.0, -1.0, +1.0, +1.0, -1.0, +1.0, +1.0]
        vbo = np.array(vbo).astype(np.float32)
        vbo = self.gl.buffer(vbo)

        self.vbo = [(vbo, "2f", "in_pos")]

        ibo = [0, 1, 2, 2, 1, 3]
        ibo = np.array(ibo).astype(np.int32)
        self.ibo = self.gl.buffer(ibo)

        volume_buffer_size = (
            self.u_volumesize[0] * self.u_volumesize[1] * self.u_volumesize[2] * 4 * 4
        )
        self.volume_buffer = self.gl.buffer(reserve=volume_buffer_size)
        self.volume_buffer.bind_to_storage_buffer(0)

        self.setup()

        self.watcher = Watcher()
        self.watcher.on_modified.connect(self.setup)
        self.watcher.start()

        # self.cs.run(self.gx, self.gy, self.gz)

        # print("storing debug data..")
        # volume_data = self.volume_buffer.read()
        # data = np.frombuffer(volume_data, dtype=np.float32)
        # data = data.reshape((*self.u_volumesize, 4))
        # data = np.multiply(data, 255.0).astype(np.uint8)

        # debug_writer = ii.get_writer("./_DEBUG_OUTPUT/output.mp4", fps=32)
        # for i, z in enumerate(data):
        #     debug_writer.append_data(z)
        # debug_writer.close()

        # print("debug data storing done!")

    def paintGL(self):
        t = time.time() % 1000.0

        self.set_uniform(self.cs, {
            "u_time": t,
        })

        self.cs.run(self.gx, self.gy, self.gz)

        self.set_uniform(self.render_program, {
            "u_time": t,
            "u_camera_pos": (0.0, 0.0, -5.0),
            "u_camera_dir": (0.0, 0.0, 1.0),
        })
        self.vao.render()
        self.update()


def main():
    app = QtWidgets.QApplication([])
    renderer = Render()
    renderer.show()
    app.exec()


if __name__ == "__main__":
    main()
