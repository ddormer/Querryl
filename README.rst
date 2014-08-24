=======
Querryl
=======
A web application for searching your Quassel database.



Postgresql
----------
It's recommended to setup a Postgresql user with read-only access to the Quassel database.

1. Run ``psql`` as the admin user and open the ``quassel`` database: ``sudo -u postgres psql quassel``
2. Run the following SQL query: ```CREATE USER querryl WITH PASSWORD 'secure-password';``
3. Give the new user read-only access to the tables: ``GRANT SELECT ON ALL TABLES IN SCHEMA public TO querryl;``


Installation
------------
1. ``pip install git+git://github.com/ddormer/Querryl``
2. ``cd Querryl``
3. ``cp config.py.sample config.py``
4. Edit ``config.py`` to fit your needs.
5. ``trial querryl``


Run
---
``twistd -n quassel``
