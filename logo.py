from manim import *

class Opening(Scene):
    def __init__(self):
        super().__init__()
        self.original_slope = PI * 0.35
        self.left_suppress_height = 6
        self.left_suppress_thickness = 1.25
        self.bar_height = 2.5
        self.bar_thickness = 1
        self.main_color = PURE_RED
        self.main_opacity = 0.8
        self.sub_color = WHITE
        self.sub_oipacity = 0.8
        
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        self.left_suppress()
        self.bar_1()
    
    
    def left_suppress(self):
        left_suppress_position_list = [
            [0,self.left_suppress_height / 2,0],
            [self.left_suppress_height / 2 / np.tan(self.original_slope),0,0],
            [0,-self.left_suppress_height / 2,0],
            [self.left_suppress_thickness + 0,-self.left_suppress_height / 2,0],
            [self.left_suppress_thickness + self.left_suppress_height / 2 / np.tan(self.original_slope),0,0], # right vertex
            [self.left_suppress_thickness + 0,self.left_suppress_height / 2,0],
        ]
        # place finetuning
        left_offset = left_suppress_position_list[4][0]
        for i in range(6):
            left_suppress_position_list[i][0] -= left_offset

        left_suppress_shape = Polygon(*left_suppress_position_list, color=self.main_color)
        left_suppress_fill = Polygon(*left_suppress_position_list, color=self.main_color)
        left_suppress_fill.set_fill(self.main_color, opacity=self.main_opacity)
        self.play(
            AnimationGroup(
                Create(left_suppress_shape),
                FadeIn(left_suppress_fill),
                lag_ratio=0.25
            )
        )
        left_suppress_group = VGroup(left_suppress_shape, left_suppress_fill)
        return left_suppress_group
    
    def bar_1(self):
        bar_position_list = [
            [0, - self.bar_height / 2, 0],
            [self.bar_thickness, - self.bar_height / 2, 0],
            [self.bar_thickness + self.bar_height / np.tan(self.original_slope),  self.bar_height / 2, 0],
            [self.bar_height / np.tan(self.original_slope),  self.bar_height / 2, 0],
        ]
        
        bar_shape = Polygon(*bar_position_list, color=self.sub_color)
        bar_fill = Polygon(*bar_position_list, color=self.sub_color)
        bar_fill.set_fill(self.sub_color, opacity=self.sub_oipacity)
        self.play(
            AnimationGroup(
                Create(bar_shape),
                FadeIn(bar_fill),
                lag_ratio=0.25
            )
        )
        left_suppress_group = VGroup(bar_shape, bar_fill)
        return left_suppress_group
        

# manim -pql logo.py Opening