from manim import *

class SimpleScene(Scene):
    def construct(self):
        text = Text("Pythagoras Theorem")
        self.play(Write(text))
        self.wait(2)
