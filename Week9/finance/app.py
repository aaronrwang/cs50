import os
import datetime
import pytz

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, is_int

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT * FROM stocks WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
    totalValue = cash
    cash = usd(cash)
    for stock in stocks:
        price = lookup(stock['stock'])['price']
        shares = stock["shares"]
        total = price * float(shares)
        totalValue += total
        price = usd(price)
        total = usd(total)
        stock.update({'price': price})
        stock.update({'total': total})
    totalValue = usd(totalValue)
    return render_template("index.html", stocks=stocks, cash=cash, total=totalValue)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        values = lookup(symbol)

        if values == None:
            return apology("Invalid Symbol")
        if not request.form.get("shares"):
            return apology("Choose shares")
        shares = request.form.get("shares")
        if not is_int(shares):
            return apology("Invalid shares")
        if int(shares) < 1:
            return apology("Invalid shares")
        cost = values["price"] * float(shares)
        rows = db.execute("SELECT cash FROM users WHERE id = ? ", session["user_id"])
        cash = rows[0]["cash"]
        if cost > float(cash):
            return apology("You're broke")
        # update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
        # Add to stock table
        if db.execute("SELECT * FROM stocks WHERE id = ? AND stock = ?", session["user_id"], symbol):
            currShares = db.execute("SELECT * FROM stocks WHERE id = ? AND stock = ?", session["user_id"], symbol)[0]["shares"]
            totalShares = int(currShares) + int(shares)
            db.execute("UPDATE stocks SET shares = ? WHERE id = ? AND stock = ?", totalShares, session["user_id"], symbol)
        else:
            db.execute("INSERT INTO stocks (id, stock, shares) VALUES (?, ?, ?)", session["user_id"], symbol, shares)
        # update history
        time = datetime.datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO transactions (id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares, values["price"], time)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        values = lookup(request.form.get("symbol"))
        if values == None:
            return apology("Invalid Symbol")
        else:
            response = values["symbol"] + ": " + usd(values["price"])
            return render_template("quote.html", response=response)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        passwordConfirm = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if username == "" or password == "":
            return apology("blank field")
        elif passwordConfirm != password:
            return apology("Passwords do not match")
        elif rows:
            return apology("Username Taken")
        else:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # get data from html into python
        symbol = request.form.get("symbol")
        if not request.form.get("shares"):
            return apology("Choose shares")
        shares = int(request.form.get("shares"))
        if not is_int(shares):
            return apology("Invalid shares")
        if int(shares) < 1:
            return apology("Invalid shares")

        # make sure symbol is valid
        rows = db.execute("SELECT * FROM stocks WHERE id = ?", session["user_id"])

        if symbol == None:
            return apology("Choose a stock")
        valid = False
        for stock in rows:
            if stock["stock"] == symbol:
                valid = True
        if not valid:
            return apology("Don't Hack bro")
        currShares = int(db.execute("SELECT * FROM stocks WHERE stock = ? AND id = ?", symbol, session["user_id"])[0]["shares"])
        if shares > currShares:
            return apology("Too Many Shares")
        # change database for stocks
        totalShares = currShares - shares
        if totalShares == 0:
            db.execute("DELETE FROM stocks WHERE id = ? AND stock = ?", session["user_id"], symbol)
        else:
            db.execute("UPDATE stocks SET shares = ? WHERE id = ? AND stock = ?", totalShares, session["user_id"], symbol)
        # change database for cash
        currCash = float(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        cost = lookup(symbol)['price'] * float(shares)
        totalCash = currCash + cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", totalCash, session["user_id"])
        # update history
        time = datetime.datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO transactions (id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, 0-shares, lookup(symbol)['price'], time)
        return redirect("/")
    else:
        stocks = db.execute("SELECT stock FROM stocks WHERE id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        # check old password match
        passwordOld = request.form.get("password")
        passkey = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["hash"]
        print(check_password_hash(passkey, passwordOld))
        if not check_password_hash(passkey, passwordOld):
            return apology("Wrong Password")
        # check new matching passwords
        p1 = request.form.get("passwordNew")
        p2 = request.form.get("passwordNewConfirm")
        if p1 != p2:
            return apology("Passwords don't match")
        hash = generate_password_hash(p1)
        db.execute("UPDATE users set hash = ? WHERE id = ?", hash, session["user_id"])
        return redirect("/")
    return render_template("password.html")


def lookup(symbol):
    symbol = symbol.upper()
    if (symbol == "AAAA"):
        return {"name": "Stock A", "price": 28.00, "symbol": "AAAA"}
    elif (symbol == "BBBB"):
        return {"name": "Stock B", "price": 14.00, "symbol": "BBBB"}
    elif (symbol == "CCCC"):
        return {"name": "Stock C", "price": 2000.00, "symbol": "CCCC"}
    else:
        return None
