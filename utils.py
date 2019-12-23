import json
import requests
#from numpy import vectorize

import constants
import pymysql.cursors


def insert_into_db(resource, name, status):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='avsystem',
                                 password='passw0rd',
                                 db='avsystem',
                                 charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `av_info` (`imei`, `name`, `status`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (resource, name, status))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        print("end")
        print(resource)
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()


def get_virus_infos(resource):
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": resource,
                  "apikey": "3f0498a1ae126f4fb78ece85a1a773d68208266ff27e430fe4add81fbf5af47b"}
    response = requests.get(url, params=parameters)
    print(response)
    res_json = response.json()
    print(res_json)
    virus_name = ""
    status = 0
    named = False
    if set_virus_name(res_json, constants.ClamAV) == "":
        if set_virus_name(res_json, constants.BKAV) != "":
            virus_name = set_virus_name(res_json, constants.BKAV)
            status += 100000
            named = True

        if set_virus_name(res_json, constants.MCAFEE) != "":
            if not named:
                virus_name = set_virus_name(res_json, constants.MCAFEE)
                named = True
            status += 10000

        if set_virus_name(res_json, constants.CMC) != "":
            if not named:
                virus_name = set_virus_name(res_json, constants.CMC)
                named = True
            status += 1000

        if set_virus_name(res_json, constants.KASPERSKY) != "":
            if not named:
                virus_name = set_virus_name(res_json, constants.KASPERSKY)
                named = True
            status += 100

        if set_virus_name(res_json, constants.MALWARE_BYTES) != "":
            if not named:
                virus_name = set_virus_name(res_json, constants.MALWARE_BYTES)
                named = True
            status += 10

        insert_into_db(resource, virus_name, status)

        return virus_name


def set_virus_name(response_dict, virus_type):
    # print(response_dict)

    if virus_type not in response_dict["scans"]:
        return ""
    virus_json_object = response_dict["scans"][virus_type]
    if virus_json_object["detected"]:
        return virus_json_object["result"]
    else:
        return ""


def get_maldb_ver():
    try:
        with open("./conf/db.ver") as f:
            return f.read()
    except IOError:
        print(
            "No malware DB version file found.\nPlease try to git clone the repository again.\n")
        return 0


def update_version(current_version):
    f = open("./conf/db.ver", 'w')
    f.write(str(current_version + 1))
    f.close()


