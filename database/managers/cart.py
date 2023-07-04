from .base import Manager


class CartManager(Manager):
    def get_cart_info(self, user_id: int) -> list[tuple]:
        cart_id = self.get_cart_id(user_id)[0]
        sql = "select service_id, master_id, day, added_time, price from cart_products where cart_id = ?;"
        return self.manager(sql, cart_id, fetchall=True)

    def get_total_price(self, user_id: int) -> int:
        sql = "select total_price from cart where user_id = ?;"
        return self.manager(sql, user_id, fetchone=True)

    def get_cart_id(self, user_id: int) -> tuple:
        sql = "select cart_id from cart where user_id = ?;"
        return self.manager(sql, user_id, fetchone=True)

    def add_user_id(self, user_id: int) -> None:
        sql = "insert into cart(user_id) values (?);"
        self.manager(sql, user_id, commit=True)

    def update_cart(self, cart_id: int, service_id: int, master_id: int, day: str, added_time: str, price: int) -> None:
        self.database.cursor().executescript("""
            INSERT INTO cart_products(cart_id, service_id, master_id, day, added_time, price)
            VALUES ( '{cart_id}', '{service_id}', '{master_id}', '{day}', '{added_time}', '{price}' )
            ON CONFLICT (cart_id, service_id)
            DO UPDATE 
            SET price = cart_products.price + {price}
            WHERE cart_products.cart_id = {cart_id}
            AND cart_products.service_id = {service_id};

            UPDATE cart
            SET total_price = info.total_price

            FROM (
                SELECT SUM(price) AS total_price FROM cart_products
                WHERE cart_id = {cart_id}
            ) AS info;
        """.format(
            cart_id=cart_id,
            service_id=service_id,
            master_id=master_id,
            day=day,
            added_time=added_time,
            price=price,
        ))
        self.database.commit()
