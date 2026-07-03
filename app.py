import gradio as gr
from vectorsearch import search, Reference
from typing import List, Generator
from rate_limiter import check_rate_limit
from messages import messages


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


def get_user_ip(request: gr.Request) -> str:
    fallback = "global"
    user_ip = fallback
    if request and request.request:
        headers = request.request.headers
        client = request.request.client
        user_ip = (
            headers.get("x-forwarded-for")
            if headers
            else client.host
            if client
            else None
        )
    return user_ip or fallback


def get_references(query: str, request: gr.Request) -> Generator[List[str], None, None]:
    if query == "":
        top_line_md = messages["empty_query_line"]
        top_character_md = messages["empty_query_character"]
        yield [top_line_md, top_character_md, "Try Entering some text!"]
        return
    user_ip = get_user_ip(request=request)
    rate_limit = check_rate_limit(user_ip=user_ip)
    if rate_limit:
        rate_limit_message = messages["rate_limit"]
        yield [rate_limit_message, "", "", "soup.webp"]
        return
    for response in search(query=query):
        yield process_refrences(response) + ["shrimp.webp"]


with gr.Blocks(
    title="SeinfelDB🥨", theme=gr.Theme.from_hub("Yntec/HaleyCH_Theme_Yellow_Green")
) as demo:
    gr.Markdown("# Find the perfect comeback 🍤")
    with gr.Row(equal_height=True):
        inp_box = gr.Textbox(label="Enter text", scale=8)
        submit_inp = gr.Button("OK", min_width=60)
    img = gr.Image("shrimp.webp", label="The best model", width=650)
    out_main_quote = gr.Markdown()
    out_main_credit = gr.Markdown()

    gr.Markdown("<br />")

    out_others = gr.Markdown()
    execute = {
        "fn": get_references,
        "inputs": inp_box,
        "outputs": [out_main_quote, out_main_credit, out_others, img],
    }
    submit_inp.click(**execute)
    inp_box.submit(**execute)

if __name__ == "__main__":
    demo.launch()
