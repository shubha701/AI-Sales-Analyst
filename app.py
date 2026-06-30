import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Sales Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ENV
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "admin123"
    }

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp{
background:#0f172a;
}

/* HERO */
.hero{
background:linear-gradient(
135deg,
#2563eb,
#7c3aed
);

padding:30px;
border-radius:20px;
text-align:center;
color:white;
margin-bottom:20px;
}

/* CARDS */
.metric-card{
background:#1e293b;
padding:20px;
border-radius:20px;
text-align:center;
color:white;
border:1px solid #334155;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
background:#020617;
}

section[data-testid="stSidebar"] *{
color:white;
}

/* INPUT LABELS */
.stTextInput label{
color:white !important;
font-weight:bold;
}

.stTextArea label{
color:white !important;
font-weight:bold;
}

/* INPUT BOX */
.stTextInput input{
background:white !important;
color:black !important;
}

.stTextArea textarea{
background:white !important;
color:black !important;
}

/* BUTTONS */
.stButton button{
width:100%;
border:none;
border-radius:10px;
background:linear-gradient(
135deg,
#2563eb,
#7c3aed
);
color:white;
font-weight:bold;
}

/* HIDE STREAMLIT */
footer{
visibility:hidden;
}

header{
visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTH PAGE
# ==========================================

def auth_page():

    st.markdown("""
    <div class="hero">
    <h1>📈 AI Sales Analytics </h1>
    <h3>Enterprise Intelligence Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Sign Up"]
    )

    # LOGIN

    with login_tab:

        username = st.text_input(
            "Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button(
            "Login"
        ):

            users = st.session_state.users

            if (
                username in users
                and
                users[username] == password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(
                    "Login Successful"
                )

                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

    # SIGNUP

    with signup_tab:

        new_user = st.text_input(
            "Create Username"
        )

        new_pass = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_pass = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "Create Account"
        ):

            if new_user == "":

                st.warning(
                    "Enter Username"
                )

            elif new_pass != confirm_pass:

                st.error(
                    "Passwords do not match"
                )

            elif (
                new_user
                in
                st.session_state.users
            ):

                st.error(
                    "Username already exists"
                )

            else:

                st.session_state.users[
                    new_user
                ] = new_pass

                st.success(
                    "Account Created"
                )

# ==========================================
# SHOW LOGIN
# ==========================================

if not st.session_state.logged_in:

    auth_page()
    st.stop()
    
# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    # 🚀 AI Sales Analytics
    ### Enterprise Analytics 
    """)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analytics",
            "AI Analyst",
            "Reports"
        ]
    )

    st.session_state.page = page

    st.divider()

    st.success(
        f"👤 {st.session_state.username}"
    )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
<h1>📊 AI Sales Analytics Dashboard</h1>
<h4>Transform Data Into Business Intelligence</h4>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Sales Dataset",
    type=[
        "csv",
        "xlsx",
        "xls"
    ]
)

if uploaded_file is None:

    st.info(
        "👈 Upload a sales dataset from the sidebar to begin."
    )

    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

with st.spinner(
    "Loading dataset..."
):

    try:

        if uploaded_file.name.endswith(
            ".csv"
        ):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file,
                engine="openpyxl"
            )

    except Exception as e:

        st.error(
            f"Error loading file: {e}"
        )

        st.stop()

# ==========================================
# DATA CLEANING
# ==========================================

df.drop_duplicates(
    inplace=True
)

df.fillna(
    0,
    inplace=True
)

if "Date" in df.columns:

    try:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

    except:
        pass

# ==========================================
# DATA PREVIEW
# ==========================================

with st.expander(
    "📄 Dataset Preview"
):

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# ==========================================
# FILTERS
# ==========================================

st.sidebar.subheader(
    "📌 Filters"
)

# Region Filter

