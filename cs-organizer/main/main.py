import os
import sys
import time
import random
import pathlib
import logging
import json
import uuid

# Enviroments
SOURCE_PATH = pathlib.Path(f"{os.path.dirname(__file__)}/source").absolute()
DEST_PATH = pathlib.Path(f"{os.path.dirname(__file__)}/dest").absolute()
CUSTOM_FORMATS_PATH = pathlib.Path(f"{SOURCE_PATH}/custom-formats").absolute()

# Aplications
applications = {
  str(uuid.uuid1()): {
    'path': str(pathlib.Path(f"{CUSTOM_FORMATS_PATH}/sonarr").absolute()),
    'raw_data': {},
    'cooked_data': {}
  },
  str(uuid.uuid1()): {
    'path': str(pathlib.Path(f"{CUSTOM_FORMATS_PATH}/radarr").absolute()),
    'raw_data': {},
    'cooked_data': {}
  }
}

# Rawdata
for _app_uuid in applications:
  for _app_files in os.listdir(applications[_app_uuid]['path']):
    _file_uuid = str(uuid.uuid1())
    applications[_app_uuid]['raw_data'][_file_uuid] = {}

    applications[_app_uuid]['raw_data'][_file_uuid].update({'full_name': _app_files})
    applications[_app_uuid]['raw_data'][_file_uuid].update({'full_path': str(pathlib.Path(f"{applications[_app_uuid]['path']}/{_app_files}"))})
    applications[_app_uuid]['raw_data'][_file_uuid].update({'raw_data': json.load(open(pathlib.Path(f"{applications[_app_uuid]['path']}/{_app_files}"), 'r'))})

# Processed data
for _app_uuid in applications:
  for _file_uuid in applications[_app_uuid]['raw_data']:
    _item_uuid = str(uuid.uuid1())
    applications[_app_uuid]['cooked_data'][_item_uuid] = {}

    applications[_app_uuid]['cooked_data'][_item_uuid].update({'trash_id': applications[_app_uuid]['raw_data'][_file_uuid]['raw_data']['trash_id']})
    applications[_app_uuid]['cooked_data'][_item_uuid].update({'trash_colection': applications[_app_uuid]['raw_data'][_file_uuid]['raw_data']['name'].split(': ')[-0]})
    applications[_app_uuid]['cooked_data'][_item_uuid].update({'trash_name': applications[_app_uuid]['raw_data'][_file_uuid]['raw_data']['name'].split(': ')[-1]})
    applications[_app_uuid]['cooked_data'][_item_uuid].update({'file_collection': applications[_app_uuid]['raw_data'][_file_uuid]['full_name'].split('-')[-0]})
    applications[_app_uuid]['cooked_data'][_item_uuid].update({'file_name': applications[_app_uuid]['raw_data'][_file_uuid]['full_name'].split('-')[-1].replace('.json','')})
    try:
      applications[_app_uuid]['cooked_data'][_item_uuid].update({'trash_scores': applications[_app_uuid]['raw_data'][_file_uuid]['raw_data']['trash_scores']['default']})
    except:
      pass

json.dump(applications,open(f"{DEST_PATH}/dump.json", 'w'),indent=2)


# On terminal run `main.py | sort -rn`
for a in applications:
  for b in applications[a]['cooked_data']:
    # for c in applications[a]['cooked_data'][c]:
    try:
      print(f"{applications[a]['cooked_data'][b]['trash_scores']}.{applications[a]['cooked_data'][b]['file_collection']}.{applications[a]['cooked_data'][b]['file_name']}.json")
    except:
      pass
