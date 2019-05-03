from flask import Flask, request, render_template, abort, redirect, url_for
import asyncio, random, threading

app = Flask(__name__)
sessions = {}
clear_loop = asyncio.new_event_loop()

def thread_clear():
    asyncio.set_event_loop(clear_loop)
    clear_loop.run_forever()

def clear_session(id):
    del sessions[id]

clear_thread = threading.Thread(target=thread_clear)
clear_thread.start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/', methods=['POST'])
def store():
    try:
        total = float(request.form['total'])
        tax = float(request.form['tax'])
        tips = float(request.form['tips'])
    except:
        abort(400)
    while True:
        id = random.randint(1000, 9999)
        if id not in sessions:
            break
    sessions[id] = {'id': id, 'total': total, 'tax': tax, 'tips': tips}
    clear_loop.call_soon_threadsafe(clear_loop.call_later, 600, clear_session, id)
    return redirect(url_for('show', id=id))

@app.route('/<int:id>', methods=['GET'])
def show(id):
    if id in sessions:
        return render_template('show.html', **sessions[id])
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
