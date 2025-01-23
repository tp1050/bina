#!/bin/bash

# Create project structure
mkdir -p app/{routes,templates,static/{css,js,img}}

# Create Python files
touch app/__init__.py
touch app/routes/{__init__.py,main.py,scanner.py,results.py}
touch config.py
touch run.py

# Create template files
touch app/templates/{base.html,index.html,scanner.html,results.html}

# Initialize git
git init
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore