from flask import Flask, render_template, flash, json, url_for, flash, redirect, request 
import database.db_connector as db #database/db_connector
import os


app = Flask(__name__)

def query_db(query, data=None):
    """
    Queries the connected database and returns the results, to be passed into a .j2 template.
    Optionally takes in a tuple called data, which is used to reference query parameters (%s).

    Upon function call, anew connection pool is created and the query is executed.
    The results are sent to the cursor and encoded as JSON. Finally, the cursor
    and connection pool are closed, and the JSON results are returned.
    """
    # open a new connection for this query
    db_connection = db.connect_to_database()

    print(query)
    print(data)

    if data is None:
        cursor = db.execute_query(db_connection=db_connection, query=query)
    else:
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)

    # query_results contains a list of dictionaries, where each dictionary is a result row
    query_results = cursor.fetchall()

    cursor.close()
    db_connection.close()

    print(query)
    print(query_results)

    return query_results


def all_customers_query():
    query = "SELECT * FROM customers;" #query that we'll pass to database 
    query_results = query_db(query=query) #pass connected database and query to databse_connector's execute_query function, db will return a cursor - an object that is able to interact with queries and getting results that flask can use 
    print(query_results)
    return query_results

def all_distributors_query():
    query = "SELECT * FROM distributors;" #query that we'll pass to database 
    query_results = query_db(query=query) #pass connected database and query to databse_connector's execute_query function, db will return a cursor - an object that is able to interact with queries and getting results that flask can use 
    print(query_results)
    return query_results

def all_orders_query():
    query = "SELECT * FROM orders;" #query that we'll pass to database 
    query_results = query_db(query=query) #pass connected database and query to databse_connector's execute_query function, db will return a cursor - an object that is able to interact with queries and getting results that flask can use 
    print(query_results)
    return query_results

def all_ordered_rooms_query():
    query = "SELECT * FROM ordered_rooms;" #query that we'll pass to database 
    query_results = query_db(query=query) #pass connected database and query to databse_connector's execute_query function, db will return a cursor - an object that is able to interact with queries and getting results that flask can use 
    print(query_results)
    return query_results

def all_rooms_query():
    query = "SELECT * FROM rooms;" #query that we'll pass to database 
    query_results = query_db(query=query) #pass connected database and query to databse_connector's execute_query function, db will return a cursor - an object that is able to interact with queries and getting results that flask can use 
    print(query_results)
    return query_results
    
# Routes 

@app.route('/')
@app.route('/home')
def root():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/customers')
def customers():
    query_results = all_customers_query()
    if query_results == (): #if there is no row fetched 
        return render_template('customers.html', results='No Customers in Database', title='Customers')
    #print(results) #({'customer_id': 1, 'first_name': 'William', 'last_name': 'Adama', 'email': 3, 'age': 61}, {'id': 2, 'first_name': 'Lee', 'last_name': 'Adama', 'email': 3, 'age': 30})
    return render_template('customers.html', title='Customers', customers=query_results) #rending the url and whenever customers is mentioned use the result we passed

@app.route('/filter_customer', methods = ['POST', 'GET'])
def filter_customers():
    if request.method == 'POST': 
        print("filtering results:")
        user_filter_input = request.form['user_filter_input']
        print(user_filter_input)
        query = 'SELECT * FROM customers WHERE customer_id = "'+user_filter_input+'" OR first_name = "'+user_filter_input+'" OR last_name ="'+user_filter_input+'" OR email = "'+user_filter_input+'"'
        print (query)
        query_results = query_db(query=query)
        print (query_results)
        query_results_len = len(query_results)
        print("results here!"+str(query_results)) 
        if query_results == (): #if there is no row fetched 
            return render_template('customers.html', results='No Results', title='Customers')
        #print("results here!"+results) #({'customer_id': 1, 'first_name': 'William', 'last_name': 'Adama', 'email': 3, 'age': 61}, {'id': 2, 'first_name': 'Lee', 'last_name': 'Adama', 'email': 3, 'age': 30})
        return render_template('customers.html', title='Customers', results='Displaying Filtered Result: '+str(query_results_len)+' Found' , customers=query_results) #rending the url and whenever customers is mentioned use the result we passed