if "Region" in df.columns:

    selected_regions = st.sidebar.multiselect(
        "Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

else:

    selected_regions = []

# Product Filter

if "Product" in df.columns:

    selected_products = st.sidebar.multiselect(
        "Product",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

else:

    selected_products = []

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if (
    "Region" in df.columns
    and
    len(selected_regions) > 0
):

    filtered_df = filtered_df[
        filtered_df["Region"]
        .isin(selected_regions)
    ]

if (
    "Product" in df.columns
    and
    len(selected_products) > 0
):

    filtered_df = filtered_df[
        filtered_df["Product"]
        .isin(selected_products)
    ]

# ==========================================
# DATASET SUMMARY
# ==========================================

st.subheader(
    "📋 Dataset Summary"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Rows",
        f"{len(filtered_df):,}"
    )

with c2:
    st.metric(
        "Columns",
        len(filtered_df.columns)
    )

with c3:

    if "Region" in filtered_df.columns:

        st.metric(
            "Regions",
            filtered_df["Region"].nunique()
        )

with c4:

    if "Product" in filtered_df.columns:

        st.metric(
            "Products",
            filtered_df["Product"].nunique()
        )

st.divider()

# ==========================================
# PAGE ROUTING VARIABLE
# ==========================================

page = st.session_state.page

# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    st.subheader("📊 Executive Dashboard")

    # =====================================
    # KPI CALCULATIONS
    # =====================================

    total_revenue = (
        filtered_df["Revenue"].sum()
        if "Revenue" in filtered_df.columns
        else 0
    )

    total_orders = (
        filtered_df["OrderID"].nunique()
        if "OrderID" in filtered_df.columns
        else len(filtered_df)
    )

    total_units = (
        filtered_df["UnitsSold"].sum()
        if "UnitsSold" in filtered_df.columns
        else 0
    )

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    # Demo growth indicators

    revenue_growth = 12.4
    orders_growth = 8.7
    units_growth = 15.2
    aov_growth = 6.5

    # =====================================
    # KPI CARDS
    # =====================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="metric-card">
        <h4>💰 Revenue</h4>
        <h2>₹{total_revenue:,.0f}</h2>
        <p style="color:#22c55e;">
        ▲ {revenue_growth}%
        </p>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>🛒 Orders</h4>
        <h2>{total_orders:,}</h2>
        <p style="color:#22c55e;">
        ▲ {orders_growth}%
        </p>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
        <h4>📦 Units Sold</h4>
        <h2>{total_units:,}</h2>
        <p style="color:#22c55e;">
        ▲ {units_growth}%
        </p>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="metric-card">
        <h4>📈 Avg Order Value</h4>
        <h2>₹{avg_order_value:,.0f}</h2>
        <p style="color:#22c55e;">
        ▲ {aov_growth}%
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # REVENUE GAUGE
    # =====================================

    st.subheader("🎯 Revenue Performance")

    gauge_max = (
        total_revenue * 1.2
        if total_revenue > 0
        else 100
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=total_revenue,
            title={
                "text":
                "Revenue Achievement"
            },
            gauge={
                "axis": {
                    "range": [0, gauge_max]
                },
                "bar": {
                    "color": "#22c55e"
                },
                "steps": [
                    {
                        "range": [0, gauge_max*0.5],
                        "color": "#ef4444"
                    },
                    {
                        "range": [
                            gauge_max*0.5,
                            gauge_max*0.8
                        ],
                        "color": "#facc15"
                    },
                    {
                        "range": [
                            gauge_max*0.8,
                            gauge_max
                        ],
                        "color": "#22c55e"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # PRODUCT & REGION CHARTS
    # =====================================

    col1, col2 = st.columns(2)

    # PRODUCT REVENUE

    with col1:

        st.subheader(
            "🏆 Revenue By Product"
        )

        if (
            "Product" in filtered_df.columns
            and
            "Revenue" in filtered_df.columns
        ):

            product_df = (
                filtered_df.groupby(
                    "Product"
                )["Revenue"]
                .sum()
                .reset_index()
                .sort_values(
                    "Revenue",
                    ascending=False
                )
            )

            fig1 = px.bar(
                product_df,
                x="Product",
                y="Revenue",
                color="Revenue",
                text_auto=True,
                template="plotly_dark"
            )

            fig1.update_layout(
                height=450
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

    # REGION PIE

    with col2:

        st.subheader(
            "🌎 Revenue By Region"
        )

        if (
            "Region" in filtered_df.columns
            and
            "Revenue" in filtered_df.columns
        ):

            region_df = (
                filtered_df.groupby(
                    "Region"
                )["Revenue"]
                .sum()
                .reset_index()
            )

            fig2 = px.pie(
                region_df,
                names="Region",
                values="Revenue",
                hole=0.55,
                template="plotly_dark"
            )

            fig2.update_layout(
                height=450
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    st.divider()

    # =====================================
    # REVENUE TREND
    # =====================================

    if (
        "Date" in filtered_df.columns
        and
        "Revenue" in filtered_df.columns
    ):

        st.subheader(
            "📈 Revenue Trend"
        )

        trend_df = (
            filtered_df.groupby(
                "Date"
            )["Revenue"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            trend_df,
            x="Date",
            y="Revenue",
            markers=True,
            template="plotly_dark"
        )

        fig3.update_layout(
            height=500
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # TOP PRODUCTS
    # =====================================

    if (
        "Product" in filtered_df.columns
        and
        "Revenue" in filtered_df.columns
    ):

        st.subheader(
            "🏅 Top Products"
        )

        top_products = (
            filtered_df.groupby(
                "Product"
            )["Revenue"]
            .sum()
            .reset_index()
            .sort_values(
                "Revenue",
                ascending=False
            )
        )

        st.dataframe(
            top_products,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # DATA TABLE
    # =====================================

    with st.expander(
        "📄 View Complete Dataset"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

# ==========================================
# ANALYTICS PAGE
# ==========================================

elif page == "Analytics":

    st.subheader("📈 Advanced Analytics")

    st.markdown("""
    Analyze sales performance, revenue distribution,
    product efficiency, and regional trends.
    """)

    st.divider()

    # =====================================
    # PRODUCT PERFORMANCE
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🏆 Product Performance")

        if (
            "Product" in filtered_df.columns
            and
            "Revenue" in filtered_df.columns
            and
            "UnitsSold" in filtered_df.columns
        ):

            product_analysis = (
                filtered_df.groupby("Product")
                .agg({
                    "Revenue": "sum",
                    "UnitsSold": "sum"
                })
                .reset_index()
            )

            fig_product = px.scatter(
                product_analysis,
                x="UnitsSold",
                y="Revenue",
                size="Revenue",
                color="Product",
                template="plotly_dark",
                title="Revenue vs Units Sold"
            )

            fig_product.update_layout(
                height=500
            )

            st.plotly_chart(
                fig_product,
                use_container_width=True
            )

    # =====================================
    # REGION ANALYSIS
    # =====================================

    with col2:

        st.markdown("### 🌍 Region Performance")

        if (
            "Region" in filtered_df.columns
            and
            "Revenue" in filtered_df.columns
        ):

            region_analysis = (
                filtered_df.groupby("Region")
                ["Revenue"]
                .sum()
                .reset_index()
                .sort_values(
                    "Revenue",
                    ascending=False
                )
            )

            fig_region = px.bar(
                region_analysis,
                x="Region",
                y="Revenue",
                color="Revenue",
                template="plotly_dark",
                title="Revenue by Region"
            )

            fig_region.update_layout(
                height=500
            )

            st.plotly_chart(
                fig_region,
                use_container_width=True
            )

    st.divider()

    # =====================================
    # MONTHLY SALES TREND
    # =====================================

    if (
        "Date" in filtered_df.columns
        and
        "Revenue" in filtered_df.columns
    ):

        st.markdown(
            "## 📅 Monthly Revenue Trend"
        )

        monthly_df = filtered_df.copy()

        monthly_df["Month"] = (
            monthly_df["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_sales = (
            monthly_df.groupby("Month")
            ["Revenue"]
            .sum()
            .reset_index()
        )

        fig_month = px.area(
            monthly_sales,
            x="Month",
            y="Revenue",
            template="plotly_dark",
            title="Monthly Revenue Growth"
        )

        fig_month.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # PRODUCT REVENUE SHARE
    # =====================================

    if (
        "Product" in filtered_df.columns
        and
        "Revenue" in filtered_df.columns
    ):

        st.markdown(
            "## 🥧 Product Revenue Share"
        )

        product_share = (
            filtered_df.groupby("Product")
            ["Revenue"]
            .sum()
            .reset_index()
        )

        fig_share = px.pie(
            product_share,
            names="Product",
            values="Revenue",
            hole=0.6,
            template="plotly_dark"
        )

        fig_share.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_share,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # REVENUE DISTRIBUTION
    # =====================================

    if "Revenue" in filtered_df.columns:

        st.markdown(
            "## 📊 Revenue Distribution"
        )

        fig_hist = px.histogram(
            filtered_df,
            x="Revenue",
            nbins=20,
            template="plotly_dark"
        )

        fig_hist.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # BUSINESS INSIGHTS
    # =====================================

    st.subheader(
        "💡 Business Insights"
    )

    try:

        top_product = (
            filtered_df.groupby("Product")
            ["Revenue"]
            .sum()
            .idxmax()
        )

        top_region = (
            filtered_df.groupby("Region")
            ["Revenue"]
            .sum()
            .idxmax()
        )

        total_revenue = (
            filtered_df["Revenue"]
            .sum()
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.success(
                f"🏆 Top Product\n\n{top_product}"
            )

        with c2:
            st.success(
                f"🌍 Top Region\n\n{top_region}"
            )

        with c3:
            st.success(
                f"💰 Revenue\n\n₹{total_revenue:,.0f}"
            )

    except:
        st.warning(
            "Unable to generate insights."
        )

    st.divider()

    # =====================================
    # ANALYTICS DATA TABLE
    # =====================================

    with st.expander(
        "📄 Analytics Dataset"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )
        
# ==========================================
# AI ANALYST PAGE
# ==========================================

elif page == "AI Analyst":

    st.subheader("🤖 AI Business Analyst")

    st.markdown("""
    Ask questions about your sales data and receive
    AI-powered business insights, recommendations,
    trends, and executive summaries.
    """)

    st.divider()

    # =====================================
    # AI CHAT INTERFACE
    # =====================================

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_area(
        "💬 Ask a Business Question",
        height=150,
        placeholder="""
Examples:

• Which product generates the highest revenue?
• What are the sales trends?
• Which region performs best?
• Give strategic recommendations.
• How can revenue be improved?
"""
    )

    col1, col2 = st.columns([1,1])

    with col1:

        generate_btn = st.button(
            "🚀 Generate Insight"
        )

    with col2:

        clear_btn = st.button(
            "🗑 Clear Chat"
        )

    if clear_btn:

        st.session_state.chat_history = []

        st.success(
            "Chat History Cleared"
        )

    # =====================================
    # GENERATE AI RESPONSE
    # =====================================

    if generate_btn:

        if not question:

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Analyzing sales data..."
            ):

                try:

                    sample_data = (
                        filtered_df
                        .head(100)
                        .to_string()
                    )

                    prompt = f"""
You are an expert Senior Business Analyst.

Analyze the following sales dataset.

DATASET:

{sample_data}

QUESTION:

{question}

Provide:

1. Direct Answer

2. Key Findings

3. Important Trends

4. Business Insights

5. Strategic Recommendations

6. Executive Summary

Keep response professional.
"""

                    response = model.generate_content(
                        prompt
                    )

                    answer = response.text

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Gemini Error: {e}"
                    )

    # =====================================
    # CHAT HISTORY
    # =====================================

    if st.session_state.chat_history:

        st.subheader(
            "📜 AI Conversation"
        )

        for chat in reversed(
            st.session_state.chat_history
        ):

            st.markdown(
                f"""
<div style="
background:#1e293b;
padding:15px;
border-radius:12px;
margin-bottom:10px;
border-left:4px solid #3b82f6;
">

<h4 style="color:#60a5fa;">
👤 Question
</h4>

<p style="color:white;">
{chat['question']}
</p>

</div>
""",
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
<div style="
background:#111827;
padding:15px;
border-radius:12px;
margin-bottom:20px;
border-left:4px solid #22c55e;
">

<h4 style="color:#4ade80;">
🤖 AI Insight
</h4>

<p style="color:white;">
{chat['answer']}
</p>

</div>
""",
                unsafe_allow_html=True
            )

    st.divider()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    st.subheader(
        "📋 Executive Summary Generator"
    )

    if st.button(
        "Generate Executive Summary"
    ):

        with st.spinner(
            "Generating Summary..."
        ):

            try:

                total_revenue = (
                    filtered_df["Revenue"]
                    .sum()
                )

                top_product = (
                    filtered_df.groupby(
                        "Product"
                    )["Revenue"]
                    .sum()
                    .idxmax()
                )

                top_region = (
                    filtered_df.groupby(
                        "Region"
                    )["Revenue"]
                    .sum()
                    .idxmax()
                )

                summary_prompt = f"""
Create a professional executive summary.

Revenue:
{total_revenue}

Top Product:
{top_product}

Top Region:
{top_region}

Include:

• Performance Overview

• Key Findings

• Risks

• Opportunities

• Recommendations

• Final Conclusion
"""

                result = model.generate_content(
                    summary_prompt
                )

                st.success(
                    "Summary Generated"
                )

                st.markdown(
                    result.text
                )

            except Exception as e:

                st.error(e)

    st.divider()

    # =====================================
    # QUICK AI QUESTIONS
    # =====================================

    st.subheader(
        "⚡ Quick Analysis"
    )

    quick_col1, quick_col2, quick_col3 = st.columns(3)

    with quick_col1:

        if st.button(
            "🏆 Best Product"
        ):

            best_product = (
                filtered_df.groupby(
                    "Product"
                )["Revenue"]
                .sum()
                .idxmax()
            )

            st.success(
                f"Top Product: {best_product}"
            )

    with quick_col2:

        if st.button(
            "🌍 Best Region"
        ):

            best_region = (
                filtered_df.groupby(
                    "Region"
                )["Revenue"]
                .sum()
                .idxmax()
            )

            st.success(
                f"Top Region: {best_region}"
            )

    with quick_col3:

        if st.button(
            "📈 Total Revenue"
        ):

            revenue = (
                filtered_df["Revenue"]
                .sum()
            )

            st.success(
                f"₹{revenue:,.0f}"
            )   
            
# ==========================================
# REPORTS PAGE
# ==========================================

elif page == "Reports":

    st.subheader("📥 Reports Center")

    st.markdown("""
    Download reports, export datasets,
    and review business performance summaries.
    """)

    st.divider()

    # =====================================
    # KPI SUMMARY
    # =====================================

    total_revenue = (
        filtered_df["Revenue"].sum()
        if "Revenue" in filtered_df.columns
        else 0
    )

    total_orders = (
        filtered_df["OrderID"].nunique()
        if "OrderID" in filtered_df.columns
        else len(filtered_df)
    )

    total_units = (
        filtered_df["UnitsSold"].sum()
        if "UnitsSold" in filtered_df.columns
        else 0
    )

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue",
        f"₹{total_revenue:,.0f}"
    )

    c2.metric(
        "Orders",
        f"{total_orders:,}"
    )

    c3.metric(
        "Units Sold",
        f"{total_units:,}"
    )

    c4.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

    st.divider()

    # =====================================
    # BUSINESS INSIGHTS
    # =====================================

    st.subheader("📊 Business Highlights")

    try:

        top_product = (
            filtered_df.groupby("Product")
            ["Revenue"]
            .sum()
            .idxmax()
        )

        top_region = (
            filtered_df.groupby("Region")
            ["Revenue"]
            .sum()
            .idxmax()
        )

        highest_revenue = (
            filtered_df["Revenue"]
            .max()
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.success(
                f"""
🏆 Top Product

{top_product}
"""
            )

        with col2:

            st.success(
                f"""
🌍 Top Region

{top_region}
"""
            )

        with col3:

            st.success(
                f"""
💰 Highest Sale

₹{highest_revenue:,.0f}
"""
            )

    except:

        st.warning(
            "Unable to generate insights."
        )

    st.divider()

    # =====================================
    # CSV DOWNLOAD
    # =====================================

    st.subheader("📄 Download CSV Report")

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="sales_report.csv",
        mime="text/csv"
    )

    st.divider()

    # =====================================
    # EXCEL DOWNLOAD
    # =====================================

    st.subheader("📊 Download Excel Report")

    excel_data = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download Excel Compatible File",
        data=excel_data,
        file_name="sales_report.xls",
        mime="application/vnd.ms-excel"
    )

    st.divider()

    # =====================================
    # REPORT PREVIEW
    # =====================================

    st.subheader("📋 Report Preview")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

    st.divider()

    # =====================================
    # DATA STATISTICS
    # =====================================

    st.subheader("📈 Dataset Statistics")

    stats_col1, stats_col2 = st.columns(2)

    with stats_col1:

        st.info(
            f"Rows : {len(filtered_df):,}"
        )

        st.info(
            f"Columns : {len(filtered_df.columns)}"
        )

    with stats_col2:

        if "Region" in filtered_df.columns:

            st.info(
                f"Regions : {filtered_df['Region'].nunique()}"
            )

        if "Product" in filtered_df.columns:

            st.info(
                f"Products : {filtered_df['Product'].nunique()}"
            )

    st.divider()

    # =====================================
    # FINAL REPORT MESSAGE
    # =====================================

    st.success(
        """
✅ Report Ready

Your sales dataset has been successfully
analyzed and is available for export.
        """
    )
                                 