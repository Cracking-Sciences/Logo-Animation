from manim import *
import copy

class LeftSuppress(VMobject):
    def __init__(self, main_color, main_opacity, original_slope, left_suppress_height, left_suppress_thickness, 
                 initial_offsets = [0,0,0],
                 **kwargs):
        super().__init__(**kwargs)
        self.original_slope = original_slope
        self.left_suppress_height = left_suppress_height
        self.left_suppress_thickness = left_suppress_thickness
        self.main_color = main_color
        self.main_opacity = main_opacity
        
        self.initial_offsets = initial_offsets
        self.create_shape()

    def create_shape(self):
        left_suppress_position_list = [
            [0,-self.left_suppress_height / 2,0],
            [self.left_suppress_thickness + 0,-self.left_suppress_height / 2,0],
            [self.left_suppress_thickness + self.left_suppress_height / 2 / np.tan(self.original_slope),0,0], # right vertex
            [self.left_suppress_thickness + 0,self.left_suppress_height / 2,0],
            [0,self.left_suppress_height / 2,0],
            [self.left_suppress_height / 2 / np.tan(self.original_slope),0,0],
        ]
        # place finetuning
        left_offset = left_suppress_position_list[2][0]
        for i in range(6):
            left_suppress_position_list[i][0] -= left_offset
            for j in range(3):
                left_suppress_position_list[i][j] += self.initial_offsets[j]
        

        self.left_suppress_shape = Polygon(*left_suppress_position_list, color=self.main_color)
        self.left_suppress_fill = Polygon(*left_suppress_position_list, color=self.main_color)
        self.left_suppress_fill.set_fill(self.main_color, opacity=self.main_opacity)
        self.group = VGroup(self.left_suppress_shape, self.left_suppress_fill)
    
    def create_animation(self):
        return AnimationGroup(
                Create(self.left_suppress_shape),
                FadeIn(self.left_suppress_fill),
                lag_ratio=0.25
            )

class Bar(VMobject):
    def __init__(self, sub_color, sub_opacity, original_slope, bar_height, bar_thickness, 
                 initial_offsets = [0,0,0],
                 **kwargs):
        super().__init__(**kwargs)
        self.original_slope = original_slope
        self.sub_color = sub_color
        self.sub_opacity = sub_opacity
        self.bar_height = bar_height
        self.bar_thickness = bar_thickness
        
        self.initial_offsets = initial_offsets
        self.create_shape()

    def create_shape(self):
        bar_position_list = [
            [0, - self.bar_height / 2, 0],
            [self.bar_thickness, - self.bar_height / 2, 0],
            [self.bar_thickness + self.bar_height / np.tan(self.original_slope),  self.bar_height / 2, 0],
            [self.bar_height / np.tan(self.original_slope),  self.bar_height / 2, 0],
        ]
        # offset
        for i in range(4):
            for j in range(3):
                bar_position_list[i][j] += self.initial_offsets[j]
        
        self.shape = Polygon(*bar_position_list, color=self.sub_color)
        self.bar_shape = Polygon(*bar_position_list, color=self.sub_color)
        self.bar_fill = Polygon(*bar_position_list, color=self.sub_color)
        self.bar_fill.set_fill(self.sub_color, opacity=self.sub_opacity)
        self.group = VGroup(self.bar_shape, self.bar_fill)

    def create_animation(self):
        fill = self.shape.copy()
        fill.set_fill(self.sub_color, opacity=self.sub_opacity)
        return AnimationGroup(
                Create(self.bar_shape),
                FadeIn(self.bar_fill),
                lag_ratio=0.25
            )


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
        self.sub_opacity = 0.8
        
    def construct(self):
        plane = NumberPlane()
        # self.add(plane)
        
        
        bar_1_final_place = [0,0,0]
        
        left_suppress = LeftSuppress(
            self.main_color,
            self.main_opacity,
            self.original_slope,
            self.left_suppress_height,
            self.left_suppress_thickness,
        )
        bar_final_offset_length = -0.77
        bar_1_initial_move_length = -0.2 # along x axis
        bar_2_initial_move_length = 0.5 # along x axis
        bar_1_then_move_length = bar_final_offset_length - bar_1_initial_move_length
        bar_2_then_move_length = bar_final_offset_length - bar_2_initial_move_length
        
        bar_1_hold = [0,0,0]
        bar_1_initial_offset = [0,0,0]
        bar_1_initial_offset[0] = bar_1_hold[0] + bar_1_initial_move_length
        bar_1_initial_offset[1] = bar_1_hold[1] + bar_1_initial_move_length * np.tan(self.original_slope)
        
        bar_1_then_offset = [0,0,0]
        bar_1_then_offset[0] = bar_1_then_move_length
        bar_1_then_offset[1] = bar_1_then_move_length * np.tan(self.original_slope)

        bar_2_hold = [self.bar_thickness + self.bar_height/2/np.tan(self.original_slope),0,0]
        bar_2_initial_offset = [0,0,0]
        bar_2_initial_offset[0] = bar_2_hold[0] + bar_2_initial_move_length
        bar_2_initial_offset[1] = bar_2_hold[1] + bar_2_initial_move_length * np.tan(self.original_slope)
        
        bar_2_then_offset = [0,0,0]
        bar_2_then_offset[0] = bar_2_then_move_length
        bar_2_then_offset[1] = bar_2_then_move_length * np.tan(self.original_slope)

        bar_1 = Bar(             
            self.sub_color,
            self.sub_opacity,
            self.original_slope,
            self.bar_height,
            self.bar_thickness,
            initial_offsets=bar_1_initial_offset
        )

        bar_2 = Bar(             
            self.sub_color,
            self.sub_opacity,
            self.original_slope,
            self.bar_height,
            self.bar_thickness,
            initial_offsets=bar_2_initial_offset
        )

        self.play(
            AnimationGroup(
                left_suppress.create_animation(),
                bar_1.create_animation(),
                bar_2.create_animation(),
                lag_ratio=0.15
            ),
            run_time=1
        )
        
        
        self.whole = VGroup(left_suppress.group, bar_1.group, bar_2.group)
        tilt_matrix = [[1, 0.2], [0, 1]]
        whole_final = copy.deepcopy(self.whole)

        
        whole_final[1].generate_target()
        whole_final[1].target.shift(bar_1_then_offset)
        whole_final[2].generate_target()
        whole_final[2].target.shift(bar_2_then_offset)

        self.play(
            AnimationGroup(
                MoveToTarget(whole_final[1]),
                MoveToTarget(whole_final[2]),
                lag_ratio=0.0
            ),
            run_time=0.0
        )

        self.play(
            ApplyMatrix(tilt_matrix, whole_final,),
            run_time=0.0
        )
        self.play(FadeOut(whole_final), run_time = 0.0)

        self.play(Transform(self.whole, whole_final, time = 1))
        self.wait()
        
        

# manim -pql logo.py Opening