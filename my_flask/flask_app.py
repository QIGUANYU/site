from flask import Flask, render_template, request, make_response  # 添加make_response
import os
import random
import string

app = Flask(__name__)
CODES_FILE = 'codes.txt'

def generate_unique_codes():
    """生成100个签到码"""
    random.seed(os.urandom(16))  # 随机
    codes = set()
    while len(codes) < 100:
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        codes.add(code)
    return list(codes)


def init_code_file():
    """签到码"""
    with open(CODES_FILE, 'w') as f:
        for code in generate_unique_codes():
            f.write(f"{code}\t0\n")


@app.route('/codes')
def codes_page():
    if os.path.exists(CODES_FILE):
        os.remove(CODES_FILE)
    init_code_file()

    codes = []
    with open(CODES_FILE, 'r') as f:
        for line in f:
            codes.append(line.strip().split('\t')[0])

    response = make_response(
        render_template('codes.html', codes=[codes[i:i + 5] for i in range(0, 100, 5)])
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/signin')
def signin_form():
    return '''
    <form action="/verify" method="post">
        Student ID: <input type="text" name="sid" required><br>
        Sign-in Code: <input type="text" name="code" required><br>
        <input type="submit" value="Sign in">
    </form>
    '''


@app.route('/verify', methods=['GET', 'POST'])
def verify_code():
    code_map = {}
    with open(CODES_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                code_map[parts[0]] = parts[1]

    sid = request.values.get('sid', '').upper().strip()
    code = request.values.get('code', '').lower().strip()

    if not code or code not in code_map:
        return "无效签到码，请检查输入"

    current_user = code_map[code]
    if current_user == '0':
        code_map[code] = sid
        response = f"{sid} 签到成功！"
    elif current_user == sid:
        response = "您已签到成功，无需重复操作"
    else:
        response = f"该签到码已被 {current_user} 使用"

    with open(CODES_FILE, 'w') as f:
        for k, v in code_map.items():
            f.write(f"{k}\t{v}\n")

    return response


@app.route('/attended')
def attended_list():
    attended = []
    with open(CODES_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2 and parts[1] != '0':
                attended.append(parts[1])
    return '<br>'.join(attended) if attended else "暂无签到记录"


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except OSError:
        app.run(host='0.0.0.0', port=5001, debug=True)