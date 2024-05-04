import streamlit as st
import openai
import os
import time

from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("API_key")
)

context = """This app assists users in finding information about specific medications 
based on their symptoms. Please follow the prompts to proceed."""

async def generate_response(question, context):
    model = "gpt-4-0125-preview"
    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content

async def app():
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    if "symptoms" not in st.session_state:
        st.session_state["symptoms"] = None
    
    if "selected_medication" not in st.session_state:
        st.session_state["selected_medication"] = None
        
    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        await display_symptoms_form1()
    elif st.session_state["current_form"] == 2:
        await display_information3()

async def display_symptoms_form1():
    form1 = st.form("Introduction")
    form1.subheader("Medication Information Lookup")
    
    text = """Cherry Mirra Calisnao     BSCS 3A \n
    CCS 229 - Intelligent Systems \n
    Final Project in Intelligent Systems \n
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)

    form1.image("med_ai.png", caption="Medication Information App", use_column_width=True)
    text = """An AI powered research co-pilot designed to assist students in finding research problems for their undergraduate thesis."""
    form1.write(text)
    
    # Prompt user for symptoms
    symptoms = form1.text_input("Enter your symptoms (comma-separated):", key="symptoms")
    
    # Display possible medications
    possible_medications = [
        "Paracetamol",
        "Ibuprofen",
        "Aspirin",
        "Cetirizine",
        "Loratadine",
        "Diphenhydramine",
        "Ranitidine",
        "Omeprazole",
        "Loperamide",
        "Simethicone",
        "Other (Specify)"
    ]
    selected_medication = form1.selectbox("Select a possible medication:", options=possible_medications)

    submit1 = form1.form_submit_button("Submit")

    if submit1:
        if symptoms:
            if "symptoms" not in st.session_state:
                st.session_state["symptoms"] = symptoms
            if selected_medication == "Other (Specify)":
                st.session_state["current_form"] = 2  # Skip to medication information form directly
            else:
                st.session_state["selected_medication"] = selected_medication  # Save selected medication
                st.session_state["current_form"] = 2  # Move to the next form
            await display_information3()  # Call the display_information3 function directly
        else:
            form1.warning("Please enter your symptoms.")       

async def display_information3():
    form3 = st.form("Medication Information")
    symptoms = st.session_state["symptoms"]
    selected_medication = st.session_state["selected_medication"]
    
    form3.write(f"Symptoms: {symptoms}")
    form3.write(f"Selected Medication: {selected_medication}")
    
    question = f"Provide information about the medication {selected_medication}, including indications, contraindications, side effects, and nursing considerations."
    progress_bar = form3.progress(0, text="The AI co-pilot is processing the request, please wait...")
    response = await generate_response(question, context)
    form3.write("Medication Information:")
    form3.write(response)

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    form3.success("AI research co-pilot task completed!") 

    submit3 = form3.form_submit_button("Submit")  # Add the submit button
    if submit3:
        form3.write("Would you like to ask another question?")  
        form3.write("If yes, please refresh the browser.") 

# Run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())