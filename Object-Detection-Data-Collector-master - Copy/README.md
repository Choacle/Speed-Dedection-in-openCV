# Object-Detection-Data-Collector
This tool lets you track an object using HSV values and creates a bounding box around it. You can resize the bounding box and move the object around and save the frames by the press of a button.

---

# Installation

    git clone https://github.com/janmejai2002/Object-Detection-Data-Collector.git

    cd Object-Detection-Data-Collector

    pip install -r requirements.txt

# Run

    python main.py

After that change the HSV slider values to find the appropriate values based on the object you want to use.

Press `t` to confirm.

Now you will see a green box around the object you want to track. Feel free to move it around.

In case you see multiple boxes, press `t` again to finetune the HSV values or get rid of other items in the frame which have nearly the same color.

You can resize the height and width of the box according to your need.  

Press for resizing:

    1 for increasing width
    2 for decreasing width
    3 for increasing height
    4 for decreasing height

Press 's' to save the frame as a `png` and coordinates inside a csv.  
The image is saved inside a folder called `Random` if you did not pass a class variable. To save it according to classes you have to pass a commanline argument as shown in the next section.

The code is easy to run and understand and uses only OpenCV, Numpy and imutils.

---

# Arguments

    python main.py --help

Output:  
    
    usage: main.py [-h] [-c CLASS]

    optional arguments:
    -h, --help                 show this help message and exit
    -c CLASS, --class CLASS    Object Class

So if I am taking pictures of an apple then I can pass

    python main.py --class "Apple"

Now the frame you save will be inside a directory titled apple and the fieldname `Class` for csv will also change.

---

Do star if you like it and have fun :D