import gradio as gr
from vectorsearch import search

with gr.Blocks(title="SeinfelDB🥨") as demo:
    gr.Markdown("# Find the perfect comeback 🍤")
    inp_box = gr.Textbox()
    gr.Image('shrimp.png',label="The best model",height=650)
    out_box = gr.Textbox()
    inp_box.submit(fn=search,inputs=inp_box,outputs=out_box)

if __name__ == "__main__":
    demo.launch()
