#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在线笔记本

"""
import os,time,flask

app = flask.Flask(__name__)
# 根路径
base_note_path = "/note/"

def read_saved_data(SAVE_FILE_PATH):
    try:
        txtfile = base_note_path + SAVE_FILE_PATH + ".txtlog"; #文件路径
        if not os.path.exists(base_note_path):
            os.makedirs(base_note_path)
        if not os.path.exists(txtfile):# 如果文件不存在，则创建文件
            with open(txtfile, 'w', encoding='utf-8') as file:
                pass  # 创建一个空文件，不写入任何内容
            return ""
        with open(txtfile, 'r', encoding='utf-8') as file:
            return file.read()
    except (IOError, OSError) as e: # 处理可能的 I/O 错误
        print(f"An error occurred while accessing the file: {e}")
        return ""
        
@app.route('/note/<path:subpath>', methods=['GET'])
def note(subpath):
    saved_content = read_saved_data(subpath)
    html_content = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>在线笔记本</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <style>
            /* 重置默认样式 */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html, body {
                height: 100%;
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden; /* 确保内容不会溢出 */
            }

            textarea {
                width: 98%; /* 留一点空间给滚动条 */
                height: 98%;
                font-size: 18px;
                padding: 10px;
                resize: none;
                border: 1px solid #ccc;
                outline: none;
            }
            </style>
        </head>
        <body>
            <input id="path" value="{{ subpath }}" style="display:none;"></input>
            <textarea id="contentArea" placeholder="Type or paste your content here...">{{ saved_content }}</textarea>
            <script>
                var contentAreaChange = false;
                $('#contentArea').on('input', function() {
                    contentAreaChange = true;
                    $(this).css('border', '1px solid red');
                });
                function sendContent() {
                    if (contentAreaChange) {
                        $('#contentArea').css('border', '1px solid #00ff00');
                        var content = $('#contentArea').val();
                        var path = $('#path').val();
                        $.ajax({
                            url: '/save_content',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({ content : content , path : path}),
                            success: function(response) {
                                contentAreaChange = false;
                                console.log('Content saved successfully');
                            },
                            error: function(error) {
                                console.error('Error saving content:', error);
                            }
                        });
                    }
                }

                // 自动每秒发送一次内容
                setInterval(sendContent, 10 * 1000);
            </script>
        </body>
    </html>
    '''
    return flask.render_template_string(html_content, saved_content=saved_content, subpath=subpath)
    

@app.route('/save_content', methods=['POST'])
def save_content():
    try:
        data = flask.request.get_json()
        content = data.get('content', '')
        path = base_note_path + data.get('path', '') + ".txtlog" #保存路径
        with open(path, 'w', encoding='utf-8') as file:
            file.write(f'{content}')
        return flask.jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return flask.jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)