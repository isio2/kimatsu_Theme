from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)
#最初の画面に遷移
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)


#ログイン
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):

        return redirect(url_for('geast'))
    if db.admin_login(user_name, password):

        return redirect(url_for('vip'))
    else:
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)



#利用者
@app.route('/geast', methods=['GET'])
def geast():
    return render_template('geast.html')


#管理者
@app.route('/vip', methods=['GET'])
def vip():
    return render_template('vip.html')


#登録
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
    explanation = request.form.get('explanation')

    db.insert_book(title, author, publisher, pages,explanation)

    return render_template('register_complete.html')

#検索
@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search_result", methods=["POST"])
def search_result():
    title = request.form.get("title")
    book_list = db.search_book(title)
    return render_template("search_result.html", books=book_list)

#一覧
@app.route('/list')
def list():
    list = db.select_all_books()
    return render_template('list.html', books = list)

#利用者一覧
@app.route('/gt_list')
def gt_list():
    gt_list = db.select_books()
    return render_template('gt_list.html', books = gt_list)

#説明
@app.route('/explanation')
def explanation():
    list = db.explanation_books()
    return render_template('explanation.html', explanations = list)

# 削除
@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/delete_exe', methods=['POST'])
def delete_exe():
    id = request.form.get('id')

    db.delete_book(id)

    return render_template('succsess.html')

#編集
@app.route('/edit')
def edit():
    id = request.args.get('id')
    return render_template('edit.html' ,id=id)

@app.route('/edit_exe', methods=['POST'])
def edit_exe():

    id = request.form.get('id')
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
    explanation = request.form.get('explanation')

    print(id,title, author, publisher, pages, explanation)

    db.edit_book(id,title, author, publisher, pages, explanation)

    return render_template('edit_complete.html')

#貸出
@app.route('/lend', methods=['GET'])
def lend():
    return render_template('lend.html')

@app.route('/lend_exe', methods=['POST'])
def lend_exe():
    title = request.form.get('title')
    db.insert_lend(title)

    return render_template('lend_complete.html')


#ログアウト
@app.route('/logout', methods=['GET'])
def logout():
    return render_template('index.html')


#新規登録
@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/staff_exe', methods=['POST'])
def staff_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('staff.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('staff.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('staff.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)