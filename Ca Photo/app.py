import os
from flask import Flask, flash, request, url_for, render_template, redirect
from PIL import Image
import io
from email.message import EmailMessage
import smtplib

"""A flask app that can convert a given image into various image sizes by resolution, then sends the resized image to the provided email address
Made by:collinsanele@gmail.com
 """



def send_mail(r_address, file, file_data):
	msg = EmailMessage()
	
	msg['Subject'] = 'Resized Image'
	msg['From'] = 'senders_email@gmail.com'
	msg['To'] = r_address
	msg.set_content("Resized Image Result")
	#with io.BytesIO() as buffer:
		#file_data.save(buffer, format="JPEG")
		#buffer.seek(0)
		#content = buffer.read()
	content = file_data
	msg.add_attachment(content, maintype='image', subtype='jpeg', filename=file.filename)
	
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login("sender's_email@gmail.com", "password")
		smtp.send_message(msg)
	
		

	
	
	



app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdrtfd5"
@app.route("/", methods=["POST", "GET"])
def upload_file():
	if request.method == "POST":
		try:
			if 'file' not in request.files:
				return redirect(request.url)
			file = request.files['file']
			if file.filename == "":
				return redirect(request.url)
			if file.filename.count(".") < 1:
				return redirect(request.url)
			if  file.filename.endswith(".jpg") is None or file.filename.endswith("png") is None:
				return redirect(request.url)
			size = request.form["size"].split("x")
		
			#Write binary file to present working dir
			with open("temp.jpg", "wb") as f:
				f.write(file.read())
		
			im = Image.open("temp.jpg")
			im.thumbnail((int(size[0]), int(size[1])))
			if len(request.form["email"]) < 4:
				return redirect(request.url)
		
			im.save("temp1", "JPEG")
		
			with open("temp1", "rb") as f:
				im = f.read()
			
			#send mail when all conditions are met
			send_mail(request.form['email'], file,im)
			flash("Success!\n Check Your Inbox")
			return render_template("form.html", cls="is-success")
			
		except Exception as e:
			print(e)
			return redirect(request.url)
			
		
	return render_template("form.html")
			


if __name__ == "__main__":
	app.run()
