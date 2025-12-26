import streamlit as st
import pandas as pd
from datetime import date
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import os
from io import BytesIO

env = Environment(loader=FileSystemLoader('templates'))

def init_state():
    defaults = {
        "project": "",
        "name": "",
        "address": "",
        "vdesc": "",
        "idesc": "",
        "ia": 0.0,
        "pd": date.today(),
        "vd": date.today(),
        "vn":0,
        "invoice_items": [],
        "site_visits": [],
        "notes": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def clear():
    
    keys_to_reset = [
        "project", "name", "address",
        "vdesc", "idesc",
        "ia", "vn",
        "invoice_items", "site_visits", "notes"
    ]

    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def generate_invoice():
    
    template = env.get_template("template_copy.html")
    output = template.render(
        projectName = business,
        clientName = client,
        siteAddress = site_address,
        date = date.today(),
        itemList1 = st.session_state.site_visits,
        itemList2 = st.session_state.invoice_items,
        total = total_sum,
        logo_path="logo/logo.jpeg",
        notes=st.session_state.notes
    )
    pdf_buffer = BytesIO()
    HTML(string=output, base_url=os.getcwd()).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer


st.title("VASTU VISION")

# ----------------------------
# HEADER SECTION
# ----------------------------
st.subheader("Business & Client Details")

business = st.text_input("Project Name/Type", key = "project")
client = st.text_input("Client Name", key = 'name')
site_address = st.text_area("Site Address", key = 'address')

st.divider()

# ----------------------------
# INVOICE META SECTION
# ----------------------------
st.subheader("Site Visits")


visit_no = st.number_input("Visit Number", min_value=0, format="%d", key="vn")
visit_desc = st.text_input("Visit Description", key="vdesc")
visit_date = st.date_input("Visit Date", key="vd")

if st.button("➕ Add Visit Item"):
    if visit_no and len(visit_desc) > 0:
        st.session_state.site_visits.append([visit_no, visit_desc, visit_date.strftime("%d-%m-%Y")])
        
    else:
        st.warning("Enter visit number and description")


st.divider()

# ----------------------------
# LIVE SUMMARY BOX
# ----------------------------


if len(st.session_state.site_visits) > 0:
    df = pd.DataFrame.from_records(st.session_state.site_visits)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No visit items added yet")

st.divider()

# ----------------------------
# PAYMENT / LINE ITEM SECTION
# ----------------------------
st.subheader("Add Payment Item")

desc = st.text_input("Item Description", key="idesc")
amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, key="ia")
pay_date = st.date_input("Payment Date", key="pd")

if st.button("➕ Add Item"):
    if desc and amount > 0:
        st.session_state.invoice_items.append([
            desc,
            float(amount),
            pay_date.strftime("%d-%m-%Y")]
        )
    else:
        st.warning("Enter description and amount")


st.divider()

# ----------------------------
# PAYMENT TABLE
# ----------------------------
st.subheader("Payment Schedule")

if len(st.session_state.invoice_items) > 0:
    df = pd.DataFrame.from_records(st.session_state.invoice_items)
    st.dataframe(df, use_container_width=True)
    
    total_sum = 0
    for item in st.session_state.invoice_items:
        total_sum += item[1]

    st.success(f"### 💰 Total Amount: ₹ {total_sum:,.2f}")
else:
    st.info("No payment items added yet")

st.divider()

st.subheader("Additional Notes")

notes = st.text_area(
    "Notes (optional)",
    placeholder="Enter any special instructions, terms, or remarks...",
    key="notes",
    height=120
)


# ----------------------------
# ACTION BUTTONS
# ----------------------------
colA, colB = st.columns(2)
with colA:
   if st.button("🖨 Generate Invoice"):
       pdf_bytes = generate_invoice()

       st.download_button(
           label="Download Invoice",
           data = pdf_bytes,
           file_name="invoice.pdf",
           mime="application.pdf",
           on_click=clear()
       )

       
      

with colB:
    if st.button("🧹 Clear Invoice"):
        st.session_state.confirm_clear = True

    if st.session_state.get("confirm_clear"):
        st.warning("Are you sure you want to clear the invoice?")
        col1, col2 = st.columns(2)

        if col1.button("Yes, Clear"):
            clear()
            st.session_state.confirm_clear = False
            st.rerun()
            

        if col2.button("Cancel"):
            st.session_state.confirm_clear = False

