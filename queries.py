from db_connection import connect_db


class FoodDelivery:

    # =========================
    # CREATE ACCOUNT
    # =========================

    @staticmethod
    def create_account(name, email, password):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO user
            (
                name,
                email,
                password
            )
            VALUES
            (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                email,
                password
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return "inserted successfully"


    # =========================
    # LOGIN
    # =========================

    @staticmethod
    def login(email, password):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM user
            WHERE email = %s
            AND password = %s
        """

        cursor.execute(
            query,
            (
                email,
                password
            )
        )

        record = cursor.fetchone()

        cursor.close()
        conn.close()

        return record


    # =========================
    # GET PRODUCTS
    # =========================

    @staticmethod
    def get_products():

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM product
        """

        cursor.execute(query)

        record = cursor.fetchall()

        cursor.close()
        conn.close()

        return record


    # =========================
    # GET USER ID
    # =========================

    @staticmethod
    def get_user_id(email):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT id
            FROM user
            WHERE email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        record = cursor.fetchone()

        cursor.close()
        conn.close()

        if record:
            return record[0]

        return None


    # =========================
    # ADD CART
    # =========================

    @staticmethod
    def add_cart(user_id, product_id, quantity):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO cart
            (
                user_id,
                product_id,
                quantity
            )
            VALUES
            (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                product_id,
                quantity
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    # =========================
    # GET CART
    # =========================

    @staticmethod
    def get_cart(user_id):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                cart.id,
                cart.user_id,
                cart.product_id,
                cart.quantity,
                product.name,
                product.image,
                product.price

            FROM cart

            JOIN product
            ON cart.product_id = product.id

            WHERE cart.user_id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        record = cursor.fetchall()

        cursor.close()
        conn.close()

        return record


    # =========================
    # INCREASE QUANTITY
    # =========================

    @staticmethod
    def increase_quantity(user_id, product_id):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            UPDATE cart

            SET quantity = quantity + 1

            WHERE user_id = %s

            AND product_id = %s
        """

        cursor.execute(
            query,
            (
                user_id,
                product_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    # =========================
    # DECREASE QUANTITY
    # =========================

    @staticmethod
    def decrease_quantity(user_id, product_id):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            UPDATE cart

            SET quantity = quantity - 1

            WHERE user_id = %s

            AND product_id = %s

            AND quantity > 1
        """

        cursor.execute(
            query,
            (
                user_id,
                product_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    # =========================
    # REMOVE CART
    # =========================

    @staticmethod
    def remove_cart(user_id, product_id):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            DELETE FROM cart

            WHERE user_id = %s

            AND product_id = %s
        """

        cursor.execute(
            query,
            (
                user_id,
                product_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return "deleted successfully"


    # =========================
    # GET PROFILE
    # =========================

    @staticmethod
    def get_profile(email):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                u.id,
                u.name,
                u.email,
                p.phone,
                p.alternative_number,
                p.address

            FROM user u

            LEFT JOIN profile p
            ON u.id = p.user_id

            WHERE u.email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        record = cursor.fetchone()

        cursor.close()
        conn.close()

        return record


    # =========================
    # UPDATE PROFILE
    # =========================

    @staticmethod
    def update_profile(
        email,
        name,
        phone,
        alternative_number,
        address
    ):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            UPDATE user

            SET name = %s

            WHERE email = %s
        """

        cursor.execute(
            query,
            (
                name,
                email
            )
        )

        query = """
            SELECT id
            FROM user
            WHERE email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            cursor.close()
            conn.close()

            return "User not found"

        user_id = user[0]

        query = """
            SELECT id
            FROM profile
            WHERE user_id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        profile = cursor.fetchone()

        if profile:

            query = """
                UPDATE profile

                SET
                    phone = %s,
                    alternative_number = %s,
                    address = %s

                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    phone,
                    alternative_number,
                    address,
                    user_id
                )
            )

        else:

            query = """
                INSERT INTO profile
                (
                    user_id,
                    phone,
                    alternative_number,
                    address
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    user_id,
                    phone,
                    alternative_number,
                    address
                )
            )

        conn.commit()

        cursor.close()
        conn.close()

        return "updated successfully"


    # =========================
    # GET CHECKOUT USER
    # =========================

    @staticmethod
    def get_checkout_user(email):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                u.id,
                u.name,
                u.email,
                p.phone,
                p.address

            FROM user u

            LEFT JOIN profile p
            ON u.id = p.user_id

            WHERE u.email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user


    # =========================
    # GET CART ITEMS
    # =========================

    @staticmethod
    def get_cart_items(user_id):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                cart.id,
                cart.user_id,
                cart.product_id,
                cart.quantity,
                product.name,
                product.image,
                product.price

            FROM cart

            JOIN product
            ON cart.product_id = product.id

            WHERE cart.user_id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        cart_items = cursor.fetchall()

        cursor.close()
        conn.close()

        return cart_items


    # =========================
    # PLACE ORDER
    # =========================

    @staticmethod
    def place_order(
        email,
        name,
        phone,
        address,
        payment_method
    ):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        try:

            # GET USER

            query = """
                SELECT id
                FROM user
                WHERE email = %s
            """

            cursor.execute(
                query,
                (email,)
            )

            user = cursor.fetchone()

            if not user:

                raise Exception(
                    "User not found"
                )

            user_id = user["id"]


            # GET CART

            query = """
                SELECT
                    cart.product_id,
                    cart.quantity,
                    product.price

                FROM cart

                JOIN product
                ON cart.product_id = product.id

                WHERE cart.user_id = %s
            """

            cursor.execute(
                query,
                (user_id,)
            )

            cart_items = cursor.fetchall()

            if not cart_items:

                raise Exception(
                    "Cart is empty"
                )


            # CALCULATE TOTAL

            total_amount = 0

            for item in cart_items:

                total_amount += (
                    item["price"] *
                    item["quantity"]
                )


            # CREATE ORDER

            query = """
                INSERT INTO orders
                (
                    user_id,
                    name,
                    phone,
                    address,
                    total_amount,
                    payment_method,
                    status
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    user_id,
                    name,
                    phone,
                    address,
                    total_amount,
                    payment_method,
                    "Placed"
                )
            )

            order_id = cursor.lastrowid


            # CREATE ORDER ITEMS

            query = """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            for item in cart_items:

                cursor.execute(
                    query,
                    (
                        order_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"]
                    )
                )


            # CLEAR CART

            query = """
                DELETE FROM cart
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (user_id,)
            )


            # SAVE EVERYTHING

            conn.commit()

            return order_id


        except Exception:

            conn.rollback()

            raise


        finally:

            cursor.close()
            conn.close()


    # =========================
    # GET MY ORDERS
    # =========================

    @staticmethod
    def get_my_orders(user_id):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                o.id,
                o.user_id,
                o.name,
                o.phone,
                o.address,
                o.total_amount,
                o.payment_method,
                o.status,
                o.order_date

            FROM orders o

            WHERE o.user_id = %s

            ORDER BY o.order_date DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return orders


    # =========================
    # GET ORDER BY ID
    # =========================

    @staticmethod
    def get_order_by_id(order_id):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                user_id,
                name,
                phone,
                address,
                total_amount,
                payment_method,
                status,
                order_date

            FROM orders

            WHERE id = %s
        """

        cursor.execute(
            query,
            (order_id,)
        )

        order = cursor.fetchone()

        cursor.close()
        conn.close()

        return order


    # =========================
    # GET ORDER ITEMS
    # =========================

    @staticmethod
    def get_order_items(order_id):

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                oi.id,
                oi.order_id,
                oi.product_id,
                p.name,
                p.image,
                oi.quantity,
                oi.price

            FROM order_items oi

            JOIN product p
            ON oi.product_id = p.id

            WHERE oi.order_id = %s
        """

        cursor.execute(
            query,
            (order_id,)
        )

        order_items = cursor.fetchall()

        cursor.close()
        conn.close()

        return order_items


    # =========================
    # GET USER BY ID
    # =========================

    @staticmethod
    def get_user_by_id(user_id):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM user
            WHERE id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user











    #=======================================
    # Admin
    #=========================

    # =====================================================
    # GET ALL ORDERS FOR ADMIN
    # =====================================================

    @staticmethod
    def get_all_orders():

        conn = connect_db()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
            SELECT
                o.id,
                o.user_id,
                u.name AS customer_name,
                u.email,
                o.phone,
                o.address,
                o.total_amount,
                o.payment_method,
                o.status,
                o.order_date

            FROM orders o

            JOIN user u
            ON o.user_id = u.id

            ORDER BY o.order_date DESC
        """

        cursor.execute(query)

        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return orders

    # =====================================================
    # ADMIN DASHBOARD - TOTAL USERS
    # =====================================================

    @staticmethod
    def get_total_users():

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*)
            FROM user
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0]


    # =====================================================
    # ADMIN DASHBOARD - TOTAL ORDERS
    # =====================================================

    @staticmethod
    def get_total_orders():

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*)
            FROM orders
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0]


    # =====================================================
    # ADMIN DASHBOARD - TOTAL PRODUCTS
    # =====================================================

    @staticmethod
    def get_total_products():

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*)
            FROM product
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0]


    # =====================================================
    # ADMIN DASHBOARD - TOTAL SALES
    # =====================================================

    @staticmethod
    def get_total_sales():

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT COALESCE(SUM(total_amount), 0)
            FROM orders
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0]




