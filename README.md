# minimal-flask-app
Minimal code for Flask app making calls to the OpenAI API


```
# Create virtual environment
python3 -m venv ./venv

# Activate your virtual environment
source venv/bin/activate
./venv/Scripts/activate

# Install the required packages. For example
pip3 install flask openai python-dotenv

# Rename the file .env-bup to .env 
# Add your OPENAI_API_KEY to the .env file.

# Run the app
python3 app.py

REFLECTION: For the Jungian Dream Analysis Machine, I prompted the model to analyse user submitted dreams in the context of Jungian ideas like archetypes(Shadow, Anima/Animus, Self, Hero, Wise Old Man, etc.), symbolism, collective unconscious, emotional patterns and personal growth themes. I said to ‘Provide thoughtful, reflective interpretations. Avoid medical diagnoses.
Speak clearly and empathetically’. I had a bit more fun on the image synthesis side of things, where I attempted to use adjectives like ‘ethereal’ and references like dadaism and the polish artist Zdzisław Beksiński to refine the images into a more bizarre, dreamlike aesthetic.

I had multiple issues before I was able to have a working app. Initially, this was all problems with not being able to upload all my files to github. My commit history is probably confusing because I deleted and recreated the same repository multiple times. Essentially, I had multiple copies of the app on my local system and this was causing very confusing problems when attempting to sync changes to the repository. Eventually I resolved this, and my next problems came when I got to using Render.

I initially did not include installing Pillow in the Render build command, which seemed to cause issues. I noticed that Pillow was not importing so I fixed this by changing my Render build command to include Pillow. Finally, the most frustrating and evasive was with gunicorn. My app kept showing a blank screen that said ‘internal server error’ every time I tried to submit a dream. It wasn’t until a long time had passed and I carefully checked all the render logs that I realized my gunicorn worker kept timing out. Requests of this kind are obviously lengthy and I guess the default timeout time was very short, so my app kept crashing. I changed the start command to gunicorn --timeout 6000 app:app and finally my app worked. 

The app is simple. There is a submission box for dreams and a button prompting the user to analyse the typed dream. When the user clicks the button, the application returns a short paragraph contextualizing the dream in Jungian ideas as well as a visual representation of the same dream right below the paragraph. If I had spent less time getting the app the worked, I would have liked to have further stylized the website and found a more interesting way to display the image output.

```
