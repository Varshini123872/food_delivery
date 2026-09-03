from flask import *

from queries import FoodDelivery


app = Flask(__name__)

app.secret_key = "mysecretkey"


# =====================================================
# SIGNUP
# =====================================================

@app.route("/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        try:

            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]

            FoodDelivery.create_account(
                name,
                email,
                password
            )

            flash("Account created successfully")

            return redirect("/signin")

        except Exception as e:

            print("SIGNUP ERROR:", e)

            return "Not inserted successfully"

    return render_template("sign_up.html")


# =====================================================
# LOGIN
# =====================================================

@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = FoodDelivery.login(
            email,
            password
        )

        print("LOGIN USER:", user)

        if user:

            # VERY IMPORTANT

            session["user_id"] = user[0]
            session["user_email"] = email

            print(
                "USER ID:",
                session["user_id"]
            )

            print(
                "SESSION:",
                session
            )

            return redirect(
                url_for("home")
            )

        else:

            msg = "Invalid username or password"

            return render_template(
                "sign_in.html",
                msg=msg
            )

    return render_template("sign_in.html")


# =====================================================
# HOME
# =====================================================

@app.route("/home")
def home():

    if "user_email" not in session:

        return redirect("/signin")

    products = FoodDelivery.get_products()

    return render_template(
        "home_page.html",
        products=products
    )


# =====================================================
# ADD TO CART
# =====================================================

@app.route(
    "/add_to_cart",
    methods=["POST"]
)
def add_to_cart():

    if "user_email" not in session:

        return "Login required", 401

    product_id = request.form.get(
        "product_id"
    )

    if not product_id:

        return "Product ID is missing", 400

    email = session["user_email"]

    user_id = FoodDelivery.get_user_id(
        email
    )

    if not user_id:

        return "User not found", 404

    FoodDelivery.add_cart(
        user_id,
        product_id,
        1
    )

    return "Added to cart", 200


# =====================================================
# CART
# =====================================================

@app.route("/cart")
def cart():

    if "user_email" not in session:

        return redirect("/signin")

    user_id = FoodDelivery.get_user_id(
        session["user_email"]
    )

    if not user_id:

        return redirect("/signin")

    cart_items = FoodDelivery.get_cart(
        user_id
    )

    return render_template(
        "cart.html",
        cart_items=cart_items
    )


# =====================================================
# INCREASE QUANTITY
# =====================================================

@app.route(
    "/increase_quantity",
    methods=["POST"]
)
def increase_quantity():

    if "user_email" not in session:

        return redirect("/signin")

    product_id = request.form.get(
        "product_id"
    )

    if not product_id:

        return "Product ID is missing", 400

    user_id = FoodDelivery.get_user_id(
        session["user_email"]
    )

    FoodDelivery.increase_quantity(
        user_id,
        product_id
    )

    return redirect("/cart")


# =====================================================
# DECREASE QUANTITY
# =====================================================

@app.route(
    "/decrease_quantity",
    methods=["POST"]
)
def decrease_quantity():

    if "user_email" not in session:

        return redirect("/signin")

    product_id = request.form.get(
        "product_id"
    )

    if not product_id:

        return "Product ID is missing", 400

    user_id = FoodDelivery.get_user_id(
        session["user_email"]
    )

    FoodDelivery.decrease_quantity(
        user_id,
        product_id
    )

    return redirect("/cart")


# =====================================================
# REMOVE CART
# =====================================================

@app.route(
    "/remove_from_cart",
    methods=["POST"]
)
def remove_from_cart():

    if "user_email" not in session:

        return "Login required", 401

    product_id = request.form.get(
        "product_id"
    )

    if not product_id:

        return "Product ID is missing", 400

    user_id = FoodDelivery.get_user_id(
        session["user_email"]
    )

    FoodDelivery.remove_cart(
        user_id,
        product_id
    )

    return redirect("/cart")


# =====================================================
# CHECKOUT
# =====================================================

@app.route("/checkout")
def checkout():

    if "user_email" not in session:

        return redirect("/signin")

    email = session["user_email"]

    user = FoodDelivery.get_checkout_user(
        email
    )

    if not user:

        return redirect("/signin")

    return render_template(
        "checkout.html",
        user=user
    )


