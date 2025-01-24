source /opt/accepter/venv/bin/activate
gh repo sync

python3 -c "from dynamic_flask_server import DynamicFlaskServer; DynamicFlaskServer().run()"