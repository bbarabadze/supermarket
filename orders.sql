# პოსტგრესში შექმენით ბაზა სახელად supermarkets_project და ბაზაში ეს ორი თეიბლი:

CREATE TABLE orders(
    order_id VARCHAR(50),
    store_name VARCHAR(20),
    customer_id INTEGER,
    user_location VARCHAR(20),

    category VARCHAR(20),
    item_id INTEGER,
    name VARCHAR(20),
    price double precision,

    total_price double precision,
    time_stamp TIMESTAMP
)PARTITION BY LIST (user_location);

CREATE TABLE notifications(
       order_id VARCHAR(50),
       sms VARCHAR(50),
       email VARCHAR(50),
       message TEXT

    );