@app.route('/add_new_customer', methods = ['POST', 'GET'])
def add_new_customer():
    print("adding new people")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    #print("First name is", first_name)
    query = 'INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s);'#query that we'll pass to database 
    #db.execute_query(db_connection=db_connection, query=query)
    query_params = (first_name, last_name, email)
    #db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
    query_db(query=query, data=query_params)
    return render_template('customers.html', results=''+first_name+' '+last_name+' Added', title='Customers', customers = all_customers_query())

@app.route('/update_customer/<int:customer_id>', methods=['POST','GET']) #expect an int after "/update_customer/" and put that into a variable called id which we can use in the function
def update_customer(customer_id):
    if request.method == 'GET':

        customer_query = 'SELECT customer_id, first_name, last_name, email FROM customers WHERE customer_id = %s' %(customer_id)

        query_customer_result = query_db(query=customer_query)

        if query_customer_result == None: #if there is no row fetched 
            return "No such customer found!"

        return render_template('customer_update.html', title='Update Customers', customer=query_customer_result[0]) #using [0] since this returns a tuple due to fetchall()
 
    elif request.method == 'POST':
        print("Update Customers!")
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        #age = request.form['age']
        email = request.form['email']

        print(request.form)

        customer_update_query = "UPDATE customers SET first_name = %s, last_name =%s, email = %s WHERE customer_id = %s"
        query_params = (first_name, last_name, email, customer_id)
        query_customer_result = query_db (query=customer_update_query, data=query_params)
        print(query_customer_result) #returns a blank tuple () 
        return render_template('customers.html', results=''+first_name+' '+last_name+' Updated', title='Customers', customers = all_customers_query())

@app.route('/delete_customer/<int:customer_id>') #expect an int after "/update_customer/" and put that into a variable called id which we can use in the function
def delete_customer(customer_id):
    '''deletes a customer with given id'''
    query = 'Delete FROM customers WHERE customer_id = %s'
    query_param = (customer_id,) #won't turn into a tuple without comma next to id, will just be an int
    result = query_db(query=query, data=query_param)
    #result = len(result)
    return render_template('customers.html', results='Customer Deleted', title='Customers', customers = all_customers_query())

@app.route('/distributors')
def distributors():
    query_results = all_distributors_query()
    if query_results == (): #if there is no row fetched 
        return render_template('distributors.html', results='No Distributors in Database', title='Distributors')
    #print(query_results) #for testing returned result
    return render_template('distributors.html', title='Distributors', distributors=query_results) #rending the url with returned query

@app.route('/add_new_distributor', methods = ['POST', 'GET'])
def add_new_distributor():
    print("adding new distributor")
    distributor_name = request.form['distributor_name']
    distributor_phone = request.form['distributor_phone']
    
    query = 'INSERT INTO distributors (distributor_name, distributor_phone) VALUES (%s, %s);'#query that we'll pass to database 
    #db.execute_query(db_connection=db_connection, query=query)
    query_params = (distributor_name, distributor_phone)
    #db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
    query_db(query=query, data=query_params)
    return render_template('distributors.html', results=''+distributor_name+' Added', title='Distributors', distributors = all_distributors_query())

