import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import os
import qrcode
from datetime import datetime

    
#pdf construction    
def pdf_construction(c_name, s_name, place, description, image_local_path):
    pdf = FPDF()
    pdf.add_page()
    
    #border
    margin = 7
    pdf.set_line_width(0.5)
    pdf.rect(margin, margin, pdf.w - 2*margin, pdf.h - 2*margin)
    
    #logo
    logo_path = os.path.join("images", "mssrf_logo.png")
    logo_width = 50
    x_position = (pdf.w - logo_width)/2
    pdf.image(logo_path, x = x_position, y = 10, w = logo_width)
    
    #watermark
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Arial", "B", 65)
    pdf.rotate(45, x=pdf.w/2, y=pdf.h/2)
    text_width = pdf.get_string_width("MSSRF ORCHIDARIUM")
    text_height = 65 * 0.7
    pdf.text(x=pdf.w/2 - text_width/2, y=pdf.h/2 + text_height/4, txt="MSSRF ORCHIDARIUM")
    pdf.rotate(0)
    pdf.set_text_color(0, 0, 0)
   
    
    #signature
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Arial", "B", 12)
    text_width_1 = pdf.get_string_width("Orchidarium digitalization")
    pdf.text(x=pdf.w - (text_width_1 + 8), y=pdf.h - 15, txt="Orchidarium digitalization")
    text_width_2 = pdf.get_string_width("Navadeep chandran")
    pdf.text(x=pdf.w - (text_width_2 + 8), y=pdf.h - 10, txt="Navadeep chandran")
    pdf.set_text_color(0, 0, 0)

    
    #common name
    pdf.set_font("Arial", "BU", size = 24)
    pdf.multi_cell(0, 40, c_name, align = 'C' )
    pdf.ln(5)
    
    #image
    image_path = image_local_path
    pdf.image(image_path, x=pdf.w/4, w=pdf.w/2 )
    pdf.ln(3)
    
    #scientific name
    pdf.set_font("Arial", "I", size = 20)
    pdf.multi_cell(0, 10, s_name, align = "C")
    pdf.ln(5)
    
    #date n time
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M")
    pdf.set_font("Arial", "I", size = 10)
    pdf.multi_cell(0, 10, f"Date & Time: {date_time_str}", align = "L")
    pdf.ln(1)
    
    #location
    pdf.set_font("Arial", "B", size = 10)
    pdf.multi_cell(0, 10, f"Location : {place}", align = "L")
    
    
    #description
    pdf.set_font("Arial", "BU", size = 18)
    pdf.multi_cell(0, 10, "Description", align = "L")
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, description, align = "L")
    pdf.ln(5)
    
    #pdf save
    pdf.output(f"{s_name}.pdf")
    



def qrcodelink(link):
    qr = qrcode.QRCode(version=1, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 10, border = 4)
    qr.add_data(link)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    return (qr_image)


def name_board_generation(common_name, scientific_name, link_of_pdf):
    # Dynamic input values
    com_name = common_name
    words = com_name.split()   # splits string into list of words
    co_name = ""
    
    for i in range(len(words)):
        co_name += words[i] + " "
        if (i + 1) % 2 == 0:   # after every 2 words
            co_name += "\n"
        
    sc_name = scientific_name
            
    qr_link = link_of_pdf
    
    # Load base background image
    background_image_path = os.path.join('images', 'bg_image.png')
    background = Image.open(background_image_path).convert('RGBA')
    
    # Generate QR code
    qr_image = qrcodelink(qr_link)
    qr_image = qr_image.resize((550, 550))
    
    # Paste QR code on background
    qr_position = (1163, 265)
    background.paste(qr_image, qr_position, qr_image)
    
    # Create drawing context
    draw = ImageDraw.Draw(background)
    
    # Load fonts (adjust the path if needed)
    common_font_path = os.path.join('Fonts', 'arialbd.ttf')
    scientific_font_path = os.path.join('Fonts', 'ariali.ttf')
    common_font = ImageFont.truetype(common_font_path, 100)  # Arial Bold, size 60
    scientific_font = ImageFont.truetype(scientific_font_path, 60)  # Arial Italic, size 40
    
    
    # Add Common Name text
    draw.text((50, 300), co_name.upper(), font=common_font, fill="white")
    
    # Add Scientific Name text
    draw.text((50, 500), sc_name.capitalize(), font=scientific_font, fill="white")
    
    # Save final image
    background.save(f"{co_name}.png")
    background_image_file_path = os.path.abspath(f"{co_name}.png")

    pdf_image = Image.open(background_image_file_path).convert("RGB")
    output_imagetopdf_file_path = background_image_file_path.replace(".png", ".pdf")
    pdf_image.save(output_imagetopdf_file_path, "PDF", resolution = 100.0)
   
#UI/UX
title = st.title("Digitalize Your Garden")

with st.form(key="plant_form"):
    co_name = st.text_input("Enter your plant common name").upper()
    sc_name = st.text_input("Enter your plant Scientific name").capitalize()
    location = st.text_input("Location where the specimen was collected").capitalize()
    description = st.text_area("Enter plant description")
    uploaded_image = st.file_uploader("Please upload the image of the plant species remember it should be in (.jpeg, .jpeg, .png) " , type = ["jpg","jpeg", "png"])
    submit = st.form_submit_button("Submit")
 
#first form for pdf   
if submit:
    if uploaded_image is not None:
        st.markdown("Image uploaded")
        
        image = Image.open(uploaded_image)
        temp_path = "temp_image.png"
        image.save(temp_path)
        uploading_image_path = os.path.abspath(temp_path)
        pdf_construction(co_name, sc_name, location, description, uploading_image_path)
        st.write("Plant details uploaded.")
        st.success("PDF generated successfully")

        #Download button for pdf
        pdf_file_path = f"{sc_name}.pdf"
        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, "rb") as file:
                st.download_button(label = ("Download PDF"), data = file, file_name = pdf_file_path, mime = "application/pdf")
        else:
            st.markdown("Sorry no pdf found")
    else:
        st.markdown("No image uploaded. Please upload an image and continue.")
        uploading_image_path = None
                    
#second form for nameboard
with st.form(key = "nameboard form"):
    drive_link = st.text_input("Please provide your pdf file link:")
    name_board = st.form_submit_button("Generate nameboard")
    if name_board:
        if drive_link is not None:
            st.markdown("Nameboard generated.")
            name_board_generation(co_name, sc_name, drive_link)
            st.success(f"Your nameboard for {co_name} is generated 👍")

            #Download button for pdf
            new_pdf_file_path = f"{co_name}.pdf"
            if os.path.exists(new_pdf_file_path):
                with open(pdf_file_path, "rb") as file:
                    st.download_button(label = ("Download PDF"), data = file, file_name = new_pdf_file_path, mime = "application/pdf")
        
                
    
       
