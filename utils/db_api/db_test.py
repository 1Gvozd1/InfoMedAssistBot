# import asyncio
# from db_gino import db
# import os
# import quick_commands as commands
# from data import config


# async def db_test():
#     await db.set_bind(config.POSTGRES_URI)
#     await db.gino.drop_all()
#     await db.gino.create_all()

#     await commands.add_user(1, 'Vlad', 'gregre')
#     await commands.add_user(2, 'terVlad', 'Тест')
#     await commands.add_user(3, 'Vletrd', 'werd')
#     await commands.add_user(100, 'etrd', '2134')
#     await commands.add_user(4, 'terad', '42334')

#     users = await commands.select_all_users()
#     print(users)

#     count = await commands.count_users()
#     print(count)

#     user = await commands.select_user(1)
#     print(user)

#     await commands.update_user_name(1, 'New name')

#     user = await commands.select_user(1)
#     print(user)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(db_test())
  