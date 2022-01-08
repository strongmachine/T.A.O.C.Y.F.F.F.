# T.A.O.C.Y.F.F.F.

The Application Of Changing Your Face For Fun



Background
* Face detection, and its counterpart, facial recognition is at the forefront of machine learning.  We want to explore these two facets through the lens of a SnapChat filter, which uses facial detection to augment a user’s facial features.

Motivation 
* Our motivation is to show the fun side of machine learning, that can translate to a professional or recreational environment, e.g., biometrics.

Questions to answer
* Which facial features are easiest for a computer to recognize; which are hardest?
* How do the filters handle scaling on multiple devices, e.g., eyes that are 1000 times larger than normal?
* How many facial landmarks are necessary to implement a snapchat-like filter?  There are a number of them to choose from 68, 5 but what is optimal? 

Tools/Modules to use
* OpenCV, a machine learning library that we haven’t used before, but is foundational for facial recognition machine learning modules. 
* Dlib, is a secondary component to understanding and mapping faces once they are recognized, it recognizes facial landmarks. Landmarks are important to implementing the output features onto the rendered face. 
* HTML, Javascript for app hosting
* Heroku for deployment
* Mediapipe, is a tool created by Google, if we wind up not being able to use the Dlip C++ based library, this is functionally the same. 

