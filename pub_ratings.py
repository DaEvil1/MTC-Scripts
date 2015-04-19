import urllib.request, csv, string, re, datetime

from bs4 import BeautifulSoup

ratings_url = "http://tagpro-origin.koalabeast.com/maps"


def get_mapnames(in_string):
    maps = []
    str_beg = "</tr><tr><td>"
    str_end = "</td><td>"
    map_end = 1
    old_map_end = 0
    position = 0
    while old_map_end <= map_end:
        old_map_end = map_end
        map_beg = in_string.find(str_beg, position) + len(str_beg)
        map_end = in_string.find(str_end, map_beg)
        position = map_end
        maps.append(in_string[map_beg:map_end])
    return maps[:-1]

def fix_str(in_string):
    cleanup =[">", "<", "/", "\"", "=", ":", "%"]

    replaced = {"span", "tdtd", "class", "indifferent", "like", "dislike", 
                "noPaddiv", "ratio", "style", "width", "dis", "divtdtrtrtd"
            }
    out_string = in_string[1136:]
    for element in cleanup:
        out_string = out_string.replace(element, "")
    for element in replaced:
        out_string = out_string.replace(element, ", ")
    while " " in out_string:
        out_string = out_string.replace(" ", "")
    while ",," in out_string:
        out_string = out_string.replace(",,", ",")
    #out_string = out_string[:-27]
    #print(out_string)
    return out_string

def fix_names(in_string, mapnames):
    out_string = in_string
    nospace = []
    for i in mapnames:
        while " " in i:
            i = i.replace(" ", "")
        nospace.append(i)
    for i in range(len(nospace)):
        out_string = out_string.replace(nospace[i], mapnames[i])
    return out_string

def get_data(in_string):
    info = ["name", "rating", "ratings", "plays", "liked", "indifferent", "disliked"]
    data = in_string.split(",")
    out_data = []
    cur_dict = {}
    for i in range(len(data)):
        cur_object = i % 7
        cur_dict[info[cur_object]] = data[i]
        if cur_object == 6:
            out_data.append(cur_dict)
            cur_dict = {}
    return out_data

def write_csv(in_data):
    filename = "pub_ratings_{}.txt".format(datetime.date.today().strftime("%B_%d_%Y")) 
    out_strings= []
    print(in_data[-1])
    for element in in_data:
        out = [element["name"], element["rating"]]
        out_strings.append(out)
    with open(filename, "w") as f:
        a = csv.writer(f, delimiter='\t', lineterminator='\n')
        a.writerows(out_strings)



def main():
    data = urllib.request.urlopen(ratings_url)
    page = BeautifulSoup(data)
    page_str = str(page)
    mapnames = get_mapnames(page_str)
    page_str = fix_str(page_str)
    page_str = fix_names(page_str, mapnames)
    page_data = get_data(page_str)
    write_csv(page_data)



if __name__ == "__main__":
    main()


