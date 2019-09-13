# oqyrman-backend
<h2>backend</h2>

**Instructions**

1) Fetch/parse book from kitap.kz and generate epub from the content with the help of **/scripts/finalv2.py**. It should also automatically translate the content into Latin alphabet. 
2) Generate a new json data with django project or there is already **/htdocs** directory exists with generated data, in order to deal with static data further.
3) Run local server with **xampp**, in order to make communication with mobile device, in our situation it is Android OS device.

---

Modules for django:

**-> pip freeze**

certifi==2019.6.16

Django==2.2.5

pytz==2019.2

sqlparse==0.3.0

---

**-> pip install djangorestframework**

**-> pip install djangorestframework-jwt**

---

In order to run local server:

**-> python3 manage.py runserver**
