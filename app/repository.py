import json


class CustomerRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_all(self) -> dict:
        with open(self.db_path) as json_file:
            data = json.load(json_file)

        return data

    def get_by_id(self, id):
        data = self.get_all()
        if id in data:
            return data[id]

        return None

    def store(self, customer: dict):
        data = self.get_all()
        data["customers"].append(customer)
        with open(self.db_path, 'w') as outfile:
            json.dump(data, outfile)

        return True



