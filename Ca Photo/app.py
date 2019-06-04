import os
from flask import Flask, flash, request, url_for, render_template, redirect
from PIL import Image
import io


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
			im = Image.open(file)
			im.thumbnail((int(size[0]), int(size[1])))
			target = os.path.join(os.path.split(os.getcwd())[0] ,"Resized_Photos")
			if os.path.exists(target)==False:
				os.mkdir(target)
			im.save(os.path.join(target, file.filename))
			flash("Success!\n Check Resized_Photos Folder in your device Internal Storage")
			return render_template("form.html", cls="is-success")
		except Exception as e:
			print(e)
			return redirect(request.url)
			
		
	return render_template("form.html")
			


if __name__ == "__main__":
	app.run()




