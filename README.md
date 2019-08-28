# Twitter Media Downloader with Gephi Support
[![DOI](https://zenodo.org/badge/175605845.svg)](https://zenodo.org/badge/latestdoi/175605845)

This small Python script can take a .csv of Twitter id numbers and download the embedded media.
The script also supports exports generated by the fantastic [TwitterStreamingImporter](https://github.com/seinecle/gephi-tutorials/blob/master/src/main/asciidoc/en/plugins/twitter-streaming-importer-en.adoc)
plugin for Gephi.

Given either a .csv list or a Gephi export, the script will download all associated...

* Photos
* Videos
* Animated Gifs

The script will also generate a report, allowing quick matching back to
your original CSV.

This script was created at the request of the AOIR Digital Methods Workgroup.

##### Citation
if you use this project in your research please cite. 

`James Allen-Robertson. (2019, April 23). Minyall/gephi_twitter_media_downloader:
 Media Downloader with Type Filter (Version v0.1.3.0). Zenodo. http://doi.org/10.5281/zenodo.2649073`


# Instructions
## I use Python / I know what I'm doing...
Great! This script requires [Tweepy](http://www.tweepy.org) and was
written in Python 3.6.
1. Download the script
2. Ensure your gephi export .csv is in the same folder as the script
3. Edit the `credentials.py` file so that...

        CONSUMER_KEY = 'YOUR_KEY'
        CONSUMER_SECRET = 'YOUR_SECRET'
4. Run `pip install -r requirements.txt`
5. Run `python download_twitter_media.py`
6. If using a Gephi export use the argument `-G` to activate Gephi compatibility.
7. If using a list of twitter ids, ensure the .csv has a header name which should be passed to the script using `-c`

        python download_twitter_media.py -c my_id_column
8. Follow the on-screen instructions
9. For a full list of options...

        python download_twitter_media.py --help
## I don't use Python / I don't know what I'm doing...
Not a problem, this script is for people like you!

### 1. Install your Python Environment
**NOTE: If you already have Miniconda / Anaconda installed on your
machine, skip this step**.

Install either [Anaconda](https://www.anaconda.com/distribution/#download-section)
 or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to give yourself an up to date Python environment
that is seperate from any native environments on your machine.


If installing Anaconda you want...
* Python 3
* 64bit Graphical Installer

If installing Miniconda you want...
* Python 3
* most likely 64bit
* .pkg installer if you are on MacOS

**What's the difference?**
Anaconda is better overall for beginners as it comes preloaded with a lot of packages and
a GUI to launch different tools. If you want to get more into Python in the future
I'd recommend Anaconda. However it is also a large download so if bandwidth
or hard disk space is an issue, go for Miniconda.

### 2. Download this package
* Download by clicking the green 'Clone or download' button above, and choose
'Download ZIP'.
* Unzip the package if necessary.
* You should have a folder called 'gephi_twitter_media_downloader-master'

### 3. Edit the credentials file (optional - do once)
**This is an optional step. if you do not complete step 3 the script will ask you
for your API keys later. Completing step 3 saves you time on repeated uses.**
* You will need your Consumer Key and Consumer Secret from the Twitter API.
You would have generated these when you set up the Gephi plugin.
* Open the 'credentials.py' file using a regular text editor such as Notepad, Textedit
or something better like [Sublime Text](https://www.sublimetext.com).
* Once opened you will see the following...

        CONSUMER_KEY = ''
        CONSUMER_SECRET = ''
* Copy/paste your keys into the file so that it looks something like this (quote marks included)...

        CONSUMER_KEY = '5dsfgsd6dg8dshdg7g'
        CONSUMER_SECRET = 'is88wudndu84740010jf455634ghHNJKHSD66s86dgf'
* Save the file ensuring it still ends with `.py`

### 4a. Prepare your Data: Copy in your Gephi Export
* Create your .csv by opening your Gephi project, going to the Data Laboratory
and clicking Export Table. Save the file as a .csv into the same folder as this script.

### 4b. Prepare your Data: Copy in and prepare your Tweet id .csv
* Ensure your list of twitter ids is saved as a .csv file.
* Ensure your list has a column name, even if it is the only column in the file.
* Make a copy of the .csv file into the same folder as this script.


### 5. Open up the folder in a Command Line
**On Mac**
* [Open up the Terminal](https://www.wikihow.com/Open-a-Terminal-Window-in-Mac).
* Type `cd` and then drag and drop the folder onto the terminal window. This
will automatically add in the full path to your folder.
* Hit return.

**On Windows**
* Open the [command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/)
* Type `cd` and then drag and drop the folder onto the terminal window. This
will automatically add in the full path to your folder.
* Hit return.

### 6. Set up a contained Python Environment (NOT OPTIONAL - do once)
* First we create a self-contained Python 'Environment'. Think of it as a contained
box with Python and all the stuff you'll need just for this script.
* Type the following and hit return.

        conda create -n twitter_env python
* If it asks you to confirm installing packages confirm `y`.

### 7. 'Step into' your new environment
* You will need to tell your command prompt to use your environemnt.
* Type the following and hit return
* For Windows:

        activate twitter_env
* For Mac:

        source activate twitter_env

* If succesful you should see to the far left of your cursor the word `twitter_env`


### 8. Install Package Requirements (NOT OPTIONAL - do once)
Before we can use the script we need to ensure your Python environment has
the packages the script uses. Whether you installed Anaconda or Miniconda
this step is required, but only once.

* In your command line type

        pip install --upgrade -r requirements.txt

* You will see a lot of text run past and hopefully will be presented
with an empty command prompt at the end.

### 9. Quick Checklist
* At this point you should be in a command prompt. On the left it should have the name of the
folder containing the script indicating your command prompt is 'in' your folder.
* You should have a .csv exported from Gephi in the same folder as the script.
* You could have completed step 3, though if you haven't you will be prompted for your credentials soon.
* You should have completed step 6.

### 10a. Run the script: Gephi Compatible
* If you are using a Gephi generated file type the following command and hit enter...

        python download_twitter_media.py -G

* Follow the on-screen instructions

### 10b. Run the script: Tweet Id .csv
* If you are using a list of tweet ids type the following command, replacing `your_column_header` with the name of the column contaning the ids, and hit enter...

        python download_twitter_media.py -c your_column_header

* Follow the on-screen instructions

### 10c. Exclude media by type (optional)
* If you want to exclude certain types of media you can use the following arguments...
    
        -nV #excludes videos
        -nP #excludes photos
        -nA #excludes animated_gifs

* Example: Download only photos using a Gephi generated .csv...

        python download_twitter_media.py -G -nV -nA


### (11). Running the Script again
* Ensure you have moved out your reports and media for safekeeping.
* When you want to use the script again on different data just complete steps
4, 5, 7 and 10, i.e. ...
    * Put your new file in the same directory as the script
    * Open up the folder in the command line
    * Step into your Python environment
    * Run the script



