import imgui
from imgui.integrations.glfw import GlfwRenderer

from voxl.types import GlfwWindowPointer


class Debug:
    def __init__(self, window: GlfwWindowPointer) -> None:
        imgui.create_context()
        self.impl = GlfwRenderer(window)

    def draw(self):
        self.impl.process_inputs()
        imgui.new_frame()

        imgui.begin("Debug")
        imgui.text("Hello from ImGui")
        if imgui.button("Click me"):
            print("clicked")
        imgui.end()  # ✅ REQUIRED

        imgui.render()
        self.impl.render(imgui.get_draw_data())
