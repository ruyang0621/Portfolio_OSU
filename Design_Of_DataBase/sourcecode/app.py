from flask import Flask, render_template, json, request
import os
import database.db_connector as db


# Configuration
db_connection = db.connect_to_database()
app = Flask(__name__)


# Routes 
@app.route('/')
def root():
    return render_template("main.j2")


@app.route('/books', methods=['POST', 'GET', 'DELETE'])
def books():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Books ORDER BY bookId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        books = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a book by name.
        if request.form['action'] == "search_book":
            searchBy, searchInput = request.form['search_book_by'], request.form['search_book_input'].capitalize()
            if searchBy == 'isbn':
                query = "SELECT * FROM Books WHERE ISBN = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(searchInput,))
                books = cursor.fetchall()
            if searchBy == 'title':
                query = "SELECT * FROM Books WHERE title = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(searchInput,))
                books = cursor.fetchall()
            if not books:
                books = None
            returnCode = '002'
        # Add an book by name.
        if request.form['action'] == "add_book":
            isbn, title, publisher, publish_year = request.form['isbn'], request.form['title'].capitalize(), request.form['publisher'].capitalize(), request.form['publish_year'].capitalize()
            query = "SELECT * FROM Books WHERE ISBN = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(isbn,))
            books = cursor.fetchall()
            if not books:
                query = "INSERT INTO Books (ISBN, publisher, title, publicationYear) VALUES (%s, %s, %s, %s);"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(isbn, publisher, title, publish_year))
                returnCode = '003'
            else:
                returnCode = '004'
            books = isbn
        if request.form['action'] == "edit_book":
            book_id = request.form['bookId']
            query = "UPDATE Books set ISBN = %s, publisher = %s, title = %s, publicationYear = %s WHERE bookId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(request.form['isbn'], request.form['publisher'], request.form['title'], request.form['publication_year'], request.form['bookId']))
            query = "SELECT * FROM Books WHERE bookId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
            books = cursor.fetchall()
            returnCode = '002'
            
    # Delete a book.
    if request.method =='DELETE':
        id = str(request.json['id'])
        query = "SELECT * FROM BooksAuthors WHERE bookId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        books_1 = cursor.fetchall()
        query = "SELECT * FROM BooksCategories WHERE bookId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        books_2 = cursor.fetchall()
        if books_1 or books_2: 
            return json.dumps({'result':'fail'})
        query = "DELETE FROM Books WHERE bookId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,)) 
        return json.dumps({'result':'success'}) 
    return render_template("books.j2", books=books, returnCode=returnCode)
    

@app.route('/authors', methods=['POST', 'GET', 'DELETE', 'PUT'])
def authors():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Authors ORDER BY authorId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        authors = cursor.fetchall()
        returnCode = '001'
        
    if request.method == 'POST':
        # Search an author by name.
        if request.form['action'] == "search_author":
            fname, lname = request.form['fname'].capitalize(), request.form['lname'].capitalize()
            query = "SELECT * FROM Authors WHERE firstName = %s AND lastName = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname))
            authors = cursor.fetchall()
            returnCode = '002'
            if not authors:
                authors = None
        # Add an author by name.
        if request.form['action'] == "add_author":
            fname, lname = request.form['add_first'].capitalize(), request.form['add_last'].capitalize()
            query = "SELECT * FROM Authors WHERE firstName = %s AND lastName = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname))
            authors = cursor.fetchall()
            if not authors:
                query = "INSERT INTO Authors (firstName, lastName) VALUES (%s, %s);"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname))
                returnCode = '003'
            else:
                returnCode = '004'
            authors = (fname, lname)
        # Update an author
        if request.form['action'] == "edit_author":
            author_id = request.form['authorId']
            query = "UPDATE Authors set firstName = %s, lastName = %s WHERE authorId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (request.form['firstName'],request.form['lastName'],request.form['authorId']))
            query = "SELECT * FROM Authors WHERE authorId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(author_id,))
            authors = cursor.fetchall()
            returnCode = '002'
    # Delete an author.
    if request.method =='DELETE':
        id = str(request.json['id'])
        query = "SELECT * FROM BooksAuthors WHERE authorId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        authors = cursor.fetchall()
        if not authors: 
            query = "DELETE FROM Authors WHERE authorId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,)) 
            return json.dumps({'result':'success'})
        return json.dumps({'result':'fail'})
    return render_template("authors.j2", authors = authors, returnCode = returnCode)
    

@app.route('/categories', methods=['POST', 'GET', 'DELETE'])
def categories():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Categories ORDER BY categoryId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        categories = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a category by name.
        if request.form['action'] == "search_category":
            category_name = request.form['search_category_name'].capitalize()
            query = "SELECT * FROM Categories WHERE categoryName = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_name,))
            categories = cursor.fetchall()
            returnCode = '002'
            if not categories:
                categories = None
        # Add a category by name.
        if request.form['action'] == "add_category":
            category_name = request.form['add_category_name'].capitalize()
            query = "SELECT * FROM Categories WHERE categoryName = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_name,))
            categories = cursor.fetchall()
            if not categories:
                query = "INSERT INTO Categories (categoryName) VALUES (%s);"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_name,))
                returnCode = '003'
            else:
                returnCode = '004'
            categories = (category_name,)
        # Update a category.
        if request.form['action'] == "edit_category":
            category_id = request.form['categoryId']
            query = "UPDATE Categories set categoryName = %s WHERE categoryId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(request.form['category'],request.form['categoryId']))
            query = "SELECT * FROM Categories WHERE categoryId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_id,))
            categories = cursor.fetchall()
            returnCode = '002'
                     
    # Delete a category by name.
    if request.method =='DELETE':
        id = str(request.json['id'])
        query = "SELECT * FROM BooksCategories WHERE categoryId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        categories = cursor.fetchall()
        if not categories: 
            query = "DELETE FROM Categories WHERE categoryId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,)) 
            return json.dumps({'result':'success'})
        return json.dumps({'result':'fail'})
    return render_template("categories.j2", categories=categories, returnCode = returnCode)
    

@app.route('/booksAuthors', methods=['POST', 'GET', 'DELETE'])
def bookAuthors():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Books order by title;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    books = cursor.fetchall()
    query = "SELECT * FROM Authors order by firstName;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    authors = cursor.fetchall()
    if request.method == 'GET':
        query = "SELECT BooksAuthors.bookId, title, authorId FROM BooksAuthors LEFT JOIN Books ON BooksAuthors.bookId = Books.bookId ORDER BY RAND() LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        booksAuthors = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a relationship by id.
        if request.form['action'] == "search_booksAuthors":
            method_ba, search_input = request.form['search_relation_by'], request.form['search_relation_input']
            if method_ba == "relation_book_id":
                query = "SELECT BooksAuthors.bookId, title, authorId FROM BooksAuthors LEFT JOIN Books ON BooksAuthors.bookId = Books.bookId WHERE BooksAuthors.bookId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(search_input,))
                booksAuthors = cursor.fetchall()
            if method_ba == "relation_author_id":
                query = "SELECT BooksAuthors.bookId, title, authorId FROM BooksAuthors LEFT JOIN Books ON BooksAuthors.bookId = Books.bookId WHERE authorId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(search_input,))
                booksAuthors = cursor.fetchall()
            returnCode = '002'
            if not booksAuthors:
                booksAuthors = None
        # Add a relationship by id.
        if request.form['action'] == "add_booksAuthors":
            author_id, book_id = request.form['add_author_id'], request.form['add_book_id']
            query = "SELECT * FROM BooksAuthors WHERE bookId = %s AND authorId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, author_id))
            result_1 = cursor.fetchall()
            if not result_1:
                query = "SELECT * FROM Authors WHERE authorId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(author_id,))
                result_2 = cursor.fetchall()
                query = "SELECT * FROM Books WHERE bookId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
                result_3 = cursor.fetchall()
                if result_2 and result_3:
                    query = "INSERT INTO BooksAuthors (bookId, authorId) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, author_id))
                    returnCode = '003'
                else:
                    returnCode = '005'
            else:
                returnCode = '004'
            booksAuthors = (book_id, author_id)
        # Update a relationship.        
        if request.form['action'] == "edit_book_author":
            book_id = request.form['bookId_ba']
            author_id = request.form['authorId_ba']
            author_id_old = request.form['authorId_old']
            query = "SELECT * FROM BooksAuthors WHERE bookId = %s AND authorId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, author_id))
            result_1 = cursor.fetchall()
            if result_1:
                returnCode = '004'
                booksAuthors = (book_id, author_id)
            else:
                query = "SELECT * FROM Authors WHERE authorId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(author_id,))
                result = cursor.fetchall()
                if not result:
                    returnCode = '005'
                    booksAuthors = (book_id, author_id)
                else:
                    query = "UPDATE BooksAuthors set authorId = %s WHERE bookId = %s AND authorId = %s;"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(author_id, book_id, author_id_old))
                    query = "SELECT BooksAuthors.bookId, title, authorId FROM BooksAuthors LEFT JOIN Books ON BooksAuthors.bookId = Books.bookId WHERE BooksAuthors.bookId = %s AND authorId = %s;"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, author_id))
                    booksAuthors = cursor.fetchall()
                    returnCode = '002'
            
    # Delete a category by name.
    if request.method =='DELETE':
        id_1, id_2 = str(request.json['id_1']), str(request.json['id_2'])
        query = "DELETE FROM BooksAuthors WHERE bookId = %s AND authorId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id_1, id_2)) 
        return json.dumps({'result':'success'})
    # Update an category 
    return render_template("booksAuthors.j2", booksAuthors=booksAuthors, returnCode=returnCode, books=books, authors=authors)
    

@app.route('/booksCategories', methods=['POST', 'GET', 'DELETE'])
def bookCategories():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Categories order by categoryName;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    categories = cursor.fetchall()
    query = "SELECT * FROM Books order by title;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    books = cursor.fetchall()
    if request.method == 'GET':
        query = "SELECT BooksCategories.bookId, title, categoryId FROM BooksCategories LEFT JOIN Books ON BooksCategories.bookId = Books.bookId ORDER BY RAND() LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        booksCategories = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a relationship by id.
        if request.form['action'] == "search_booksCategories":
            method_ba, search_input = request.form['search_relation_by'], request.form['search_relation_input']
            if method_ba == "relation_book_id":
                query = "SELECT BooksCategories.bookId, title, categoryId FROM BooksCategories LEFT JOIN Books ON BooksCategories.bookId = Books.bookId WHERE BooksCategories.bookId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(search_input,))
                booksCategobooksAuthorsries = cursor.fetchall()
            if method_ba == "relation_category_id":
                query = "SELECT BooksCategories.bookId, title, categoryId FROM BooksCategories LEFT JOIN Books ON BooksCategories.bookId = Books.bookId WHERE categoryId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(search_input,))
                booksCategories = cursor.fetchall()
            returnCode = '002'
            if not booksCategories:
                booksCategories = None
        # Add a relationship by id.
        if request.form['action'] == "add_booksCategories":
            category_id, book_id = request.form['add_category_id'], request.form['add_book_id']
            query = "SELECT * FROM BooksCategories WHERE bookId = %s AND categoryId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, category_id))
            result_1 = cursor.fetchall()
            if not result_1:
                query = "SELECT * FROM Categories WHERE categoryId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_id,))
                result_2 = cursor.fetchall()
                query = "SELECT * FROM Books WHERE bookId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
                result_3 = cursor.fetchall()
                if result_2 and result_3:
                    query = "INSERT INTO BooksCategories (bookId, categoryId) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, category_id))
                    returnCode = '003'
                else:
                    returnCode = '005'
            else:
                returnCode = '004'
            booksCategories = (book_id, category_id)
        # Update a relationship.        
        if request.form['action'] == "edit_book_category":
            book_id = request.form['bookId_bc']
            category_id = request.form['categoryId_bc']
            category_id_old = request.form['category_id_old']
            query = "SELECT * FROM BooksCategories WHERE bookId = %s AND categoryId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, category_id))
            result_1 = cursor.fetchall()
            if result_1:
                returnCode = '004'
                booksCategories = (book_id, category_id)
            else:
                query = "SELECT * FROM Categories WHERE categoryId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_id,))
                result = cursor.fetchall()
                if not result:
                    returnCode = '005'
                    booksCategories = (book_id, category_id)
                else:
                    query = "UPDATE BooksCategories set categoryId = %s WHERE bookId = %s and categoryId = %s;"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(category_id, book_id, category_id_old))
                    query = "SELECT BooksCategories.bookId, title, categoryId FROM BooksCategories LEFT JOIN Books ON BooksCategories.bookId = Books.bookId WHERE BooksCategories.bookId = %s AND BooksCategories.categoryId = %s;"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, category_id))
                    booksCategories = cursor.fetchall()
                    returnCode = '002'
            
    # Delete a category by name.
    if request.method =='DELETE':
        id_1, id_2 = str(request.json['id_1']), str(request.json['id_2'])
        query = "DELETE FROM BooksCategories WHERE bookId = %s AND categoryId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id_1, id_2)) 
        return json.dumps({'result':'success'})
    # Update an category    
    return render_template("booksCategories.j2", booksCategories=booksCategories, returnCode=returnCode, categories=categories,books=books)


@app.route('/copies', methods=['POST', 'GET', 'DELETE'])
def copies():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Copies ORDER BY copyId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        copies = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a copy by ID.
        if request.form['action'] == "search_copy":
            book_id = request.form['book_id']
            query = "SELECT * FROM Copies WHERE bookId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
            copies = cursor.fetchall()
            returnCode = '002'
            if not copies:
                copies = None
        # Add a copy by name.
        if request.form['action'] == "add_copy":
            book_id, condition = request.form['book_id_add'], request.form['condition']
            query = "SELECT * FROM Books WHERE bookId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
            books = cursor.fetchall()
            if not books:
                returnCode = '004'
            else:
                query = "SELECT count(copyId) AS count FROM Copies WHERE bookId = %s;" 
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id,))
                copy_count = cursor.fetchall()
                copy_count = copy_count[0]['count']
                if copy_count == 3:
                    returnCode ='005'
                else:
                    copy_num = copy_count + 1
                    query = "INSERT INTO Copies (bookId, copyNum, bookCondition) VALUES (%s, %s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(book_id, copy_num, condition))
                    returnCode = '003'
            copies = (book_id, condition)
        # Update a copy.
        if request.form['action'] == "edit_copy":
            copy_id = request.form['copyId']
            book_status = request.form['bookStatus']
            book_condition = request.form['bookCondition']
            query = "UPDATE Copies set bookCondition = %s, status = %s WHERE copyId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (book_condition, book_status, copy_id))
            query = "SELECT * FROM Copies WHERE copyId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(copy_id,))
            copies = cursor.fetchall()
            returnCode = '002'
            
    # Delete a copy.
    if request.method == 'DELETE':
        id = str(request.json['id'])
        query = "SELECT * FROM BorrowRecords WHERE copyId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        copies = cursor.fetchall()
        if not copies:
            query = "DELETE FROM Copies WHERE copyId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
            return json.dumps({'result':'success'})
        return json.dumps({'result':'fail'})
    return render_template("copies.j2", copies=copies, returnCode=returnCode)


