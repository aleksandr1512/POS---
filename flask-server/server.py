from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("db.db", check_same_thread=False)
cur = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def form():
    cur.execute(f"SELECT theme, who, time FROM lesons")
    answer = cur.fetchall()
    get_response = [list(set([row[0] for row in answer])),
                    list(set([row[1] for row in answer])),
                    list(set([row[2] for row in answer]))]
    print(get_response)

    if request.method == 'POST':
        theme = request.form['theme']
        who = request.form['who']
        time = int(request.form['time'])
        
        print(time)

        if theme == 'all':
            theme_cond = "WHERE theme = theme"
        else:
            theme_cond = f"WHERE theme = '{theme}'"

        if who == 'all':
            who_cond = "who = who"
        else:
            who_cond = f"who = '{who}'"

        if time == 0:
            time_cond = "time = time"
        else:
            time_cond = f"time = '{time}'"

        cur.execute(f"""SELECT id, title, age, target FROM lesons 
                             {theme_cond}
                             AND {who_cond}
                             AND {time_cond}""")
        response = cur.fetchall()
        print(response)
        return render_template('blog.html', posts=response) 
    return render_template('form.html', parameters=get_response)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    cur.execute(f"SELECT *FROM lesons WHERE id = {post_id}")
    return render_template('post.html', post=cur.fetchone())

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        cur.execute(f"""INSERT INTO lesons (theme, who, time, title, age, target, intro, main, reflection, conclusion) VALUES (
                    '{request.form['theme']}',
                    '{request.form['who']}',
                    '{int(request.form['time'])}',
                    '{request.form['title']}',
                    '{request.form['age'],}',
                    '{request.form['target']}',
                    '{request.form['intro']}',
                    '{request.form['main']}',
                    '{request.form['reflection']}',
                    '{request.form['conclusion']}')""")
    return render_template("add_post.html")


@app.route('/all')
def show_all():
    cur.execute(f"SELECT id, title, age, target FROM lesons ")
    return render_template('blog.html', posts=cur.fetchall()) 

if __name__ == '__main__':
    app.run(port=8001, debug=True)