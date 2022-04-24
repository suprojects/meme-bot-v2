from database import db

botusers = db["botusers"]


async def new(from_user):

    botusers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "username": from_user.username,
                "firstname": from_user.first_name,
                "lastname": from_user.last_name,
            }
        },
        upsert=True,
    )


async def users():
    return botusers.find()
