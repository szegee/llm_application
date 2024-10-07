# Set up and run this Streamlit App
import streamlit as st
import llm_functions # <--- This is the helper function that we have created 
import prep_data1
import matplotlib.pyplot as plt
import plotly.express as px


flyer_otters_path = "pictures/flyer_otters.png"  
iras_logo_path = "pictures/iras logo.png"  

st.sidebar.write("Your personal income tax relief calculator")

# Display the logo at the top of the sidebar
st.sidebar.image(iras_logo_path, use_column_width=True)  # `use_column_width` makes the logo fit the sidebar's width
st.sidebar.image(flyer_otters_path, use_column_width=True) 

with st.container(height = 450):

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Enter your tax income:")
        total_income = st.number_input("Total income (S$)", min_value=0, max_value=99999, step=100)
        st.subheader("Your Total Tax Relief based on input below:")
        placeholder_total_relief = st.empty()  # Placeholder for pie chart (renders first)

    with col6:

        placeholder_piechart = st.empty()  # Placeholder for pie chart (renders first)

#pie chart



st.title("Enter your tax relief amount below:")
st.info("🎯 If the total amount of reliefs claimed exceeds the relief cap, the tax reliefs will be capped at $80,000.")

# display the total tax relief
#st.subheader("Your Total Tax Relief:")
#placeholder_total_relief = st.empty()  # Placeholder for pie chart (renders first)


col1, col2 = st.columns(2)

# Add inputs to the columns in the first row
with col1:
    st.header("👮🏼‍♂️ NS related")
    relief10 = st.number_input("NSman (Self) Relief (S$)", min_value=0, max_value=10000, value=0, step=100)
    relief11 = st.number_input("NSman (Wife) Relief (S$)", min_value=0, max_value=10000, value=0, step=100)
    relief12 = st.number_input("NSman (Parent) Relief (S$)", min_value=0, max_value=10000, value=0, step=100)    
   
with col2:
    st.header("💼 Personal income")
    relief7 = st.number_input("Earned Income Relief (S$)", min_value=0, max_value=10000, value=0, step=100)
    relief8 = st.number_input("Foreign Domestic Worker Levy Relief (S$)", min_value=0, max_value=10000, value=0, step=100)
    relief9 = st.number_input("CPF Relief (S$)", min_value=0, max_value=10000, value=0, step=100)


col3, col4 = st.columns(2)

# Add inputs to the columns in the second row
with col3:
    st.header("👨‍👨‍👧‍👦 Family related")
    relief1 = st.number_input("Spouse Relief/ Spouse Relief (Disability) (S$)", min_value=0, max_value=20000, value=0, step=100)
    relief2 = st.number_input("Parent Relief/Parent Relief (Disability) (S$)", min_value=0, max_value=10000, value=0, step=100)
    relief3 = st.number_input("Grandparent Caregiver Relief (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief4 = st.number_input("Sibling Relief (Disability) (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief5 = st.number_input("Working Mother's Child Relief (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief6 = st.number_input("Qualifying Child Relief/Child Relief (Disability) (S$)", min_value=0, max_value=10000, value=0, step=10)

with col4:
    st.header("✅ Others")
    relief13 = st.number_input("Life Insurance Relief (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief14 = st.number_input("Course Fees Relief (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief15 = st.number_input("SRS Relief (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief16 = st.number_input("CPF Relief (Compulsory and Voluntary Medisave Contributions) (S$)", min_value=0, max_value=10000, value=0, step=10)
    relief17 = st.number_input("CPF Cash Top-up Relief (S$)", min_value=0, max_value=10000, value=0, step=10)

# Calculate the sum of all the relief
total_relief_ = [i for i in range(1, 15)] 
total_relief_ = min( sum(total_relief_),80000)

total_relief_ = sum(globals()[f'relief{i}'] for i in range(1, 18))
total_relief_ = min( total_relief_,80000)


placeholder_total_relief.write(f"${total_relief_}")

# Create a pie chart with the input values
labels = ['Total Deduction (relief)', 'Assessable Income']
values = [total_relief_, total_income - total_relief_]

# Plot the pie chart
# fig, ax = plt.subplots()
# ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

fig = px.pie(values=values, names=labels, title="Total Relief vs Assessable Income", hole=0.3)

# Update layout to adjust the size
fig.update_layout(
    width=300,
    height=400,
    showlegend = False
)

# Display the pie chart at the top
placeholder_piechart.plotly_chart(fig)

# Optional: Provide some tips or next steps
st.info("🎯 Tip: Make sure to check all eligible reliefs to maximize your tax savings!")
