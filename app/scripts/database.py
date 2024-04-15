def get_restaurants(oyster, minutes_to_release, logger):
    try:
        # make query and process data
        restaurants = oyster['restaurants'].find({'minutes_to_release': minutes_to_release})
        restaurants_data = [{
            'venue_id': r['venue_id'],
            'days_to_release': r['days_to_release'],
            'minutes_to_release': r['minutes_to_release'],
            'name': r['name']
        } for r in restaurants]
        return restaurants_data   
    except Exception as e:
        logger.error(f"database connection issue: {e}")
        return None


def get_profiles(oyster, logger):
    try:
        # make query and process data
        profiles = oyster['profiles'].find({})
        profiles_data = [{
            '_id': p['_id'],
            'auth_token': p['auth_token'],
            'payment_method_id': p['payment_method_id']
        } for p in profiles]
        return profiles_data
    except Exception as e:
        logger.error(f"database connection issue: {e}")
        return None


def get_tables(oyster, venue_ids, logger):
    try:
        tables = oyster['tables'].find({"venue_id": {"$in": venue_ids}})
        tables_data = [{
            'venue_id': t['venue_id'],
            'template_id': t['template_id'],
            'service_id': t['service_id'],
            'time_string': t['time_string'],
            'party_size': t['party_size'],
            'table_type': t['venue_id'],
            '_id': t['_id'],
        } for t in tables]
        return tables_data
    except Exception as e:
        logger.error(f"database connection issue: {e}")
        return None