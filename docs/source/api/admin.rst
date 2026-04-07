Admin API
==============

On server startup an admin account with username ``admin`` and
password ``admin`` is created to be able to manage the server remotely,
set these passwords with the :http:post:`/admin/reset_password` route to guard access to
the server.

All admin routes(except :http:post:`/admin/login`) require an authorization token given by :http:post:`/admin/login` in the :http:header:`Authorization` header as ``Bearer <token>``

.. autoflask:: src.app:app
    :include-empty-docstring:
    :blueprints: admin
    