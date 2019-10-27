import airbnb
import listing
from datetime import datetime

date_1 = '2019-11-10'
date_2 = '2019-11-22'
api = airbnb.Api()


def main():
    days = days_between(date_1, date_2)
    search = api.get_homes('Carlsbad, CA', checkin='2019-11-10',checkout='2019-11-20', items_per_grid=100)
    for x in search['explore_tabs'][0]['sections']:
        if x['result_type'] == 'listings':
            listings = x['listings']
    list_of_homes = []

    for x in listings:
        real_price = x['pricing_quote']['price']['total']['amount']
        nightly_rate = int(real_price / days)
        listing_obj = x['listing']
        if 'neighborhood' in listing_obj:
            neighborhood = listing_obj['neighborhood']
        else:
            neighborhood = listing_obj['city']

        a_listing = listing.Listing(price=real_price, nightly_rate=nightly_rate, name=listing_obj['name'],
                                    bathrooms=listing_obj['bathrooms'], beds=listing_obj['beds'],
                                    neighborhood=neighborhood, listing_id=listing_obj['id'])
        list_of_homes.append(a_listing)

    sorta = sorted(list_of_homes, key=lambda listing:listing.nightly_rate)
    for x in sorta:
        print("Nightly rate: $", x.nightly_rate, "Name: ", x.name, " Area: ", x.neighborhood, " Total price: ", x.price)






"""
Print details about the request

 """

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

main()
