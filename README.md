Voteflow
==============================

VoteFlow is a website/app built on django to try out a LiquidDemocracy-like system.  
Currently in early stages - expect some uglyness and broken bits.  

Previously known as "MeshDemocracy: Agora"

Live Demo: [Click here - very pre-alpha!](http://voteflow.net/)

###Topic Tree
The topic tree is a central component - anyone can create a topic as a subtopic of any other topic - or top-level

###Posting
Posting lets people place messages directly inside topics, or as a reply to an existing message

###Representation
A user may pick a representitive for a topic - this also applies to sub-topics, and can chain.  
So, Theo is representing 100 people in Science.  
Theo and 9 other people also representing 100 people in science make Albert their representitive for Science->Physics.  
Albert is now representing 1000 people in physics.

###Voting
Any user may vote on any Posting/Message.

##Todo
- ~~Correct Liquid Counting~~
- ~~Use Agora as DevMap/Todo list for its-self~~
- Sorting, by user selectable methods ~~partial~~
- ~~Full Tree View - for topics and posts~~
- images
- user profile page ~~partial~~
- ~~representation graph~~ - show representation for a topic
- ~~vote graph - should representation for a vote~~
- groups/circles
- AJAX/Dynamic Updates ~~partial~~
- Template Styling/CSS ~~partial~~
- search/filter
- ~~notifications~~
- ~~OAUTH FB/Goog/~~ GitHub login
- loads more

----------------------------
##Running MD: Agora
###Linux

dependencies:

    pip install django 
    pip install markdown
    pip install python-social-auth
    pip install oauthlib
    pip install pillow
    pip install html2text

install

    #Install Dependencies then
    git clone https://github.com/chozabu/VoteFlow.git #Clone the project
    cd VoteFlow #enter project
    python manage.py migrate #create DB
    python manage.py runserver #Run Server
    firefox http://127.0.0.1:8000/agora/ #Try it out!
    
or in a virtualenv

    git clone https://github.com/chozabu/VoteFlow
    cd VoteFlow/
    virtualenv env
    source env/bin/activate
    #Install Dependencies HERE
    python manage.py migrate
    python manage.py runserver

###Other OS

add me


##Project Structure
Project setup should be fairly standard for django.
Important files are in agora/:  
- urls.py - based on browser URL, directs you to a view
- views.py - Pulls data from models, returns through a template
- models.py - Database models
- templates/agora/* - HTML templates
- static/agora/* - CSS and other files

##Licence
Agora is published under the GNU AGPL  
https://gnu.org/licenses/agpl.html  
