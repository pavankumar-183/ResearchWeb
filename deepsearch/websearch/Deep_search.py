import gradio as gr
from dotenv import load_dotenv
from Research_Manager import ResearchManager

load_dotenv(override=True)

css = """
body{
    background:linear-gradient(135deg,#0f172a,#1e3a8a,#312e81,#0f172a);
    background-size:400% 400%;
    animation:bgmove 15s ease infinite;
}

@keyframes bgmove{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.container{
    max-width:1100px !important;
}

.main-card{
    background:rgba(255,255,255,.08);
    backdrop-filter:blur(16px);
    border-radius:25px;
    padding:30px;
    border:1px solid rgba(255,255,255,.15);
    box-shadow:0 10px 40px rgba(0,0,0,.3);
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:700;
    color:white;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    color:#d1d5db;
    margin-bottom:25px;
}

.gr-textbox textarea{
    background:rgba(255,255,255,.1)!important;
    color:white!important;
    border-radius:18px!important;
    border:2px solid transparent!important;
    transition:.3s!important;
}

.gr-textbox textarea:focus{
    transform:scale(1.02);
    border:2px solid #60a5fa!important;
    box-shadow:0 0 25px rgba(96,165,250,.6);
}

.gr-button{
    border-radius:16px!important;
    background:linear-gradient(90deg,#2563eb,#7c3aed)!important;
    color:white!important;
    font-size:18px!important;
    transition:.3s;
}

.gr-button:hover{
    transform:translateY(-2px);
    box-shadow:0 0 20px rgba(59,130,246,.5);
}

.examples{
    margin-top:20px;
}

.report-box{
    background:rgba(255,255,255,.08);
    border-radius:20px;
    padding:20px;
}
"""


async def run(query):

    search_plan = await ResearchManager.plan_searches(query)

    search_results = await ResearchManager.perform_searches(search_plan)

    report = await ResearchManager.write_report(
        query,
        search_results
    )

    await ResearchManager.email_report(report)

    return report.markdown_report


with gr.Blocks(
    css=css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo"
    ),
    title="Deep Research"
) as ui:

    with gr.Column(elem_classes="main-card"):

        gr.HTML("""
        <div class="title">
        🔬 Deep Research AI
        </div>

        <div class="subtitle">
        Research • Analyze • Summarize • Email
        </div>
        """)

        query = gr.Textbox(
            label="Research Topic",
            placeholder="Example: Future of Quantum Computing...",
            lines=3,
        )

        gr.Markdown("### 💡 Try these example prompts")

        gr.Examples(

            examples=[
               ["Future of Artificial Intelligence"],
               ["History of Modern Education"],
               ["Open Source LLM Comparison"],
               ["Quantum Computing"],
               ["Climate Change Solutions"],
               ["Future of Robotics"]
            ],
            inputs=query
        )

        run_btn = gr.Button(
            "🚀 Start Research",
            variant="primary"
        )

        report = gr.Markdown(
            value="### Your report will appear here...",
            elem_classes="report-box"
        )

        run_btn.click(
            fn=run,
            inputs=query,
            outputs=report
        )

        query.submit(
            fn=run,
            inputs=query,
            outputs=report
        )

ui.launch(inbrowser=True)