import streamlit as st
from PIL import Image


st.title (" ROVER VQA ")


print("All files moved successfully.")

                        
                
input_answer1 = st.text_area("Enter Exact Topic For Presentation:")
button_pressed1 = st.button("Submit Exact Topic")

if button_pressed1 and input_answer1:
    st.write(f"Selected Topic: {input_answer1}")

st.subheader("OR")

input_answer2 = st.text_area("Enter A Broad Topic To Get Related Topic Ideas For Presentation")
button_pressed2 = st.button("Submit Broad Topic")

if button_pressed2 and input_answer2 :
    st.write(f"Pick your Topic")
    button_t1 = st.button(f"1. Topic: 1")
    button_t2 = st.button(f"2. Topic: 2")
    button_t3 = st.button(f"3. Topic: 3")
    button_t4 = st.button(f"4. Topic: 4")
    button_t5 = st.button(f"5. Topic: 5")
  
st.subheader("OPTIONAL:")
uploaded_file = st.file_uploader("Upload Presentation To Show Your Style And Preference.", type=["jpg", "jpeg", "png", "docx", "pptx"])
button_pressed3 = st.button("Submit Preference")

if button_pressed3:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Image/Document Uploaded Successfully")
    else:
        st.write("Uploaded Image")
        
button_pressed5 = st.button("Generate Presentation")

if button_pressed5:
    st.write("Generating")

button_pressed5 = st.button("Download Presentation")

if button_pressed5:
    st.download_button(label="Download Image", data=data, file_name=file_name)
    st.write("DONE!")




