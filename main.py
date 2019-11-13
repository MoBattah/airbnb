import airbnb
import listing
from datetime import datetime

### PARAMETERS
date_1 = '2019-12-06'
date_2 = '2019-12-23'
location = 'Oceanside, CA'
private_entrance = True
api = airbnb.Api()


def main():
    days = days_between(date_1, date_2)
    search = api.get_homes(location, checkin=date_1,checkout=date_2, items_per_grid=100)
    for x in search['explore_tabs'][0]['sections']:
        if x['result_type'] == 'listings':
            listings = x['listings']
    list_of_homes = []

    for x in listings:
        real_price = x['pricing_quote']['price']['total']['amount']
        fake_rate = x['pricing_quote']['rate']['amount']
        fake_price = int(fake_rate) * int(days)
        nightly_rate = int(real_price / days)
        listing_obj = x['listing']
        if 'neighborhood' in listing_obj:
            neighborhood = listing_obj['neighborhood']
        else:
            neighborhood = listing_obj['city']

        amenities = listing_obj['amenity_ids']
        if 'beds' in listing_obj:
            pass
        else:
            listing_obj['beds'] = 1
        monthly_rate = nightly_rate * 30
        a_listing = listing.Listing(amenities = amenities, fake_price = fake_price, price=real_price, nightly_rate=nightly_rate,monthly_rate=monthly_rate, name=listing_obj['name'],
                                    bathrooms=listing_obj['bathrooms'], beds=listing_obj['beds'],
                                    neighborhood=neighborhood, listing_id=listing_obj['id'])
        list_of_homes.append(a_listing)
        print(real_price, a_listing.name)

    sorta = sorted(list_of_homes, key=lambda listing:listing.monthly_rate)
    for x in sorta:
        if 57 in x.amenities:
                print( "Name: ", x.name, " Area: ", x.neighborhood,"** Private Entrace **\n Nightly rate: $", x.nightly_rate,"\n Monthly rate: $", x.monthly_rate, "\n Total price: ", x.price, " Advertised Price: ", x.fake_price, "Difference :", x.fake_price - x.price, "\n Link: ", "https://airbnb.com/rooms/"+str(x.id))
        else:
            print("Name: ", x.name, " Area: ", x.neighborhood, "\n Nightly rate: $", x.nightly_rate,
                  "\n Monthly rate: $", x.monthly_rate, "\n Total price: ", x.price, " Advertised Price: ",
                  x.fake_price, "Difference :", x.fake_price - x.price, "\n Link: ",
                  "https://airbnb.com/rooms/" + str(x.id))


"""
Print details about the request

 """
#print("Request \nMarket: ", search['metadata']['geography']['market'])

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

main()
