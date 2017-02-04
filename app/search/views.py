from flask import Blueprint, jsonify, render_template, request

from .engine import engine

search_view = Blueprint('search_view', __name__)

def decode_query(query):
    decoded = {}
    for hint in query.split(','):
        splitted = hint.split(':')
        if len(splitted) == 2:
            key, value = splitted
            decoded[key] = value
    return decoded

@search_view.route('/')
def index():
    '''
    /
        fill the query form with demo query
    ?q=n1:o1,n2:o2
        fill in query form
        search libs
    ?q=n1:o1,n2:o2&l=libc_1.2.3
        fill in query form
        search libs
        show symbols in the lib
    '''
    query = decode_query(request.args.get('q', ''))
    if len(query) == 0:
        demo_query = {'__libc_start_main_ret':'7ae', '_IO_2_1_stdin_':'600'}
        return render_template('index.html', query=demo_query)
    else:
        libs = engine.find(query)

    lib = request.args.get('l')
    if not lib:
        return render_template('index.html', query=query, libs=libs)

    symbols = engine.dump(lib, list(query.keys()))
    return render_template('index.html', query=query, libs=libs, lib=lib, symbols=symbols)
