import os
import shutil
import nginx
from flask import request, jsonify, Blueprint
from tldextract import tldextract

from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton

app = FlaskAppSingleton().get_app()

web = Blueprint('website_manager', __name__)

conf = app.config
CONF_FILE = '/etc/nginx/conf.d'
WEBSITE_DIR = conf['WEBSITE_DIR'] if 'WEBSITE_DIR' in conf else '/var/www'


@web.route('/website_list', endpoint='website_list', methods=['GET'])
@auth.login_required
def get_websites_list():
    if request.method == 'GET':
        site_list = []
        for file in os.listdir(CONF_FILE):
            if file.endswith('.conf'):
                conf = nginx.loadf(os.path.join(CONF_FILE, file))
                server = conf.server
                domain = server.filter('Key', 'server_name')[0].value
                port = server.filter('Key', 'listen')[0].value
                root_dir = server.filter('Key', 'root')[0].value
                site_list.append({
                    'domain': domain,
                    'listen_port': port,
                    'root_dir': root_dir
                })
        return site_list
    else:
        return jsonify({'message': 'Invalid request method.'}), 405


@web.route('/website_create', endpoint='website_create', methods=['POST'])
@auth.login_required
def create_website():
    if request.method == 'POST':
        domain = request.form.get('domain')
        port = request.form.get('listen_port')
        root_dir = request.form.get('root_dir')
        is_create_dynamic_website = request.form.get('is_create_dynamic_website')
        extracted_domain = tldextract.extract(domain)
        domain_without_suffix = extracted_domain.domain
        if not domain or not port or not root_dir:
            return jsonify({'message': 'Invalid request data.'}), 400
        conf_file = os.path.join(CONF_FILE, domain + '.conf')
        if os.path.exists(conf_file):
            return jsonify({'message': 'Website already exists.'}), 409
        root_dir = os.path.join(WEBSITE_DIR, root_dir)
        conf = nginx.Conf()
        server_block = nginx.Server()
        server_block.add(nginx.Key('listen', str(port)))
        server_block.add(nginx.Key('server_name', domain))
        server_block.add(nginx.Key('root', root_dir))
        server_block.add(nginx.Key('index', 'index.html index.htm'))
        server_block.add(nginx.Location('/', nginx.Key('try_files', '$uri $uri/ =404')))
        # 判断是否创建PHP-FPM配置
        if is_create_dynamic_website == '1':
            server_block.add(nginx.Location('~ \.php$',
                                            nginx.Key('include', 'fastcgi.conf'),
                                            nginx.Key('fastcgi_pass', 'unix:/run/php/php8.1-fpm.sock'),
                                            nginx.Key('fastcgi_param',
                                                      'SCRIPT_FILENAME $document_root$fastcgi_script_name'),
                                            nginx.Key('include', 'fastcgi_params')
                                            ))
            conf.add(server_block)
        # 判断是否创建日志目录
        log_dir = os.path.join(root_dir, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # 判断是否创建网站根目录
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        conf.add(server_block)
        conf_file = os.path.join(CONF_FILE, domain_without_suffix + '.conf')
        nginx.dumpf(conf, conf_file)
        os.system('nginx -s reload')
        return jsonify({'code': 201, 'message': 'Website created successfully.'}), 200
    else:
        return jsonify({'message': 'Invalid request method.'}), 405


@web.route('/website_delete', endpoint='website_delete', methods=['DELETE'])
@auth.login_required
def delete_website():
    if request.method == 'DELETE':
        website_name = request.args.get('website_name')
        if website_name is None:
            return jsonify({'message': 'Invalid request data.'}), 400
        website_dir = os.path.join(WEBSITE_DIR, website_name)
        conf_file = os.path.join(CONF_FILE, website_name + '.conf')
        # 截取conf_file的域名部分
        extracted_domain = tldextract.extract(website_name)
        domain_without_suffix = extracted_domain.domain
        conf_file = os.path.join(CONF_FILE, domain_without_suffix + '.conf')
        if not website_name:
            return jsonify({'message': 'Invalid request data.'}), 400
        if os.path.exists(website_dir) and os.path.exists(conf_file):
            shutil.rmtree(website_dir)
            os.remove(conf_file)
            os.system('nginx -s reload')
            return jsonify({'message': 'successfully deleted website.'}), 200
        print(website_dir)
        print(conf_file)
        return jsonify({'message': 'Website does not exist.'}), 404
    else:
        return jsonify({'message': 'Invalid request method.'}), 405
