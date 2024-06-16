from flask import Flask, render_template, request
from utils.query import get_result
from utils.insert import insert

app = Flask(__name__)

@app.route("/insert", methods=['GET', 'POST'])
def insert_user():
    if request.method == 'POST':
        file = request.files.get("file", None)
        name = request.form.get("name", None)
        
        if not file or not name:
            return render_template("insert.html", msg = "error : all fields reqired")

        else:
            file_path = "faces/temp.jpg"
            file.save(file_path)
            
            flag = insert(file_path, name)

            if flag:
                return render_template("insert.html", msg = "success : face added")

            else:
                return render_template("insert.html", msg = "error : face not detected")
        
    return render_template("insert.html", msg = "")

@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        file = request.files.get("file", None)
        
        if not file:
           return render_template("result.html", msg = "error : select a file") 
       
        else:
            file_path = "faces/web.jpg"
            file.save(file_path)
            
            result = get_result(file_path)
            
            return render_template("result.html", msg = result, r = True)
    
    return render_template("result.html", msg = "")

if __name__ == "__main__":
    app.run(debug=True)
