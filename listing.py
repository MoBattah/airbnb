class Listing:
    def __init__(self, amenities, fake_price, price, monthly_rate, beds, bathrooms, neighborhood, name, nightly_rate, listing_id):
        self.price = price
        self.beds = beds
        self.bathrooms = bathrooms
        self.neighborhood = neighborhood
        self.name = name
        self.nightly_rate = nightly_rate
        self.id = listing_id
        self.fake_price = fake_price
        self.amenities = amenities
        self.monthly_rate = monthly_rate
