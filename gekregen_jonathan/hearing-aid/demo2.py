import snowboydecoder
import sys
import signal

# Demo code for listening to two hotwords at the same time

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def say_things(number):
    if number == 1:
        print("Hello, how can I be of service")
    elif number == 2:
        print("Gerrit is not home at the moment, sorry.")
    elif number == 3:
        print("You said one")
    elif number == 4:
        print("You said two")
    elif number == 5:
        print("You said three")



def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 6:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: say_things(1),
             lambda: say_things(2),
             lambda: say_things(3),
             lambda: say_things(4),
             lambda: say_things(5)]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
