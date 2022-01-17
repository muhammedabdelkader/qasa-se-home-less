# qasa-se-home-less

Serverless preactive finding Condo or House based on your pref. 

In order to operate, you need to set email and token in ```./data/tokenz.csv``` ; 

then set Pref using one of the templates for your search critria in ```./data/clientPref.json```;

cron command ```curl http://<IP:port>/sendMeAds/<email>/<Token>```.