@app.route('/filter_distributor', methods = ['POST', 'GET'])
def filter_distributor():
    if request.method == 'POST': 
        print("filtering results:")
        user_filter_input = request.form['user_filter_input']
        print(user_filter_input)
        query = 'SELECT * FROM distributors WHERE distributor_id = "'+user_filter_input+'" OR distributor_name = "'+user_filter_input+'" OR  distributor_phone ="'+user_filter_input+'"'
        print (query)
        query_results = query_db(query=query)
        print (query_results)
        query_results_len = len(query_results)
        print("results here!"+str(query_results)) 
        if query_results == (): #if there is no row fetched 
            return render_template('distributors.html', results='No Results', title='Distributors')
        #print("results here!"+results) #({'customer_id': 1, 'first_name': 'William', 'last_name': 'Adama', 'email': 3, 'age': 61}, {'id': 2, 'first_name': 'Lee', 'last_name': 'Adama', 'email': 3, 'age': 30})
        return render_template('distributors.html', title='Distributors', results='Displaying Filtered Result: '+str(query_results_len)+' Found' , distributors=query_results) #rending the url and whenever customers is mentioned use the result we passed

@app.route('/delete_distributor/<int:distributor_id>') #expect an int after "/update_distributor/" and put that into a variable called id which we can use in the function
def delete_distributor(distributor_id):
    '''deletes a distributor with given id'''
    query = 'Delete FROM distributors WHERE distributor_id = %s'
    query_param = (distributor_id,) #won't turn into a tuple without comma next to id, will just be an int
    result = query_db(query=query, data=query_param)
    #result = len(result)
    return render_template('distributors.html', results='Distributor Deleted', title='Distributors', distributors = all_distributors_query())

@app.route('/update_distributor/<int:distributor_id>', methods=['POST','GET']) #expect an int after "/update_distributor/" and put that into a variable called id which we can use in the function
def update_distributor(distributor_id):
    if request.method == 'GET':

        distributor_query = 'SELECT distributor_id, distributor_name, distributor_phone FROM distributors WHERE distributor_id = %s' %(distributor_id)

        query_distributor_result = query_db(query=distributor_query)

        if query_distributor_result == None: #if there is no row fetched 
            return "No such distributor found!"

        return render_template('update_distributor.html', title='Update Distributor', distributor=query_distributor_result[0]) #using [0] since this returns a tuple due to fetchall()
 
    elif request.method == 'POST':
        print("Update Distributors!")
        distributor_id = request.form['distributor_id']
        distributor_name = request.form['distributor_name']
        distributor_phone = request.form['distributor_phone']

        print(request.form)

        distributor_update_query = "UPDATE distributors SET distributor_name = %s, distributor_phone =%s WHERE distributor_id = %s"
        query_params = (distributor_name, distributor_phone, distributor_id)
        query_distributor_result = query_db (query=distributor_update_query, data=query_params)
        print(query_distributor_result) #returns a blank tuple () 
        return render_template('distributors.html', results=''+distributor_name+' Updated', title='Distributors', distributors = all_distributors_query())


@app.route('/rooms')
def rooms():
    query_results = all_rooms_query()

    if query_results == (): #if there is no row fetched 
        return render_template('rooms.html', results='No Rooms in Database', title='Rooms', distributors=all_distributors_query())

    return render_template('rooms.html', title='Rooms', rooms=query_results, distributors=all_distributors_query()) #rending the url with returned query

@app.route('/add_new_room', methods = ['POST', 'GET'])
def add_new_room():
    print("adding new room")
    #distributor_id = request.form['distributor_id']
    distributor_id = request.form['distributor_id']
    beds = request.form['beds']
    city = request.form['city']
    state = request.form['state']
    price = request.form['price']

    query = 'SELECT distributor_name FROM distributors WHERE distributor_id = "'+distributor_id+'"'
    print (query)
    distributor_name = query_db(query=query)[0]['distributor_name']
    print (distributor_id)

    #print("First name is", first_name)
    query = 'INSERT INTO rooms (distributor_id, distributor_name, beds, city, state, price) VALUES (%s, %s, %s, %s, %s, %s);'#query that we'll pass to database 
    #db.execute_query(db_connection=db_connection, query=query)
    query_params = (distributor_id, distributor_name, beds, city, state, price)
    #db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
    query_db(query=query, data=query_params)
    return redirect(url_for('rooms'))

