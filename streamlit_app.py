import os

import streamlit as st

from pipeline import run_research_pipeline


st.set_page_config(
    page_title="ResearchOS",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1180px; padding-top: 2rem; }
    .hero { padding: 1.5rem 0 1rem; }
    .hero h1 { margin-bottom: .25rem; }
    .hero p { color: #64748b; font-size: 1.05rem; }
    [data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: .75rem;
        padding: .75rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_pipeline_status(result: dict) -> None:
    columns = st.columns(4)
    for column, label in zip(columns, ("Search", "Read", "Write", "Critic")):
        column.metric(label, "Complete")


st.markdown(
    """
    <div class="hero">
        <h1>ResearchOS</h1>
        <p>Search, read, write, and critique a research report with one workflow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Research settings")
    st.caption("Credentials are loaded from the root `.env` file.")
    groq_ready = bool(os.getenv("GROQ_API_KEY"))
    tavily_ready = bool(os.getenv("TAVILY_API_KEY"))
    st.status(
        "API keys configured" if groq_ready and tavily_ready else "API keys missing",
        state="complete" if groq_ready and tavily_ready else "error",
    )
    st.caption("Required: `GROQ_API_KEY` and `TAVILY_API_KEY`")

    #if st.button("New research", use_container_width=True):
     #   st.session_state.pop("research_result", None)
        #st.rerun()

with st.form("research_form"):
    topic = st.text_area(
        "What would you like to research?",
        placeholder="Example: How are small language models changing on-device AI?",
        height=100,
    )
    submitted = st.form_submit_button(
        "Run research",
        type="primary",
        use_container_width=True,
    )

if submitted:
    topic = topic.strip()
    if not topic:
        st.error("Enter a research topic before running the pipeline.")
    elif not groq_ready or not tavily_ready:
        st.error(
            "Add both `GROQ_API_KEY` and `TAVILY_API_KEY` to the root `.env` file, "
            "then restart Streamlit."
        )
    else:
        with st.status("Running research pipeline...", expanded=True) as status:
            try:
                result = run_research_pipeline(topic)
                st.session_state["research_result"] = result
                status.update(label="Research complete", state="complete")
            except Exception as exc:
                status.update(label="Research failed", state="error")
                st.error(f"The research pipeline failed: {exc}")

result = st.session_state.get("research_result")
if result:
    st.divider()
    render_pipeline_status(result)
    st.subheader("Research report")

    report_tab, critique_tab, search_tab, reading_tab = st.tabs(
        ["Report", "Critique", "Search results", "Detailed reading"]
    )
    with report_tab:
        st.markdown(result["report"])
        st.download_button(
            "Download report",
            data=result["report"],
            file_name="research-report.md",
            mime="text/markdown",
        )
    with critique_tab:
        st.markdown(result["feedback"])
    with search_tab:
        st.text(result["search_results"])
    with reading_tab:
        st.text(result["scraped_content"])
