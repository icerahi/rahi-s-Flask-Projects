from flask import Flask,render_template, redirect,url_for,request
import cv2,os
import numpy as np
 
from PIL import Image
from pi import camera
 
 

app=Flask(__name__)

@app.route("/detect")
def detect():
    camera()
    
    return redirect(url_for('index'))


 
@app.route("/")
def index():
    return render_template("index.html")

   

if __name__=="__main__":
    app.run()
