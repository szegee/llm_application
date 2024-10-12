from utility import check_password
import streamlit as st  

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

about_us_otters_path = "pictures/about_us_otter.png"  

st.sidebar.write("Your personal income tax relief calculator")

# Display the logo at the top of the sidebar
st.sidebar.image(about_us_otters_path, use_column_width=True) 

st.title("Methodology")

# Display image
st.image("pictures/Methodology.png" , caption="How I created the app")

st.markdown("""
This section outlines the steps used to build and structure the data for our application. Below is a detailed breakdown of the methodology:

1. **Scrape Data from IRAS Websites**  
   The first step involves collecting relevant tax relief information data from the IRAS (Inland Revenue Authority of Singapore) website. This is done through automated web scripts that extract textual content and relevant information from publicly accessible pages.

2. **Chunk the Scraped Data**  
   Once the data is scraped, it is divided into smaller, more manageable chunks. Each chunk corresponds to content extracted from a single URL page. This ensures that the data is well-organized, and we can efficiently process individual sections of the content.

3. **Generate Embeddings and Create FAISS Vector Store**  
   After chunking the data, each chunk is passed through OpenAI's embedding model, text-embedding-3-small, to generate vector embeddings. These embeddings capture the semantic meaning of the text. The generated vectors are stored in a FAISS (Facebook AI Similarity Search) vector store, which allows for efficient similarity search and retrieval operations based on the vector embeddings.

""")
