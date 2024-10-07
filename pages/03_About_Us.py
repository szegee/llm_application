# Set up and run this Streamlit App
import streamlit as st
import llm_functions # <--- This is the helper function that we have created 🆕
import prep_data1



about_us_otters_path = "pictures/about_us_otter.png"  

st.sidebar.write("Your personal income tax relief calculator")

# Display the logo at the top of the sidebar
st.sidebar.image(about_us_otters_path, use_column_width=True) 

st.title("About Us 🌟")

st.header("Project Scope")
st.write("""
    this project encompasses the development of a user-friendly Streamlit application tailored specifically for Singapore tax residents. By leveraging Retrieval Augmented Generation (RAG) for our chatbot and robust calculation algorithms for tax payable, this app aims to provide a comprehensive solution that addresses both informational and practical needs related to personal income tax.
""")

st.header("Objectives")
st.markdown("""
- **Educate and Inform**: Provide clear and concise information about various tax reliefs available to Singapore residents.
- **Simplify Tax Calculations**: Offer an intuitive calculator to help users accurately determine their tax liabilities.
- **Enhance User Experience**: Utilize cutting-edge LLM powered by RAG to offer real-time, accurate responses to user queries through our intelligent chatbot.
- **Ensure Accuracy and Compliance**: Keep our data and tools up-to-date with the latest tax relief from IRAS to ensure users receive reliable information.
""")

st.header("Data Sources")
st.write("""
    To ensure the accuracy and reliability of the information provided, we utilize data from the following sources:
""")
st.markdown("""
- **Inland Revenue Authority of Singapore (IRAS) official website**: The official government body responsible for tax collection and regulation in Singapore.

""")

st.header("Features")
st.markdown("""
This app is packed with features designed to make your tax journey as smooth as possible:

1. **Smart Chatbot 🤖**
    - **Retrieval Augmented Generation (RAG)**: This chatbot uses RAG to provide accurate and contextually relevant answers to your tax-related questions.
    - **24/7 Assistance**: Get help anytime, anywhere without waiting for business hours.

2. **Tax Payable Calculator 💰**
    - **User-Friendly Interface**: Input your financial details through sliders or input boxes and instantly see your tax liability.
    - **Comprehensive Calculation**: Takes into account various tax reliefs and deductions to provide an accurate estimate.

""")


