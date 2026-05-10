import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
import json

# --- NEW: Folder Anchor ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. File Trackers (Bulletproof Paths) ---
TRACKER_FILE = os.path.join(SCRIPT_DIR, "inv_tracker.txt")
TEMPLATES_FILE = os.path.join(SCRIPT_DIR, "templates.json")
SIGNATURE_FILE = os.path.join(SCRIPT_DIR, "signature.png")

# --- 2. Auto-Invoice Number System ---
def get_next_inv_number():
    if not os.path.exists(TRACKER_FILE):
        return 1
    with open(TRACKER_FILE, "r") as f:
        return int(f.read().strip())

def increment_inv_number():
    current = get_next_inv_number()
    with open(TRACKER_FILE, "w") as f:
        f.write(str(current + 1))

# --- 3. Template Management System ---
def load_templates():
    default_templates = {
        "Blank Draft": {
            "client_name": "", 
            "client_address": "", 
            "items": [{"Description": "Custom Item", "Quantity": 1, "Price (RM)": 0.0}]
        },
        "Kindle Mind - Setup": {
            "client_name": "Kindle Mind Cheng", 
            "client_address": "Cheng, Melaka\nAttn: Sally\n",
            "items": [{"Description": "Online Review Hub - Setup", "Quantity": 1, "Price (RM)": 190.0}]
        },
        "Kindle Mind - Monthly": {
            "client_name": "Kindle Mind Cheng", 
            "client_address": "Cheng, Melaka\nAttn: Sally\n",
            "items": [{"Description": "Online Review Hub - Monthly Maintenance", "Quantity": 1, "Price (RM)": 40.0}]
        },
        "San Guo - Setup": {
            "client_name": "San Guo", 
            "client_address": "Melaka\nAttn: Sally\n",
            "items": [{"Description": "Online Review Hub - Setup", "Quantity": 1, "Price (RM)": 190.0}]
        }
    }
    
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, "r") as f:
            return json.load(f)
    else:
        with open(TEMPLATES_FILE, "w") as f:
            json.dump(default_templates, f, indent=4)
        return default_templates

def save_template(name, client_name, client_address, items_df):
    templates = load_templates()
    templates[name] = {
        "client_name": client_name,
        "client_address": client_address,
        "items": items_df.to_dict('records')
    }
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=4)

def delete_template(name):
    templates = load_templates()
    if name in templates and name != "Blank Draft":
        del templates[name]
        with open(TEMPLATES_FILE, "w") as f:
            json.dump(templates, f, indent=4)

# --- 4. PDF Generation Engine ---
def create_invoice(client_name, client_address, invoice_no, inv_date, items_df, show_received_by=False):
    pdf = FPDF()
    pdf.add_page()
    
    # Left-Aligned Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 8, "ALICIA GOH TING TING", ln=True, align='L')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Melaka, Malaysia | aliciagoh0704@gmail.com | +60 11-1059 6271", ln=True, align='L')
    pdf.line(10, 25, 200, 25) 
    pdf.ln(10)

    # Client & Invoice Details
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 5, "Bill to:")
    pdf.cell(40, 5, "Invoice No:", align='R')
    pdf.cell(50, 5, f"INV-{invoice_no:03d}", ln=True, align='R')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(100, 5, client_name)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 5, "Invoice Date:", align='R')
    pdf.set_font("Arial", '', 10)
    pdf.cell(50, 5, inv_date.strftime('%Y-%m-%d'), ln=True, align='R')
    
    x, y = pdf.get_x(), pdf.get_y()
    pdf.multi_cell(90, 5, client_address)
    pdf.set_xy(x + 100, y)
    
    pdf.ln(25)

    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(90, 8, "Description", 1, 0, 'L', True)
    pdf.cell(30, 8, "Quantity", 1, 0, 'C', True)
    pdf.cell(35, 8, "Price (RM)", 1, 0, 'C', True)
    pdf.cell(35, 8, "Amount (RM)", 1, 1, 'R', True)

    # Table Content
    pdf.set_font("Arial", '', 10)
    grand_total = 0.0
    
    for index, row in items_df.iterrows():
        desc = str(row['Description'])
        qty = float(row['Quantity'])
        price = float(row['Price (RM)'])
        line_total = qty * price
        grand_total += line_total
        
        pdf.cell(90, 8, desc, 1)
        pdf.cell(30, 8, str(int(qty)), 1, 0, 'C')
        pdf.cell(35, 8, f"{price:.2f}", 1, 0, 'C')
        pdf.cell(35, 8, f"{line_total:.2f}", 1, 1, 'R')

    pdf.ln(5)

    # Totals
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(120)
    pdf.cell(35, 8, "Total Due", align='R')
    pdf.cell(35, 8, f"RM {grand_total:.2f}", align='R', ln=True)
    pdf.ln(15)

    # --- Signature Section ---
    if os.path.exists(SIGNATURE_FILE):
        pdf.ln(5)
        pdf.image(SIGNATURE_FILE, x=10, w=40)

        y_line = pdf.get_y() + 2
        pdf.line(10, y_line, 50, y_line)

        pdf.set_y(y_line + 1)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(40, 5, "Authorized Signature", align='C')

        if show_received_by:
            pdf.line(140, y_line, 190, y_line)
            pdf.set_xy(140, y_line + 1)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(50, 5, "Received By", align='C')

        pdf.ln(15)

    # --- Payment Terms & Final Return ---
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 5, "Payment Instructions", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Bank: Maybank", ln=True)
    pdf.cell(0, 5, "Account Name: Alicia Goh Ting Ting", ln=True)
    pdf.cell(0, 5, "Account No: 1541 2925 4285", ln=True)
    
    # This is the crucial line that was missing!
    return pdf.output(dest='S').encode('latin-1')

