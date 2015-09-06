MeshDemocracy: Agora
==============================
MeshDemocracy is a decentralised system, to let people discuss, select representitives, and organise on a massive scale through representation chains. Currently on hold while developing Agora.

#Agora
MD: Agora is a website/app built on django to test out the  concepts behind MD.  
Currently in early stages - expect some uglyness and broken bits.

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
- Correct Liquid Counting
- Use Agora as DevMap/Todo list for its-self
- Sorting, by user selectable methods
- Full Tree View - for topics and posts
- images
- user profile page
- representation graph - show representation for a topic
- vote graph - should representation for a vote
- groups/circles
- AJAX/Dynamic Updates
- Template Styling/CSS
- search/filter
- notifications
- OAUTH FB/Goog/GitHub login
- loads more

----------------------------
##Running MD: Agora
###Linux

    pip install django #Install Dependencies
    git clone https://github.com/chozabu/MeshDemocAgora.git #Clone the project
    cd MeshDemocAgora #enter project
    python manage.py migrate #create DB
    python manage.py runserver #Run Server
    firefox http://127.0.0.1:8000/agora/ #Try it out!

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
