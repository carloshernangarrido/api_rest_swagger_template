import sqlalchemy
from secret import db
from flask import abort, make_response

engine = sqlalchemy.engine.create_engine(
    f"mysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}")


def read_all():
    with engine.connect() as con:
        con.execute('USE sql_store')
        rs = con.execute('SELECT *\n'
                         'FROM customers')
        l_rs = [dict(_) for _ in rs]
    return l_rs


def create(customer):
    last_name = customer.get("last_name")
    first_name = customer.get("first_name")
    with engine.connect() as con:
        con.execute('USE sql_store')
        rs = con.execute(f'SELECT *\n'
                         f'FROM customers\n'
                         f'WHERE last_name = "{last_name}"'
                         f'AND first_name = "{first_name}"')
        a = [dict(u) for u in rs]
    if len(a) == 0:
        with engine.connect() as con:
            con.execute('USE sql_store;')
            con.execute(f'INSERT INTO sql_store.customers (first_name, last_name)\n'
                        f'VALUES ("{first_name}", "{last_name}");')
    else:
        abort(406,
              f"Customer with last name {last_name} and first name {first_name} "
              f"already exists"
              )


def read_one(first_name_last_name):
    first_name, last_name = first_name_last_name.split('_')
    with engine.connect() as con:
        con.execute('USE sql_store')
        rs = con.execute(f'SELECT *\n'
                         f'FROM customers\n'
                         f'WHERE binary last_name = "{last_name}"\n'
                         f'AND binary first_name = "{first_name}"')
        l_rs = [dict(_) for _ in rs]
    if len(l_rs) == 1:
        return l_rs
    elif len(l_rs) == 0:
        abort(404, f"Customer with first name {first_name} and last name {last_name}"
                   f" was not found")
    else:
        abort(404, "More than one customers has that first and last name")


def update(first_name_last_name, customer):
    l_rs = read_one(first_name_last_name)
    raw = f"UPDATE customers\n" \
          f"SET last_name = '{customer['last_name']}'"
    if 'first_name' in customer.keys():
        raw += f", first_name = '{customer['first_name']}'"
    if 'birth_date' in customer.keys():
        raw += f"' birth_date = '{customer['birth_date']}"
    raw += f"\nWHERE customer_id = {l_rs[0]['customer_id']}"
    with engine.connect() as con:
        con.execute('USE sql_store;')
        con.execute(raw)
    with engine.connect() as con:
        con.execute('USE sql_store')
        raw = f'SELECT *\n'\
              f'FROM customers\n'\
              f'WHERE binary last_name = "{customer["last_name"]}"\n'
        if 'first_name' in customer.keys():
            raw += f'AND binary first_name = "{customer["first_name"]}"'
        else:
            raw += f'AND binary first_name = "{first_name}"'
        rs = con.execute(raw)
        return [dict(_) for _ in rs]


def delete(first_name_last_name):
    l_rs = read_one(first_name_last_name)
    with engine.connect() as con:
        con.execute('USE sql_store')
        con.execute(f'DELETE FROM customers\n'
                    f'WHERE customer_id = {l_rs[0]["customer_id"]}\n')
    return make_response(f"{l_rs} successfully deleted", 200)