@app.route('/update_room/<int:room_id>', methods=['POST','GET']) #expect an int after "/update_room/" and put that into a variable called id which we can use in the function
def update_room(room_id):
    if request.method == 'GET':

        room_query = 'SELECT room_id, distributor_id, distributor_name, beds, city, state, price from rooms WHERE room_id = %s' %(room_id)

        query_room_result = query_db(query=room_query)

        if query_room_result == None: #if there is no row fetched 
            return "No such room found!"
            
        return render_template('update_room.html', title='Update Rooms', room=query_room_result[0],) #using [0] since this returns a tuple due to fetchall()
 
    elif request.method == 'POST':
        print("Update Rooms!")
        beds = request.form['beds']
        city = request.form['city']
        state = request.form['state']
        price = request.form['price']

        print(request.form)

        room_update_query = "UPDATE rooms SET beds = %s, city =%s, state = %s, price = %s WHERE room_id = %s"
        query_params = (beds, city, state, price, room_id)
        query_room_result = query_db (query=room_update_query, data=query_params)
        print(query_room_result) #returns a blank tuple () 
        return render_template('rooms.html', results='Room '+str(room_id)+' Updated', title='Rooms', rooms = all_rooms_query(), distributors = all_distributors_query())

@app.route('/filter_room', methods = ['POST', 'GET'])
def filter_room():
    if request.method == 'POST': 
        print("filtering results:")
        user_filter_input = request.form['user_filter_input']
        print(user_filter_input)
        query = 'SELECT * FROM rooms WHERE room_id = "'+user_filter_input+'" OR distributor_name = "'+user_filter_input+'" OR  beds ="'+user_filter_input+'" OR city ="'+user_filter_input+'" OR state ="'+user_filter_input+'" OR price ="'+user_filter_input+'"'
        print (query)
        query_results = query_db(query=query)
        print (query_results)
        query_results_len = len(query_results)
        print("results here!"+str(query_results)) 
        if query_results == (): #if there is no row fetched 
            return render_template('rooms.html', results='No Results', title='Rooms')
        return render_template('rooms.html', title='Rooms', results='Displaying Filtered Result: '+str(query_results_len)+' Found' , rooms=query_results) #rending the url and whenever customers is mentioned use the result we passed

@app.route('/delete_room/<int:room_id>') #expect an int after "/delete_room/" and put that into a variable called id which we can use in the function
def delete_room(room_id):
    '''deletes a room with given id'''
    query = 'Delete FROM rooms WHERE room_id = %s'
    query_param = (room_id,) #won't turn into a tuple without comma next to id, will just be an int
    result = query_db(query=query, data=query_param)
    #result = len(result)
    return render_template('rooms.html', results='Room Deleted', title='Rooms', rooms = all_rooms_query(), distributors = all_distributors_query())



@app.route('/orders')
def orders():
    query_results = all_orders_query()
    if query_results == (): #if there is no row fetched 
        return render_template('orders.html', results='No Orders in Database', title='Orders', customers=all_customers_query())

    return render_template('orders.html', title='Orders', orders=query_results, customers=all_customers_query()) #rending the url with returned query


