from flask import Flask, request, render_template, url_for, redirect
from urllib.request import urlopen
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

mini_database = []

# Flag가 있는 위치 지금 바로 우리 위치 /(현재 디렉토리!!!!!!!!)


@app.route('/')
def index():
    return redirect(url_for('view'))


@app.route('/request')
def url_request():
    url = request.args.get('url', '').lower()
    title = request.args.get('title', '')
    if url == '' or url.startswith("file://") or "flag" in url or title == '':
        # (space) file://
        # https://127.0.0.1:80/
        # url은 file://로 시작하는지 검사하고 flag가 안에 있는지 검사한다.
        # 반면 title은 입력값이 널인지 확인만 하고 그냥 넘긴다.
        # 근데 결국에는 url만 읽어오기 때문에 상관없는것 같다.
        return render_template('request.html')

    try:
        data = urlopen(url).read()  # 그 안에 있는 내용을 읽는다.
        mini_database.append({title: base64.b64encode(data).decode('utf-8')})
        return redirect(url_for('view'))
    except:
        return render_template("request.html")


@app.route('/view')
def view():
    return render_template('view.html', img_list=mini_database)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # ../../flag.txt
        title = request.form.get('title', '')
        if not f or title == '':
            return render_template('upload.html')

        en_data = base64.b64encode(f.read()).decode('utf-8')
        mini_database.append({title: en_data})
        return redirect(url_for('view'))
    else:
        return render_template('upload.html')


# ftp://127.0.0.1:80/static/assetA#03.jpg
if __name__ == "__main__":
    img_list = [
        # %23 == #
        {'초록색 선글라스': "static/assetA#03.jpg"},
        {'분홍색 선글라스': "static/assetB#03.jpg"},
        {'보라색 선글라스': "static/assetC#03.jpg"},
        {'파란색 선글라스': "static/assetD#03.jpg"}
    ]
    for img in img_list:
        for k, v in img.items():
            data = open(v, 'rb').read()
            mini_database.append({k: base64.b64encode(data).decode('utf-8')})

    app.run(host="0.0.0.0", port=80, debug=False)
