import json
import os

import requests
import streamlit as st


st.set_page_config(
    page_title="MenuMind",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

webhook_url = os.environ.get("MENUMIND_WEBHOOK_URL", "").strip()

if not webhook_url:
    try:
        webhook_url = st.secrets.get("MENUMIND_WEBHOOK_URL", "").strip()
    except FileNotFoundError:
        pass


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.html(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #f4f2ec;
        color: #20231f;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    p {
        color: #5f635c;
    }

    /* ---------- Header ---------- */

    .brand {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #20231f;
    }

    .brand-subtitle {
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #85897f;
        margin-top: 0.15rem;
    }

    /* ---------- Hero ---------- */

    .hero-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #68755d;
        margin-top: 3.5rem;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(3rem, 6vw, 5.5rem);
        line-height: 0.94;
        letter-spacing: -0.065em;
        font-weight: 700;
        color: #20231f;
        margin: 0;
    }

    .hero-description {
        max-width: 570px;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #696d65;
        margin-top: 1.7rem;
    }

    /* ---------- Cards ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #dedbd2;
        border-radius: 18px;
        background: #faf9f5;
    }

    /* ---------- Section headings ---------- */

    .section-number {
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #8a8d85;
        font-weight: 700;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: #20231f;
        margin-top: 0.3rem;
    }

    .section-description {
        color: #777a73;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-top: 0.3rem;
    }

    /* ---------- Inputs ---------- */

    label {
        color: #3c4039 !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background: #20231f;
        border-radius: 10px;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background-color: #20231f !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #b9bdb6;
        opacity: 1;
    }

    /* ---------- Button ---------- */

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        border: none;
        background: #20231f;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
        transition: 0.2s ease;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: #343832;
        color: #ffffff;
    }

    /* ---------- Right information panel ---------- */

    .workflow-box {
        background: #20231f;
        color: #ffffff;
        border-radius: 18px;
        min-height: 390px;
        padding: 2.4rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .workflow-number {
        font-size: 0.72rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #aeb5a5;
        font-weight: 700;
    }

    .workflow-title {
        font-size: 2rem;
        line-height: 1.08;
        letter-spacing: -0.04em;
        font-weight: 700;
        margin-top: 2rem;
        color: #ffffff;
    }

    .workflow-text {
        color: #b9bdb6;
        line-height: 1.65;
        font-size: 0.95rem;
        margin-top: 1.2rem;
    }

    .workflow-line {
        height: 1px;
        background: #454941;
        margin-top: 4rem;
        margin-bottom: 1rem;
    }

    .workflow-meta {
        display: flex;
        justify-content: space-between;
        color: #999e95;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* ---------- Results ---------- */

    .result-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #20231f;
        margin-bottom: 0.3rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        border-top: 1px solid #dedbd2;
        margin-top: 4rem;
        padding-top: 1.3rem;
        display: flex;
        justify-content: space-between;
        gap: 2rem;
    }

    .footer-warning {
        max-width: 700px;
        font-size: 0.72rem;
        line-height: 1.55;
        color: #858980;
    }

    .footer-brand {
        text-align: right;
        font-size: 0.7rem;
        line-height: 1.5;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #858980;
    }

    @media (max-width: 768px) {

        .main .block-container {
            padding-top: 1.5rem;
        }

        .hero-label {
            margin-top: 2rem;
        }

        .hero-title {
            font-size: 3.2rem;
        }

        .workflow-box {
            min-height: 320px;
        }

        .footer {
            flex-direction: column;
        }

        .footer-brand {
            text-align: left;
        }

    }

    </style>
    """,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

header_left, header_right = st.columns([1, 1])

with header_left:
    st.html(
        """
        <div class="brand">MenuMind</div>
        <div class="brand-subtitle">Dietary & allergen review</div>
        """,
    )


# ---------------------------------------------------------
# Hero
# ---------------------------------------------------------

hero_left, hero_right = st.columns([1.25, 0.75])

with hero_left:
    st.html(
        """
        <div class="hero-label">Independent kitchen review</div>

        <div class="hero-title">
            Know your<br>
            menu better.
        </div>

        <div class="hero-description">
            Submit your menu and ingredients for a structured dietary
            and allergen review. The completed report will be sent
            directly to the chef email you provide.
        </div>
        """,
    )


# ---------------------------------------------------------
# Main workspace
# ---------------------------------------------------------

st.write("")

form_column, info_column = st.columns([1.08, 0.92], gap="large")


# ---------------------------------------------------------
# Form
# ---------------------------------------------------------

with form_column:

    with st.container(border=True):

        st.html(
            """
            <div class="section-number">01 / Menu details</div>

            <div class="section-title">
                Kitchen information
            </div>

            <div class="section-description">
                Enter the kitchen details and menu you want reviewed.
            </div>
            """,
        )

        st.write("")

        with st.form("menu_review"):

            restaurant_name = st.text_input(
                "Restaurant or kitchen name",
                placeholder="e.g. The Green Kitchen",
            )

            chef_email = st.text_input(
                "Chef email",
                placeholder="chef@example.com",
            )

            menu_text = st.text_area(
                "Menu items and ingredients",
                placeholder=(
                    "Garlic bread: wheat flour, butter, garlic, parsley\n"
                    "Tomato soup: tomatoes, vegetable stock, cream"
                ),
                height=220,
            )

            submitted = st.form_submit_button(
                "Submit menu for review",
                type="primary",
            )


# ---------------------------------------------------------
# Information panel
# ---------------------------------------------------------

with info_column:

    st.html(
        """
        <div class="workflow-box">

            <div>
                <div class="workflow-number">02 / Review workflow</div>

                <div class="workflow-title">
                    From menu text to a structured review.
                </div>

                <div class="workflow-text">
                    Your submission is sent through the MenuMind
                    review workflow. Once processing is complete,
                    the finished report is delivered to the chef
                    email provided.
                </div>
            </div>

            <div>
                <div class="workflow-line"></div>

                <div class="workflow-meta">
                    <span>MenuMind</span>
                    <span>Review workflow</span>
                </div>
            </div>

        </div>
        """,
    )


# ---------------------------------------------------------
# Submission / webhook logic
# ---------------------------------------------------------

if submitted:

    if not all(
        (
            restaurant_name.strip(),
            chef_email.strip(),
            menu_text.strip(),
        )
    ):
        st.error(
            "Enter a kitchen name, chef email, and menu before submitting."
        )

    elif not webhook_url:

        st.error(
            "The n8n webhook is not configured for this app."
        )
        
        st.caption(
            "Use the production webhook URL from your n8n Webhook node."
        )

    else:

        payload = {
            "restaurant_name": restaurant_name.strip(),
            "chef_email": chef_email.strip(),
            "menu_text": menu_text.strip(),
        }

        try:

            with st.spinner("Sending menu for review..."):

                response = requests.post(
                    webhook_url,
                    json=payload,
                    timeout=180,
                )

            response.raise_for_status()

            st.success(
                "Menu submitted. Check the chef email for the review and PDF."
            )

            try:
                result = response.json()

            except (
                json.JSONDecodeError,
                requests.exceptions.JSONDecodeError,
            ):
                result = None

            if isinstance(result, (dict, list)):

                pdf_url = (
                    result.get("pdf_url")
                    or result.get("download_url")
                    if isinstance(result, dict)
                    else None
                )

                if pdf_url:

                    st.link_button(
                        "Open generated PDF",
                        pdf_url,
                    )

                else:

                    st.caption("n8n response")
                    st.json(result)

            elif response.text.strip():

                st.caption("n8n response")
                st.text(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "The request took over three minutes. "
                "Check the workflow execution in n8n; "
                "it may still be processing the menu."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Could not reach the n8n webhook: {error}"
            )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.html(
    """
    <div class="footer">

        <div class="footer-warning">
            AI-generated labels are a review aid, not a food-safety
            guarantee. Verify ingredients, supplier labels, and
            cross-contact risks before serving.
        </div>

        <div class="footer-brand">
            MenuMind<br>
            Review assistance
        </div>

    </div>
    """,
)