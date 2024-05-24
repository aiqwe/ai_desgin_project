import gradio as gr
from matplotlib import pyplot as plt
from src import process

def plot(user_id = 1):
    group = process.get_group_info(user_id = 1)
    my = process.get_personal_info(user_id = 1)


demo = gr.Blocks()

with demo:
    gr.Markdown(
        r"Let's do some kinematics! Choose the speed and angle to see the trajectory. Remember that the range $R = v_0^2 \cdot \frac{\sin(2\theta)}{g}$"
    )

    with gr.Row():
        speed = gr.Slider(1, 30, 25, label="Speed")
        angle = gr.Slider(0, 90, 45, label="Angle")
    output = gr.LinePlot(
        x="x",
        y="y",
        overlay_point=True,
        tooltip=["x", "y"],
        x_lim=[0, 100],
        y_lim=[0, 60],
        width=350,
        height=300,
    )
    btn = gr.Button(value="Run")
    btn.click(plot, [speed, angle], output)

if __name__ == "__main__":
    demo.launch()