@app.route('/add_new_order', methods = ['POST', 'GET'])
def add_new_order():
    print("adding new order")
    customer_id = request.form['customer_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    #query = 'SELECT customer_name FROM customers WHERE customer_id = "'+customer_id+'"'
    #print (query)
    #customer_name = query_db(query=query)[0]['distributor_name']
    #print (customer_name)

    #print("First name is", first_name)
    query = 'INSERT INTO orders (customer_id, start_date, end_date) VALUES (%s, %s, %s);'#query that we'll pass to database 
    #db.execute_query(db_connection=db_connection, query=query)
    query_params = (customer_id, start_date, end_date)
    #db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
    query_db(query=query, data=query_params)
    return redirect(url_for('orders'))

@app.route('/update_order/<int:order_id>', methods=['POST','GET']) #expect an int after "/update_room/" and put that into a variable called id which we can use in the function
def update_order(order_id):
    if request.method == 'GET':

        order_query = 'SELECT order_id, customer_id, start_date, end_date from orders WHERE order_id = %s' %(order_id)

        query_order_result = query_db(query=order_query)

        if query_order_result == None: #if there is no row fetched 
            return "No such room found!"

        print(query_order_result)
        print(query_order_result)
        print(query_order_result)
        return render_template('update_order.html', title='Update Orders', order=query_order_result[0]) #using [0] since this returns a tuple due to fetchall()
 
    elif request.method == 'POST':
        print("Update Orders!")
        order_id = request.form['order_id']
        #customer_id = request.form['start_date']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        print(request.form)

        order_update_query = "UPDATE orders SET start_date = %s, end_date = %s WHERE order_id = %s"
        query_params = (start_date, end_date, order_id)
        query_order_result = query_db (query=order_update_query, data=query_params)
        print(query_order_result) #returns a blank tuple () 
        return render_template('orders.html', results='Order '+order_id+' Updated', title='Orders', orders = all_orders_query(), customers = all_customers_query())

@app.route('/filter_order', methods = ['POST', 'GET'])
def filter_order():
    if request.method == 'POST': 
        print("filtering results:")
        user_filter_input = request.form['user_filter_input']
        print(user_filter_input)
        query = 'SELECT * FROM orders WHERE order_id = "'+user_filter_input+'" OR start_date = "'+user_filter_input+'" OR  end_date ="'+user_filter_input+'"'
        print (query)
        query_results = query_db(query=query)
        print (query_results)
        query_results_len = len(query_results)
        print("results here!"+str(query_results)) 
        if query_results == (): #if there is no row fetched 
            return render_template('orders.html', results='No Results', title='Orders')
        #print("results here!"+results) #({'customer_id': 1, 'first_name': 'William', 'last_name': 'Adama', 'email': 3, 'age': 61}, {'id': 2, 'first_name': 'Lee', 'last_name': 'Adama', 'email': 3, 'age': 30})
        return render_template('orders.html', title='Orders', results='Displaying Filtered Result: '+str(query_results_len)+' Found' , orders=query_results, customers = all_customers_query()) #rending the url and whenever customers is mentioned use the result we passed

@app.route('/delete_order/<int:order_id>') #expect an int after "/delete_order/" and put that into a variable called id which we can use in the function
def delete_order(order_id):
    '''deletes a order with given id'''
    query = 'Delete FROM orders WHERE order_id = %s'
    query_param = (order_id,) #won't turn into a tuple without comma next to id, will just be an int
    result = query_db(query=query, data=query_param)
    #result = len(result)
    return render_template('orders.html', results='Order Deleted', title='Orders', orders = all_orders_query(), customers = all_customers_query())


@app.route('/ordered_rooms')
def ordered_rooms():
    query_results = all_ordered_rooms_query()
    if query_results == (): #if there is no row fetched 
        return render_template('ordered_rooms.html', results='No Ordered Rooms in Database', title='Ordered Rooms')
    #print(query_results) #for testing returned result
    return render_template('ordered_rooms.html', title='Ordered Rooms', ordered_rooms = all_ordered_rooms_query(), orders=all_orders_query(), rooms=all_rooms_query()) #rending the url with returned query

@app.route('/add_new_ordered_room', methods = ['POST', 'GET']) #add relationship between room and order entities
def add_new_ordered_room():
    print("adding new ordered room")
    room_id = request.form['room_id']
    order_id = request.form['order_id']
    query = 'INSERT INTO ordered_rooms (room_id, order_id) VALUES (%s, %s);'#query that we'll pass to database 
    #db.execute_query(db_connection=db_connection, query=query)
    query_params = (room_id, order_id)
    #db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
    query_db(query=query, data=query_params)
    first_update_query = 'UPDATE ordered_rooms SET total_price = (SELECT rooms.price FROM rooms WHERE rooms.room_id = ordered_rooms.room_id);'
    query_db(query=first_update_query)
    second_update_query = 'UPDATE ordered_rooms SET total_price = ordered_rooms.total_price * (SELECT DATEDIFF(orders.end_date, orders.start_date) FROM orders WHERE orders.order_id = ordered_rooms.order_id);'
    query_db(query=second_update_query)
    return redirect(url_for('ordered_rooms'))


@app.route('/update_ordered_room/<int:order_id>,<int:room_id>', methods=['POST','GET']) #expect 2 ints after "/update_ordered_room/" and put that into a variable called id which we can use in the function
def update_ordered_room(order_id, room_id):
    if request.method == 'GET':

        ordered_room_query = 'SELECT order_id, room_id, total_price FROM ordered_rooms WHERE order_id = %s AND room_id = %s'
        query_params = (order_id, room_id)

        query_order_result = query_db(query=ordered_room_query)

        if query_order_result == None: #if there is no row fetched 
            return "No such ordered room/relationship found!"

        return render_template('update_ordered_rooms.html', title='Update Ordered Rooms', ordered_room=query_order_result[0]) #using [0] since this returns a tuple due to fetchall()
 
    elif request.method == 'POST':
        print("Update Ordered Room!")
        room_id = request.form['room_id']
        order_id = request.form['order_id']
        print(request.form)

        order_update_query = "UPDATE ordered_rooms SET order_id = %s, room_id = %s WHERE order_id = %s AND room_id = %s"
        query_params = (order_id, room_id)
        query_order_result = query_db (query=order_update_query, data=query_params)
        print(query_order_result) #returns a blank tuple () 
        return render_template('ordered_rooms.html', results='Ordered Rooms Updated', title='Ordered Rooms', ordered_rooms = all_ordered_rooms_query())

@app.route('/delete_ordered_room/<int:order_id>,<int:room_id>') #expect 2 ints after "/update_ordered_room/" and put that into a variable called id which we can use in the function
def delete_ordered_room(order_id, room_id):
    '''deletes a order with given id'''
    query = 'Delete FROM ordered_rooms WHERE order_id = %s AND room_id = %s'
    query_param = (order_id, room_id,) #won't turn into a tuple without comma next to id, will just be an int
    result = query_db(query=query, data=query_param)
    #result = len(result)
    return render_template('ordered_rooms.html', results='Ordered Room Deleted', title='Ordered Rooms', ordered_rooms = all_ordered_rooms_query())

@app.route('/filter_ordered_rooms', methods = ['POST', 'GET'])
def filter_ordered_rooms():
    if request.method == 'POST': 
        print("filtering results:")
        user_filter_input = request.form['user_filter_input']
        print(user_filter_input)
        query = 'SELECT * FROM ordered_rooms WHERE order_id = "'+user_filter_input+'" OR room_id = "'+user_filter_input+'" OR  total_price ="'+user_filter_input+'"'
        print (query)
        query_results = query_db(query=query)
        print (query_results)
        query_results_len = len(query_results)
        print("results here!"+str(query_results)) 
        if query_results == (): #if there is no row fetched 
            return render_template('ordered_rooms.html', results='No Results', title='Ordered Rooms')
        return render_template('ordered_rooms.html', title='Ordered Rooms', results='Displaying Filtered Result: '+str(query_results_len)+' Found' , ordered_rooms=query_results) #rending the url and whenever customers is mentioned use the result we passed


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4867))  #change here, 
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True) # This will force the server to reload whenever changes are made to your project, so that way
                                   # you don't have to manually kill the process and restart it every time.

'''
Would love to have editable information in table instead of secondary page for each
Make it so that adding a room is impossible if dates are in ordered....add to next time sheet..aint nobdy got time
Edward was suppsoed to calculate prices based on length of stay 
Incorporate some of these elements: https://www.tutorialrepublic.com/codelab.php?topic=bootstrap&file=crud-data-table-for-database-with-modal-form
'''