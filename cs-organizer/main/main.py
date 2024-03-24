import os
import sys
import time
import random
import pathlib
import logging
import json
import uuid

SOURCE_PATH = pathlib.Path("source").absolute()
DEST_PATH = pathlib.Path("dest").absolute()
CUSTOM_FORMATS_PATH = pathlib.Path(f"{SOURCE_PATH}/custom-formats").absolute()

applications = {
  str(uuid.uuid1()): {
    "path": str(pathlib.Path(f"{CUSTOM_FORMATS_PATH}/sonarr").absolute()),
    "files": {},
    "database": {}
  },
  str(uuid.uuid1()): {
    "path": str(pathlib.Path(f"{CUSTOM_FORMATS_PATH}/radarr").absolute()),
    "files": {},
    "database": {}
  }
}

for _app_uuid in applications:
  for _app_files in os.listdir(applications[_app_uuid]['path']):
    _files_uuid = str(uuid.uuid1())
    _database_uuid = str(uuid.uuid1())

    applications[_app_uuid]['files'][_files_uuid] = {}
    applications[_app_uuid]["database"][_database_uuid] = {}

    applications[_app_uuid]['files'][_files_uuid].update({"full_name": _app_files})
    applications[_app_uuid]['files'][_files_uuid].update({"full_path": str(pathlib.Path(f"{applications[_app_uuid]['path']}/{_app_files}"))})
    applications[_app_uuid]['files'][_files_uuid].update({"raw_data": json.load(open(pathlib.Path(f"{applications[_app_uuid]['path']}/{_app_files}"), 'r'))})

    applications[_app_uuid]["database"][_database_uuid].update({"trash_id": applications[_app_uuid]['files'][_files_uuid]['raw_data']['trash_id']})
    applications[_app_uuid]["database"][_database_uuid].update({"trash_colection": applications[_app_uuid]['files'][_files_uuid]['raw_data']['name'].split(': ')[-0]})
    applications[_app_uuid]["database"][_database_uuid].update({"trash_name": applications[_app_uuid]['files'][_files_uuid]['raw_data']['name'].split(': ')[-1]})
    applications[_app_uuid]["database"][_database_uuid].update({"file_collection": applications[_app_uuid]['files'][_files_uuid]['full_name'].split('-')[-0]})
    applications[_app_uuid]["database"][_database_uuid].update({"file_name": applications[_app_uuid]['files'][_files_uuid]['full_name'].split('-')[-1].replace('.json','')})
    try:
      applications[_app_uuid]["database"][_database_uuid].update({"format_score": applications[_app_uuid]['files'][_files_uuid]['raw_data']['trash_scores']['default']})
    except:
      pass

print(json.dumps(applications,indent=2))
