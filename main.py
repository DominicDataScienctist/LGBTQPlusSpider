import os
import argparse
import yaml

from utils import get_sheet_info, spider



parser = argparse.ArgumentParser(description="List fish in aquarium.")
parser.add_argument("--google_spreadsheet", "-s",  type=str, default='google_spreadsheet_url.yaml')
parser.add_argument("--google_cloud_config", "-g",  type=str, default='config.json')
args = parser.parse_args()


def main(arguments):
    cwd = os.getcwd()
    google_spreadsheet_config = os.path.join(cwd, arguments.google_spreadsheet)
    config = os.path.join(cwd, arguments.google_cloud_config)
    print(config)
    with open(google_spreadsheet_config, "r") as stream:
        try:
            google_spreadsheet_url = yaml.safe_load(stream)['url']
        except yaml.YAMLError as exc:
            google_spreadsheet_url = None

    worksheets, past_urls = get_sheet_info(config, google_spreadsheet_url)
    res_ap = spider(worksheets, past_urls)
    return res_ap


if __name__ == "__main__":
    main(args)