# --- 5. Streamlit UI ---
st.set_page_config(page_title="Invoice Gen", layout="wide")

# Load existing templates
all_templates = load_templates()
template_names = list(all_templates.keys())

# Sidebar: Load Template
st.sidebar.header("📁 Load Template")
selected_preset = st.sidebar.selectbox("Choose a Client Template", template_names)

# Get data for selected template
active_data = all_templates[selected_preset]
def_client = active_data["client_name"]
def_addr = active_data["client_address"]
def_items = active_data["items"]

# Main Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Client Details")
    c_name = st.text_input("Client Name", value=def_client)
    c_address = st.text_area("Client Address (Multiple Lines OK)", value=def_addr, height=100)

with col2:
    st.subheader("Invoice Info")
    current_no = get_next_inv_number()
    inv_no = st.number_input("Invoice Number (INV-XXX)", value=current_no, step=1)
    inv_date = st.date_input("Invoice Date")

st.divider()

st.subheader("🛒 Line Items")
items_df = pd.DataFrame(def_items)
# Updated width attribute to fix Streamlit warning
edited_df = st.data_editor(items_df, num_rows="dynamic", width="stretch")

st.divider()

# Signature options
show_received_by = st.checkbox("Add Received By signature line")

# Generate Button
if st.button("🚀 Generate & Save Invoice", type="primary"):
    pdf_bytes = create_invoice(c_name, c_address, inv_no, inv_date, edited_df, show_received_by)
    st.success(f"Invoice INV-{inv_no:03d} generated successfully!")
    
    col_dl, col_save = st.columns(2)
    with col_dl:
        st.download_button(
            label="⬇️ Download PDF Invoice",
            data=pdf_bytes,
            file_name=f"INV-{inv_no:03d}_{c_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    
    if inv_no == current_no:
        increment_inv_number()
        st.info("System automatically updated to the next invoice number!")

# --- 6. Sidebar: Template Manager ---
st.sidebar.divider()
st.sidebar.header("💾 Template Manager")

# Update existing template
if selected_preset != "Blank Draft":
    if st.sidebar.button(f"🔄 Update '{selected_preset}'", width="stretch"):
        save_template(selected_preset, c_name, c_address, edited_df)
        st.rerun()

# Save as new template
new_template_name = st.sidebar.text_input("Save as New Template:")
if st.sidebar.button("➕ Save New", type="primary", width="stretch"):
    if new_template_name and new_template_name != "Blank Draft":
        save_template(new_template_name, c_name, c_address, edited_df)
        st.rerun()
    elif new_template_name == "Blank Draft":
        st.sidebar.error("Cannot overwrite Blank Draft.")
    else:
        st.sidebar.error("Please enter a name.")

# Delete existing template
if selected_preset != "Blank Draft":
    if st.sidebar.button(f"🗑️ Delete '{selected_preset}'", width="stretch"):
        delete_template(selected_preset)
        st.rerun()