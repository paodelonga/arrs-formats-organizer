import os
import shutil
import pathlib
import json
from uuid import uuid4

class Application:
  def __init__(self):
    self.SOURCE_PATH = pathlib.Path(f"{os.path.dirname(__file__)}/source").absolute()
    self.DEST_PATH = pathlib.Path(f"{os.path.dirname(__file__)}/dest").absolute()
    self.CUSTOM_FORMATS_PATH = pathlib.Path(f"{self.SOURCE_PATH}/custom-formats").absolute()

    [pathlib.Path(x).mkdir(exist_ok=True) for x in [self.DEST_PATH, self.SOURCE_PATH, self.CUSTOM_FORMATS_PATH]]

  def register_db(self):
    database = {
      'application': {
      }
    }

    for db_app in os.listdir(self.CUSTOM_FORMATS_PATH):
      database['application'].update({
        str(uuid4()): {
          'name': f"{db_app}",
          'path': f"{self.CUSTOM_FORMATS_PATH}/{db_app}",
          'custom_formats': {},
          'filtered_data': {}
        }
      })

    return database

  def read_db(self, new_db: dict):
    database = new_db
    for app_uuid in database['application']:
      for custom_format in os.listdir(database['application'][app_uuid]['path']):
        custom_format_uuid = str(uuid4())

        database['application'][app_uuid]['custom_formats'].update({
          custom_format_uuid: {
            'filename': custom_format,
            'path': f"{database['application'][app_uuid]['path']}/{custom_format}",
            'file_content': json.load(open(f"{database['application'][app_uuid]['path']}/{custom_format}", 'r'))
          }
        })

    return database

  def filter_db(self, raw_db: dict):
    database = raw_db
    for app_uuid in database['application']:
      for custom_format_uuid in database['application'][app_uuid]['custom_formats']:
        filtered_data_uuid = str(uuid4())

        database['application'][app_uuid]['filtered_data'].update({
          filtered_data_uuid: {
            'custom_format': {
              'relative_uuid': custom_format_uuid,
              'trash_id': f"{database['application'][app_uuid]['custom_formats'][custom_format_uuid]['file_content']['trash_id']}",
              'trash_score': '',
              'trash_collection': f"{database['application'][app_uuid]['custom_formats'][custom_format_uuid]['file_content']['name'].split(': ',1)[0]}",
              'trash_name': f"{database['application'][app_uuid]['custom_formats'][custom_format_uuid]['file_content']['name'].split(': ',1)[-1]}",
            },
            'file': {
              'fullpath': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['path'],
              'filename': {
                'old': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['filename'],
                'new': f"",
                'trash_collection': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['filename'].split('-',1)[0],
                'trash_name': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['filename'].split('-',1)[-1].replace('.json',''),
              },
              'content': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['file_content']
            }
          }
        })

        try:
          database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['custom_format'].update({
            'trash_score': database['application'][app_uuid]['custom_formats'][custom_format_uuid]['file_content']['trash_scores']['default']
          })
          database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename'].update({
            'new': '-'.join([
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['custom_format']['trash_score']),
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename']['trash_collection']),
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename']['trash_name'])
            ])
          })
        except KeyError as KE:
          database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['custom_format'].update({
            'trash_score': 0
          })
          database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename'].update({
            'new': '-'.join([
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['custom_format']['trash_score']),
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename']['trash_collection']),
              str(database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename']['trash_name'])
            ])
          })

    return database

  def save_files(self, db):
    database = db
    # print(json.dumps(database, indent=2))
    for app_uuid in database['application']:
      app_dest_path = pathlib.Path(f"{self.DEST_PATH}/custom-formats/{database['application'][app_uuid]['name']}")

      if app_dest_path.exists():
        shutil.rmtree(app_dest_path)

      app_dest_path.mkdir(parents=True, exist_ok=True)

      for filtered_data_uuid in database['application'][app_uuid]['filtered_data']:
        new_filename = database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['filename']['new']
        new_filepath = pathlib.Path(f"{app_dest_path}/{new_filename}.json")
        dump_filepath = pathlib.Path(f"{self.DEST_PATH}/custom-formats/dump.json")

        with open(new_filepath, 'w') as custom_format_file:
          json.dump(
            database['application'][app_uuid]['filtered_data'][filtered_data_uuid]['file']['content'],
            custom_format_file,
            indent=2
          )

        with open(dump_filepath, 'w') as dump_file:
          json.dump(database, dump_file, indent=2)


  def run(self):
    REGISTERED_DB = self.register_db()
    RAW_DB = self.read_db(REGISTERED_DB)
    FILTERED_DB = self.filter_db(RAW_DB)
    self.save_files(FILTERED_DB)

if __name__ == '__main__':
  app = Application()
  app.run()
