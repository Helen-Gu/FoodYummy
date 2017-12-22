#!flask/bin/python
import sys
activate_this = 'C:/Users/HiroAAA/Envs/FY/Scripts/activate_this.py'
if sys.version_info[0] < 3:
	execfile(activate_this, dict(__file__=activate_this))
else:
	with open(activate_this,"r") as file_:
		exec(file_.read(), dict(__file__=activate_this))
sys.path.append("/Users/apple/OneDrive - McGill University/FoodYummy/")
from app import create_app

application=create_app(config_name='default')