# =====================================================
# PLACE ORDER
# =====================================================

@app.route(
    "/place_order",
    methods=["POST"]
)
def place_order():

    if "user_email" not in session:

        return redirect("/signin")

    email = session["user_email"]

    name = request.form.get("name")
    phone = request.form.get("phone")
    address = request.form.get("address")

    payment_method = request.form.get(
        "payment_method"
    )

    print("ORDER EMAIL:", email)
    print("NAME:", name)
    print("PHONE:", phone)
    print("ADDRESS:", address)
    print("PAYMENT:", payment_method)

    try:

        order_id = FoodDelivery.place_order(
            email,
            name,
            phone,
            address,
            payment_method
        )

        print(
            "ORDER CREATED:",
            order_id
        )

        return redirect(
            url_for("order_success")
        )

    except Exception as e:

        print(
            "ORDER ERROR:",
            e
        )

        return "Order could not be placed"


# =====================================================
# ORDER SUCCESS
# =====================================================

@app.route("/order_success")
def order_success():

    if "user_email" not in session:

        return redirect("/signin")

    return render_template(
        "order_success.html"
    )


# =====================================================
# MY ORDERS
# =====================================================

@app.route("/orders")
def my_orders():

    if "user_id" not in session:

        return redirect("/signin")

    user_id = session["user_id"]

    print(
        "MY ORDERS USER ID:",
        user_id
    )

    orders = FoodDelivery.get_my_orders(
        user_id
    )

    print(
        "MY ORDERS:",
        orders
    )

    return render_template(
        "my_orders.html",
        orders=orders
    )


# =====================================================
# SINGLE ORDER
# =====================================================

@app.route("/order/<int:order_id>")
def view_order(order_id):

    if "user_id" not in session:

        return redirect("/signin")

    order = FoodDelivery.get_order_by_id(
        order_id
    )

    if not order:

        return "Order not found", 404

    if order["user_id"] != session["user_id"]:

        return "Unauthorized", 403

    order_items = FoodDelivery.get_order_items(
        order_id
    )

    return render_template(
        "order_details.html",
        order=order,
        order_items=order_items
    )


# =====================================================
# PROFILE
# =====================================================

@app.route("/profile")
def profile():

    if "user_email" not in session:

        return redirect("/signin")

    profile_data = FoodDelivery.get_profile(
        session["user_email"]
    )

    return render_template(
        "profile.html",
        profile=profile_data
    )


# =====================================================
# UPDATE PROFILE
# =====================================================

@app.route(
    "/update_profile",
    methods=["POST"]
)
def update_profile():

    if "user_email" not in session:

        return "Login required", 401

    email = session["user_email"]

    name = request.form.get("name")
    phone = request.form.get("phone")

    alternative_number = request.form.get(
        "alternative_number"
    )

    address = request.form.get(
        "address"
    )

    FoodDelivery.update_profile(
        email,
        name,
        phone,
        alternative_number,
        address
    )

    return "Profile updated successfully", 200



# =====================================================
# ADMIN LOGIN
# =====================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Temporary admin credentials
        if email == "admin@gmail.com" and password == "admin123":

            session["admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        else:

            return render_template(
                "admin_login.html",
                msg="Invalid Admin Email or Password"
            )

    return render_template(
        "admin_login.html"
    )


# =====================================================
# ADMIN LOGOUT
# =====================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(
        url_for("admin_login")
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:

        return redirect(
            url_for("admin_login")
        )

    total_users = FoodDelivery.get_total_users()

    total_orders = FoodDelivery.get_total_orders()

    total_products = FoodDelivery.get_total_products()

    total_sales = FoodDelivery.get_total_sales()

    return render_template(
        "admin_dashboard.html",

        total_users=total_users,

        total_orders=total_orders,

        total_products=total_products,

        total_sales=total_sales
    )

# =====================================================
# ADMIN ORDERS
# =====================================================

@app.route("/admin/orders")
def admin_orders():

    # Check admin login
    if "admin" not in session:

        return redirect(
            url_for("admin_login")
        )

    # Get all orders from database
    orders = FoodDelivery.get_all_orders()

    return render_template(
        "admin_orders.html",
        orders=orders
    )


























# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/signin")


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )