Browser → sends HTTP request to → Render (cloud server) → routes to → Gunicorn (web server) → passes to → Flask (your app) → returns response back up the chain → Browser renders the HTML/JS

FE is simple dropdown menu of NBA regions and when you click on a menu item it kicks off a GET request to an NBA API for the teams in that region, returned back to the FE

Wanted to test using Upstash-hosted Redis instance (cache-aside)

Hosting the whole project on Render

Check it out here:
https://redis-n-hosting-test.onrender.com/

(free tier so there's cold starts)
