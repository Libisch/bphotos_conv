# -*- coding: utf-8 -*-

import json
import datetime
from slugify import slugify

input_file = open("bphotos.json", "r")
bdata = json.load(input_file)

# Slug.En
def slug(i):
    header = header_en(i)
    words = header.split(',')
    n_words = ""
    for word in words:
        n_words += word
    slug_ending = slugify(n_words, to_lower=True)
    slug = "image_{}".format(slug_ending)
    return slug

def date(i):
    date = bdata[i]['date'][0]
    return date

# UnitText1.En
def unit_text_en(i):
    text = bdata[i]['description_today'][0]
    photographer = bdata[i]['photographer'][0].strip()
    unit_text_en = ""
    if len(photographer) > 4:
        try:
            unit_text_en = "Today: {}.\nCourtesy of www.bagnowka.pl. Photographer: {}".format(text, photographer)
        except UnicodeEncodeError:
            unit_text_en = "Today: {}.\nCourtesy of www.bagnowka.pl".format(text)
    else:
        unit_text_en = "Today: {}.\nCourtesy of www.bagnowka.pl".format(text)
    return unit_text_en

# related ("place_[related place extracted from description]")
def related(i):
    text = bdata[i]['description_today'][0]
    find_place = text.split(',')
    place = lower(find_place[0])
    related = ["palce_{}".format(place)]
    return related

# UnitID, _id
def create_and_set_id(i):
    UnitId = "1111111111{}".format(i)
    # To be used for "_id" as well
    return UnitId

def gallery_name(i):
    gallery_name = bdata[i]['gallery_name'][0].strip()
    return gallery_name

# Header.En
def header_en(i):
    try:
        gallery_name = bdata[i]['gallery_name'][0].strip()
        photo_title = str(bdata[i]['photo_title'][0])
        if photo_title == "Email: ":
            photo_title = "null"
        date = bdata[i]['date'][0]
        header_en = ""
        if len(date) >= 4:
            if photo_title == "null" or photo_title == "None":
                header_en = "{}, {}".format(gallery_name, date)
            else:
                header_en = "{}, {}, {}".format(gallery_name, photo_title, date)
        else:
            if photo_title == "null" or photo_title == "None":
                header_en = "{}".format(gallery_name)
            else:
                header_en = "{}, {}".format(gallery_name, photo_title)
    except UnicodeEncodeError:
        header_en = "None"
    return header_en

# main_image_url
def main_image_url(i):
    main_image_url = "null"
    base_url = "https://s3-us-west-2.amazonaws.com/bagnowka-scraped/"
    if len(bdata[i]['images']) > 0:
        image_path = bdata[i]['images'][0]['path']
        main_image_url = "{}{}".format(base_url, image_path)
        return main_image_url
    else:
        main_image_url = "null"
        return main_image_url
# PictureId
def picture_id(i):
    if len(bdata[i]['images']) > 0:
        image_path = bdata[i]['images'][0]['path']
        split_path = image_path.split('/')
        p_id = split_path[1].split('.')
        picture_id = p_id[0]
        return picture_id
    else: 
        return "ERROR"

# thumbnail_url 
# TODO: change path from "full" to correct folder
def thumbnail_url(i):
    base_url = "https://s3-us-west-2.amazonaws.com/bagnowka-scraped/"
    image_path = bdata[i]['images'][0]['path']
    thumbnail_url = "{}{}".format(base_url, image_path)
    return thumbnail_url

def create_doc(i):
    currentDT = datetime.datetime.now()
    dt = currentDT.strftime("%Y-%m-%d{}%H:%M:%S{}".format("T", "Z"))
    photo_data = {"bagnowka":"True","RightsDesc":"Full","UpdateUser":"BH Online","UpdateDate":dt,"StatusDesc":"Completed","DisplayStatusDesc":"Museum and Internet","main_image_url": main_image_url(i),"Pictures":[{"PictureId":picture_id(i)}],"UnitPeriod":[{"PeriodDateTypeDesc":{"En":"Year","He":"שנים"},"PeriodDesc":{"En":date(i),"He":date(i)}}],"TS":"","UnitTypeDesc":"Photo","Slug":{"En":slug(i)},"UnitText1":{"En":unit_text_en(i)},"related":["place_belarus"],"PeriodDesc":{"En":date(i),"He":date(i)},"UnitHeaderDMSoundex":{"En":"","He":""},"UnitId":create_and_set_id(i),"_id":create_and_set_id(i),"Header":{"En":header_en(i)},"thumbnail_url":main_image_url(i)}
    return photo_data


def main():
    all_photos_array = []
    count = 0
    for i in range(len(bdata)):
        if main_image_url(i) == "null":
            pass
        elif header_en(i) == "None":
            pass
        else:
            doc = create_doc(i)
            all_photos_array.append(doc)
            count += 1
            print("Doc #{} added...".format(i))
    all_photos = json.dumps(all_photos_array)
    with open('all_photos_new_array.json', 'w') as file:
        file.write(all_photos)
    print("{} docs written to 'all_photos_new_array.json'".format(count))

if __name__ == '__main__':
    main()

    

