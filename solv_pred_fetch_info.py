#key func: fetch required information from the database (json)

def fetch_name(cas, db_json):

    for i, entry in enumerate(db_json):
        if cas == entry['CAS']:
            solv_name = entry['Name']
            
    return solv_name