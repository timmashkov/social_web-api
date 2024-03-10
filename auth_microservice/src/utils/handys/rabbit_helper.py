from utils.handys.db_helpers.for_rabbit import get_profiles, get_groups, get_users


async def send_data_rpc():
    return await get_profiles(), await get_groups(), await get_users()
