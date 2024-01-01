import os
import openai
import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
import requests,io

comments=""
images = []
def generate():
    global images
    images.clear()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    user_prompt = prompt_entry.get("0.0", tkinter.END)
    if user_prompt=="":
        comment.configure(text="Generating Random Art!")
    user_prompt += "in style: " + dropdown.get()

    response = openai.Image.create(
        prompt=user_prompt,
        n=int(count_no.get()),
        size="512x512"
    )

    image_urls = []
    for i in range(len(response['data'])):
        image_urls.append(response['data'][i]['url'])
    print(image_urls)


    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)


    def update_image(index=0):
        comment.configure(text="Image Generated")
        canvas.image = images[index]
        canvas.create_image(0, 0, anchor="nw", image=images[index])
        index = (index + 1) % len(images)
        canvas.after(3000, update_image, index)

    comment.configure(text=comments)
    update_image()


root = ctk.CTk()
root.title("AI Image Genrator")

#ctk.set_appearance_mode("Light")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

propmt_label = ctk.CTkLabel(input_frame,text="Prompt")
propmt_label.grid(row=0,column=0,padx=10,pady=10)
prompt_entry = ctk.CTkTextbox(input_frame,height=10)
prompt_entry.grid(row=0,column=1,padx=10,pady=10)

dropdown_label = ctk.CTkLabel(input_frame,text="Style")
dropdown_label.grid(row=1,column=0,padx=10,pady=10)
list=["Realastic","Catroon","3D Illustration","Flat Art"]
dropdown = ctk.CTkComboBox(input_frame,values=list)
dropdown.grid(row=1,column=1,padx=10,pady=10)

count_label = ctk.CTkLabel(input_frame,text="No. of Image")
count_label.grid(row=2,column=0,padx=10,pady=10)
count_no = ctk.CTkSlider(input_frame,from_=1,to=10,number_of_steps=9)
count_no.grid(row=2,column=1,padx=10,pady=10)
genrate_button = ctk.CTkButton(input_frame,text="Generate Images",command=generate)
genrate_button.grid(row=3,column=0,columnspan=2,sticky="news",padx=10,pady=10)
comment=ctk.CTkLabel(input_frame,text="Generating Images takes time")
comment.grid(row=4,column=0,columnspan=2,sticky="news",padx=10,pady=10)

canvas = tkinter.Canvas(root,width=512,height=512,bg="#1e1f22",bd=0,highlightthickness=0)
canvas.pack(side="left")

root.mainloop()