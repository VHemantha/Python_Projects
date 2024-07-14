import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import re

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    usernam = session.get("user_id")
    cih = db.execute("SELECT * FROM users WHERE id = ?", usernam)
    username = cih[0]["username"]
    db.execute("CREATE TABLE IF NOT EXISTS ? (id INTEGER NOT NULL PRIMARY KEY ,symbol TEXT NOT NULL, name TEXT NOT NULL, shares NUMERIC NOT NULL, price NUMERIC NOT NULL, date INT)", username)
    foo = db.execute("SELECT * FROM ?", username)
    for row in foo:
        s_symbol = row["symbol"]
        new_prices = lookup(s_symbol)
        price = new_prices["price"]
        db.execute("CREATE TABLE IF NOT EXISTS current_prices (id INTEGER NOT NULL PRIMARY KEY ,symbol TEXT NOT NULL,  cprice NUMERIC NOT NULL)")
        if not db.execute("SELECT symbol FROM current_prices WHERE symbol = ?", s_symbol):
            db.execute("INSERT INTO current_prices (symbol,cprice) VALUES(?, ?)", s_symbol, price)
        else:
            db.execute("UPDATE current_prices SET cprice = ? WHERE symbol = ?", price, s_symbol)

    data = db.execute("SELECT ?.symbol,?.name,SUM(?.shares) As shares,?.price,current_prices.cprice FROM ? INNER JOIN current_prices ON ?.symbol=current_prices.symbol GROUP BY ?.symbol",
                      username, username, username, username, username, username, username)
    return render_template("index.html", portfolio=data, cash=cih[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = request.form.get("symbol")
        shares = request.form.get("shares")
        if not lookup(request.form.get("symbol")):
            return apology("Enter valid stock symbol")

        if not request.form.get("shares").isnumeric() or int(shares) < 1:
            return apology("Number of shares should be greter than 0 not blank")

        stock_data = lookup(stock)
        usernam = session.get("user_id")
        cashr = float(stock_data["price"]) * int(shares)
        cih = db.execute("SELECT * FROM users WHERE id = ?", usernam)
        cihn = cih[0]["cash"]
        if cashr > cihn:
            return apology("Do not have enough cash to purchase")

        else:
            username = cih[0]["username"]
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            ccash = cihn - (int(shares) * (int(stock_data["price"])))
            db.execute("CREATE TABLE IF NOT EXISTS ? (id INTEGER NOT NULL PRIMARY KEY ,symbol TEXT NOT NULL, name TEXT NOT NULL, shares NUMERIC NOT NULL, price NUMERIC NOT NULL, date INT)", username)
            db.execute("INSERT INTO ? (symbol,name,shares,price,date) VALUES(?, ?, ?,?,?)",
                       username, stock, stock_data["name"], shares, int(stock_data["price"]), dt_string)
            db.execute("UPDATE users SET cash = ? WHERE username = ?", ccash, username)
            return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    usernam = session.get("user_id")
    cih = db.execute("SELECT * FROM users WHERE id = ?", usernam)
    username = cih[0]["username"]
    data = db.execute("SELECT * FROM ?", username)
    return render_template("history.html", history=data)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/changepassword", methods=["GET", "POST"])
def change():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Enter username")
        elif not db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username")):
            return apology("Invalid username")
        elif not request.form.get("password"):
            return apology("No Password Found")

        else:
            password_hash = generate_password_hash(request.form.get("password"))
            db.execute("UPDATE users SET hash = ? WHERE username = ?", password_hash, request.form.get("username"))
            flash("Password update successful")
            return render_template("login.html")
    return render_template("changepassword.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("Enter valid stock symbol")

        else:
            sym = request.form.get("symbol")
            symdata = lookup(sym)
            return render_template("quoted.html", data=symdata)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure No duplicate users
        elif db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username")):
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif not re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', request.form.get("password")):
            flash("Password must have 8 chacters with number symbol and lowere and uppercase letters")
            return apology("Weak Password", 400)

        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("Password Doesn't Match", 400)

        # generate password hash
        else:
            uname = request.form.get("username")
            password_hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", str(uname), password_hash)
            flash("Successfully Registered !")
            return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    usernam = session.get("user_id")
    cih = db.execute("SELECT * FROM users WHERE id = ?", usernam)
    username = cih[0]["username"]
    data = db.execute("SELECT DISTINCT(symbol) FROM ?", username)
    if request.method == "POST":
        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        sh = db.execute("SELECT SUM(shares) AS shares FROM ? WHERE symbol = ?", username, stock)
        num_shares = int(sh[0]["shares"])
        if not request.form.get("shares").isnumeric() or int(shares) < 1:
            return apology("Number of shares should be greter than 0")
        elif shares > num_shares:
            return apology("Do not have enough shares to sell")
        else:
            share = shares * -1
            stock_data = lookup(stock)
            now = datetime.now()
            ccash = cih[0]["cash"] + (shares * (int(stock_data["price"])))
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            db.execute("INSERT INTO ? (symbol,name,shares,price,date) VALUES(?, ?, ?,?,?)",
                       username, stock, stock_data["name"], share, int(stock_data["price"]), dt_string)
            db.execute("UPDATE users SET cash = ? WHERE username = ?", ccash, username)
            return redirect("/")

    return render_template("sell.html", symbol=data)