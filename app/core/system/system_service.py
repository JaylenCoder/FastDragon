# -*- coding: utf-8 -*-
# @Time    : 2022/02/12 21:01:19
# @File    : system_service.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from app.core.system.system_schema import PersonalAccount
from app.main.database import CRUDMixin, m2d, mysql_async
from app.models.peewee.fast_dragon import User
from app.utils.run_async import fast_async


class DemoClass(CRUDMixin):
    model = User

    async def demo_orm(self):
        # saa = await mysql_async.create(User, uid="343as34535", user_name="testa33_33333dd_ss")
        # print(saa)

        # query_data = await User.select().where(User.user_name == "test_dd_ss")
        # print([i.user_name for i in query_data])
        asd = await self.find_one(User.user_name == "testa33_dd_ss")
        # asd = await self.find("user_name", **{"user_name": "testa33_dd_ss"})
        print(asd)
        # ddd = PersonalAccount(**m2d(asd))
        # print(ddd)
        # return ddd.dict()
        # print(ddd(asd))
        # for i in m2d(asd):
        #     print(i)
        return m2d(asd)


# def get_user_by_email(email: str):
#     return models.User.filter(models.User.email == email).first()
#
#
# def get_users(skip: int = 0, limit: int = 100):
#     return list(models.User.select().offset(skip).limit(limit))
#
#
# def create_user(user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db_user.save()
#     return db_user
#
#
# def get_items(skip: int = 0, limit: int = 100):
#     return list(models.Item.select().offset(skip).limit(limit))
#
#
# def create_user_item(item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db_item.save()
#     return db_item

if __name__ == '__main__':
    print(fast_async(DemoClass().demo_orm()))
    # get_user(2)
