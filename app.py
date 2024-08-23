from flask import Flask,render_template,request
import sqlite3
import pickle
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        fname=request.form.get('name')
        pno=request.form.get('phone')
        email=request.form.get('email')
        addr=request.form.get('address')
        msg=request.form.get('message')
        conn=sqlite3.connect('ytdatabase.db')
        cur=conn.cursor()
        cur.execute(f'''
                    insert into contact values('{fname}','{pno}','{email}','{addr}','{msg}')
                    ''')
        conn.commit()
        return render_template('message.html')
    else:
        return render_template('contactus.html')
    
@app.route('/analytical')
def analytical():
    return render_template('analytical.html')

@app.route('/predictor',methods=['GET','POST'])
def likepredict():
    if request.method=='POST':
        views=request.form.get('views')
        dislike=request.form.get('dislikes')
        comment=request.form.get('comment_count')
        genre=request.form.get('genre')
        print(views,dislike,comment,genre)
        with open('model.pickle','rb') as mod:
            model=pickle.load(mod)
        pred=model.predict([[float(views),float(dislike),float(comment),float(genre)]])
        return render_template('result.html',pred=str(round(pred[0])))
    else:
        return render_template('likepredict.html')
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050)