@app.route('/members', methods=['POST', 'GET', 'DELETE'])
def members():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Members ORDER BY memId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        members = cursor.fetchall()
        returnCode = '001'

    if request.method == 'POST':
        # Search a member by name.
        if request.form['action'] == "search_member":
            fname, lname = request.form['fname'].capitalize(), request.form['lname'].capitalize()
            query = "SELECT * FROM Members WHERE firstName = %s AND lastName = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname))
            members = cursor.fetchall()
            returnCode = '002'
            if not members:
                members = None
        # Add a member by name.
        if request.form['action'] == "add_member":
            fname, lname, address, email, phone = request.form['add_first'].capitalize(), request.form['add_last'].capitalize(), request.form['add_address'].capitalize(), request.form['add_email'], request.form['add_phone']
            query = "SELECT * FROM Members WHERE firstName = %s AND lastName = %s AND memCell = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname, phone))
            members = cursor.fetchall()
            if not members:
                query = "INSERT INTO Members (firstName, lastName, memAddress, memEmail, memCell) VALUES (%s, %s, %s, %s, %s);"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname,address,email,phone))
                returnCode = '003'
            else:
                returnCode = '004'
            members = (fname, lname)
        # Update a member.
        if request.form['action'] == "edit_member":
            member_id = request.form['memId']
            first_name = request.form['firstName']
            last_name =request.form['lastName']
            address = request.form['homeAddress']
            email = request.form['email']
            cell = request.form['phone']
            query = "UPDATE Members set firstName = %s, lastName = %s, memAddress = %s, memEmail = %s, memCell = %s WHERE memId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (first_name, last_name, address, email, cell, member_id))
            query = "SELECT * FROM Members WHERE memId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(member_id,))
            members = cursor.fetchall()
            returnCode = '002'
        
    # Delete a member.
    if request.method == 'DELETE':
        id = str(request.json['id'])
        query = "SELECT * FROM BorrowRecords WHERE memId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        members = cursor.fetchall()
        if not members:
            query = "DELETE FROM Members WHERE memId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
            return json.dumps({'result':'success'})
        return json.dumps({'result':'fail'})
    return render_template("members.j2", members=members, returnCode=returnCode)


@app.route('/borrowRecords', methods=['GET', 'POST','DELETE'])
def borrowRecords():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Members order by memId;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    members = cursor.fetchall()
    query = "SELECT * FROM Copies where status != 'On Loan' order by copyId;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    copies = cursor.fetchall()
    if request.method == 'GET':
        query = "SELECT * FROM BorrowRecords ORDER BY borrowId DESC LIMIT 10;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        borrowRecords = cursor.fetchall()
        returnCode = '001'
    
    if request.method == 'POST':
        # Search a borrow record by member id.
        if request.form['action'] == "search_borrowRecords": # input type hidden action and value
            memId_bc = request.form['memId']
            query = "SELECT * FROM BorrowRecords WHERE memId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(memId_bc,))
            borrowRecords = cursor.fetchall()
            print(borrowRecords)
            returnCode = '002'
            if not borrowRecords:
                borrowRecords = None
        # Add a borrow record 
        if request.form['action'] == "add_borrow_record":
            member_id = request.form['member_id']
            copy_id = request.form['copy_id']
            borrow_date = request.form['borrow_date']
            due_date = request.form['due_date']
            
            query = "SELECT * FROM BorrowRecords WHERE memId = %s AND copyId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(member_id, copy_id))
            borrowed = cursor.fetchall()
            if not borrowed:
                query = "SELECT * FROM Members WHERE memId = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(member_id,))
                result_2 = cursor.fetchall()
                query = "SELECT * FROM Copies WHERE copyId = %s and status != 'On Loan';"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(copy_id,))
                result_3 = cursor.fetchall()
                if result_2 and result_3:
                    query = "INSERT INTO BorrowRecords (memId, copyId, borrowDate, dueDate) VALUES (%s, %s, %s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(member_id, copy_id,borrow_date,due_date))
                    returnCode = '003'
                else:
                    returnCode = '005'
            else:
                returnCode = '004'
            borrowRecords = (member_id, copy_id,borrow_date,due_date)
        
        # Update a borrow Record.
        if request.form['action'] == "edit_borrow_record":
            borrowId = request.form['borrowId']
            memId = request.form['memId']
            copyId =request.form['copyId']
            borrowDate = request.form['borrowDate']
            dueDate = request.form['dueDate']
            passDue = request.form['passDue']
            query = "UPDATE BorrowRecords set memId = %s, copyId = %s, borrowDate = %s, dueDate = %s, passDue = %s WHERE borrowId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (memId, copyId, borrowDate, dueDate, passDue,borrowId))
            query = "SELECT * FROM BorrowRecords WHERE borrowId = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(borrowId,))
            borrowRecords = cursor.fetchall()
            returnCode = '002'
        
    # Delete a member.
    if request.method == 'DELETE':
        id = str(request.json['id'])
        query = "DELETE FROM BorrowRecords WHERE borrowId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (id,))
        members = cursor.fetchall()
        return json.dumps({'result':'success'})
            
    return render_template("borrowRecords.j2", borrowRecords=borrowRecords, returnCode=returnCode, members=members, copies=copies)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)