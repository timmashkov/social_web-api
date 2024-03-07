from utils.handys.db_helpers.for_rabbit import get_profiles, get_groups


async def send_profiles_rpc():
    return await get_profiles(), await get_groups()


async def send_groups_rpc():
    return await get_groups()
