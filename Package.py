class Package:
    def __init__(self, package_id, address, city, state, zip_code, time_to_deliver, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.time_to_deliver = time_to_deliver
        self.weight = weight
        self.status = 'At the HUB'

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip_code, self.time_to_deliver, self.weight,
            self.status)

    def update_status(self, status):
        self.status = status

    def update_address(self, address):
        self.address = address

    def update_zip_code(self, zip_code):
        self.zip_code = zip_code
