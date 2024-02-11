from datetime import timedelta, datetime
import requests
import pandas as pd
import calendar

api_key = "YOUR SERPAPI PRIVATE KEY"

locations = [
    'Adoni, Andhra Pradesh, India',
    'Amaravati, Andhra Pradesh, India',
    'Anantapur, Andhra Pradesh, India',
    'Port Blair, Andaman and Nicobar Islands, India',
    'Electronic city, Banglore, India',
    'Kormangala, Banglore, India',
    'Mysuru, Banglore, India',
    'Tumakuru, Banglore, India',
    'Whitefield, Banglore, India',
    'Sholinganalur, Chennai, India',
    'Ambatur, Chennai, India',
    'Anna Nagar, Chennai, India',
    'T.Nagar, Chennai, India',
    'Gachibowli, Hyderabad, India',
    'Madhapur, Hyderabad, India',
    'Banjara Hills, Hyderabad, India',
    'Ameerpet, Hyderabad, India'
]

data = []

for location in locations:
    query = f'restaurants near {location}'
    url = f"https://serpapi.com/search.json?engine=google_maps&q={query}&api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        results = response.json()
        local_results = results.get("local_results", [])

        for shop in local_results:
            keyword = query
            title = shop.get("title", " ")
            reviews = shop.get("reviews", " ")
            review_points = shop.get("rating", " ")
            address = shop.get("address", " ")
            opening_hours = shop.get("operating_hours", {})
            formatted_hours = []
            current_date = datetime.now()
            
            ordered_days = [day.capitalize() for day in calendar.day_name]
            
            for day in ordered_days:
                hours = opening_hours.get(day.lower(), '')
                formatted_hours.append(f"{day}: {hours.replace('\u202f', '')}  {current_date.strftime('%Y-%m-%d')}")
                current_date += timedelta(days=1)

            website = shop.get("website", "null")
            phone = shop.get("phone", "null")
            description = shop.get("description", "null")
            service_options = shop.get("service_options", {})
            dine_in = service_options.get("dine_in", False)
            takeout = service_options.get("takeout", False)
            delivery = service_options.get("delivery", False)
            order_online = shop.get("order_online", "null") 
            thumbnail = shop.get("thumbnail", "null")
            place_id = shop.get("place_id", "null")
            data_id = shop.get("data_id", "null")
            data_cid = shop.get("data_cid", "null")
            reviews_link = shop.get("reviews_link", "null")
            photos_link = shop.get("photos_link", "null")
            gps_coordinates = shop.get("gps_coordinates", {})
            latitude = gps_coordinates.get("latitude", " ")
            longitude = gps_coordinates.get("longitude", " ")
            place_id_search = shop.get("place_id_search", " ")
            provider_id = shop.get("provider_id", " ")
            rating = shop.get("rating", "null")
            price = shop.get("price", "null")
            restaurant_type = shop.get("type", " ")
            types = shop.get("types", " ")
            data.append({
                "keyword": keyword,
                "Title": title,
                "Reviews": reviews,
                "Review_points": review_points,
                "Address": address,
                "Opening_Hours": formatted_hours,
                "Website": website,
                "Description": description,
                "Dine_In": dine_in,
                "Takeout": takeout,
                "Delivery": delivery,
                "Order_Online": order_online,
                "Thumbnail": thumbnail,
                "Place_ID": place_id,
                "Data_ID": data_id,
                "Data_CID": data_cid,
                "Reviews_Link": reviews_link,
                "Photos_Link": photos_link,
                "Latitude": latitude,
                "Longitude": longitude,
                "Place_ID_Search": place_id_search,
                "Provider_ID": provider_id,
                "Rating": rating,
                "Price": price,
                "Restaurant_Type": restaurant_type,
                "Types": types,
                "Monday_Opening_Time": formatted_hours[0].split()[1],  
                "Tuesday_Opening_Time": formatted_hours[1].split()[1],  
                "Wednesday_Opening_Time": formatted_hours[2].split()[1],  
                "Thursday_Opening_Time": formatted_hours[3].split()[1],  
                "Friday_Opening_Time": formatted_hours[4].split()[1],  
                "Saturday_Opening_Time": formatted_hours[5].split()[1], 
                "Sunday_Opening_Time": formatted_hours[6].split()[1], 
            })
    else:
        print(f"Failed to retrieve data for {location}. Status code: {response.status_code}")


df = pd.DataFrame(data)

df.to_excel("restaurants_all_locations.xlsx", index=False)
print("Data exported to 'restaurants_all_locations.xlsx'")
