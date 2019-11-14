import airbnb
import listing
from datetime import datetime

### PARAMETERS
date_1 = '2019-12-01'
date_2 = '2019-12-16'
location = 'Carlsbad, CA'
private_entrance = True



def main():
    list_of_listings = search_and_collect_listings(date_1, date_2)
    list_of_homes = create_listing_classes(list_of_listings)
    sort_and_print_listings(list_of_homes)



def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def search_and_collect_listings(date_1, date_2):
    api = airbnb.Api()
    search = api.get_homes(location, checkin=date_1, checkout=date_2, items_per_grid=100)
    list_of_listings = []

    ##This will find the listings section and assign raw_listings to the array.
    for x in search['explore_tabs'][0]['sections']:
        if x['result_type'] == 'listings':
            raw_listings = x['listings']
            for x in raw_listings:
                list_of_listings.append(x)
            print("Found ", len(raw_listings), " listings!")
    return list_of_listings


def create_listing_classes(list_of_listings):
    list_of_homes = []
    days = days_between(date_1, date_2)
    for x in list_of_listings:
        #If statement adds San Diego and Oceanside taxes. Applies flat 10% tax.
        if x['listing']['city'] == 'San Diego' or 'Oceanside':
            untaxed_price = int(x['pricing_quote']['price']['total']['amount'])
            real_price = untaxed_price + untaxed_price * .10
        else:
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
        a_listing = listing.Listing(amenities=amenities, fake_price=fake_price, price=real_price,
                                    nightly_rate=nightly_rate, monthly_rate=monthly_rate, name=listing_obj['name'],
                                    bathrooms=listing_obj['bathrooms'], beds=listing_obj['beds'],
                                    neighborhood=neighborhood, listing_id=listing_obj['id'])
        list_of_homes.append(a_listing)
    return list_of_homes


def sort_and_print_listings(list_of_homes):
    listings_by_monthly_rate = sorted(list_of_homes, key=lambda listing: listing.monthly_rate)
    print("Total listings: ", len(list_of_homes))
    for x in listings_by_monthly_rate:
        difference = int(x.fake_price - x.price)
        if 57 in x.amenities:
            print("Name: ", x.name, " Area: ", x.neighborhood, "** Private Entrace **\n Nightly rate: $",
                  x.nightly_rate, "\n Monthly rate: $", x.monthly_rate, "\n Total price: ", x.price,
                  " Advertised Price: ", x.fake_price, "Difference :", difference, "\n Link: ",
                  "https://airbnb.com/rooms/" + str(x.id))
        else:
            print("Name: ", x.name, " Area: ", x.neighborhood, "\n Nightly rate: $", x.nightly_rate,
                  "\n Monthly rate: $", x.monthly_rate, "\n Total price: ", x.price, " Advertised Price: ",
                  x.fake_price, "Difference :", difference, "\n Link: ",
                  "https://airbnb.com/rooms/" + str(x.id))

main()
