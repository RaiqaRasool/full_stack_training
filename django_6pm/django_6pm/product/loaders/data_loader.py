import json
import os

from product.utils.utils import print_status_msg


class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.items = []

    def load_data(self):
        if not os.path.exists(self.filepath):
            print_status_msg("Given file does not exist", status="error")
            return self.items

        with open(self.filepath, "r") as f:
            try:
                self.items = json.load(f)
            except json.JSONDecodeError as e:
                print_status_msg(f"Error decoding JSON: {e}", status="error")
                return self.items
        print_status_msg("Read and parsed JSON data from file")
        return self.items
