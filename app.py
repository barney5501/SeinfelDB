import gradio as gr
from vectorsearch import search, Reference
from typing import List, Generator


def process_refrences(lines: List[Reference]) -> List[str]:
    top = lines[0]
    top_line_md = f'<center>\n\n# "{top.dialogue}"</center>'
    top_character_md = f"<center>\n\n## -{top.character}, {top.seid}</center>"
    others = [
        f"## {other.dialogue}\n\n{other.character},{other.seid}." for other in lines[1:]
    ]
    others_md = ""
    if len(others) > 0:
        others_md = "# Also:\n\n" + "\n\n---\n\n".join(others)

    return [top_line_md, top_character_md, others_md]


def get_references(query: str) -> Generator[List[str], None, None]:
    if query == "":
        top_line_md = '<center>\n\n# "Well you\'re not saying nothing you must be saying something."</center>'
        top_character_md = '<center>\n\n## -JERRY, S03E12 "</center>'
        yield [top_line_md, top_character_md, "Try Entering some text!"]
        return

    for response in search(query=query):
        yield process_refrences(response)


with gr.Blocks(
    title="SeinfelDB🥨", theme=gr.Theme.from_hub("Yntec/HaleyCH_Theme_Yellow_Green")
) as demo:
    gr.Markdown("# Find the perfect comeback 🍤")
    with gr.Row(equal_height=True):
        inp_box = gr.Textbox(label="Enter text", scale=8)
        submit_inp = gr.Button("OK", min_width=60)
    gr.Image("shrimp.png", label="The best model", width=650)
    out_main_quote = gr.Markdown()
    out_main_credit = gr.Markdown()

    gr.Markdown("<br />")

    out_others = gr.Markdown()
    execute = {
        "fn": get_references,
        "inputs": inp_box,
        "outputs": [out_main_quote, out_main_credit, out_others],
    }
    submit_inp.click(**execute)
    inp_box.submit(**execute)

if __name__ == "__main__":
    demo.launch()
