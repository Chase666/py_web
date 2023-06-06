from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/headers')
def headers():
    return render_template("headers.html")
    
@app.route('/args')
def args():
    return render_template("args.html")

@app.route('/cookies')
def cookies():
    resp = make_response(render_template("cookies.html"))
    if 'q' in request.cookies: 
        resp.set_cookie('q', 'qq', expires = 0)
    else:
        resp.set_cookie('q', 'qq')

    return resp

@app.route('/form', methods = ['GET', 'POST'])
def form():
    return render_template("form.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

def normalize_number(start, number):
    result = ''
    if start == '+7' or start == '8':
        result = f'8-{number[1:4]}-{number[4:7]}-{number[7:9]}-{number[9:]}'
    elif start == '10':
        result = f'8-{number[0:3]}-{number[3:6]}-{number[6:8]}-{number[8:]}'
    return result

@app.route('/phone_number', methods = ['GET', 'POST'])
def phone_number():
    errors = [
        'Недопустимый ввод. Неверное количество цифр.', 
        'Недопустимый ввод. В номере телефона встречаются недопустимые символы.',
    ]
    allowed_symbols = [' ', '(', ')', '-', '.', '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    phone_number = None
    error_msg = None
    invalid = False
    
    if request.method == 'POST':
        nums_phone_number = ''
        phone_number = request.form.get('phone_number')
        number_length = 0
        for num in phone_number:
            if num not in allowed_symbols:
                error_msg = errors[1]
                invalid = True
                break
            if num.isdigit():
                number_length += 1
                nums_phone_number += str(num)
        if error_msg==errors[1]:
            return render_template('phone_number.html', phone_number=phone_number, invalid=invalid, error_msg=error_msg)
        elif len(nums_phone_number) < 10:
            return render_template('phone_number.html', phone_number=phone_number, invalid=True, error_msg=errors[0])
        if invalid == False and phone_number[0] == '+' and phone_number[1] == '7' and len(nums_phone_number) == 11:
            phone_number = normalize_number('+7', nums_phone_number)
        elif invalid == False and phone_number[0] == '8' and len(nums_phone_number) == 11:
            phone_number = normalize_number('8', nums_phone_number)
        elif invalid == False and len(nums_phone_number) == 10:
            phone_number = normalize_number('10', nums_phone_number)
        elif invalid == False and len(nums_phone_number) > 10:
            error_msg = errors[0]
            invalid = True

    return render_template('phone_number.html', phone_number=phone_number, invalid=invalid, error_msg=error_msg)