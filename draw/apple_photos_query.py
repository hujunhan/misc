import osxphotos

photosdb = osxphotos.PhotosDB(osxphotos.utils.get_last_library_path())

# get data from each photo: date, location, places, title
# put into a dict, if without location, then skip
photos_with_location = photosdb.query(
    osxphotos.QueryOptions(location=True, not_shared=True)
)

print(len(photos_with_location))
print(
    photos_with_location[0].location,
    photos_with_location[0].date,
)
## output example:(35.19540333333333, -106.43543) 2023-11-26 17:01:29.422000-07:00

# save the data into a pickle file
import pickle

dump_dict = {}
for photo in photos_with_location:
    dump_dict[photo.uuid] = {
        "location": photo.location,
        "date": photo.date,
    }
filepath = "draw/photos_with_location.pkl"
with open(filepath, "wb") as f:
    pickle.dump(dump_dict, f)
