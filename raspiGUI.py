

#import modules for project
import PySimpleGUI as sg
from gpiozero import LED,PWMLED

#define variables
led = PWMLED(4)
relay = LED(17)

#main layout
layout = [[sg.text('Colins Raspberry Pi GUI Controller', font=("Helvetica",75))] #this is a text box
            [sg.Button('Light',button_color='white on red', font=("Helvetica",75),pad=(5,5),key='-B-')] #this is a button
            [sg.Slider(range=(0,10), default_value=10, orientation="h", key="brightness", size=(40,30), enable_events=True)], #this is a slider
            [sg.Button("Relay", font=("Helvetica",75),pad=(5,5), button_color="white on red",key='-B2-')], #this is a button
            [sg.Exit()]] #exit button to get out of gui


#declare a window
#this is what shows on the raspberry pi, make sure that layout fits raspberry pi screen
window = sg.Window('My name is Colin and I am a programmer', layout, size=(800,400), element_justification="center", finalize=True)
window.Maximize()

#two variables to hold the state of if the button is up or down
down = False
b2down = False

#while loop to keep window updating
while True:                                 #Event loop
    event, values = window.read()
    print(event, values)                    #prints values to terminal window
    if event in (sg.WIN_CLOSED, 'Exit'):    #exit clause
        led.off()                           #if GUI is closed, turn off LED
        relay.off()                         #if GUI is closed, turn off relay
        break
    elif event == '-B-':                    #if LED button is pressed
        down = not down                     #changes state of down variable
        #the update call changes the color of the button and text
        window['-B-'].update(button_color='white on green' if down else 'white on red')
        if down:                            #makes sure the LED is on, then sets it to max brightness
            window['brightness'].update(10) #resets the slider to 10
            led.value = 1
        else:
            led.off()                       #if the button state is off, turns LED off
    elif event == '-B2-':                   #button 2 to control the relay
        b2down = not b2down
        #same function as for -B- to toggle the colors of the button and text
        window['-B2-'].update(button_color='white on green' if b2down else 'white on red')
        if b2down:                          #simple if statement, turns on or off based on button state
            relay.on()
        else:
            relay.off()
    elif event == 'brightness':             #checks  if the slider has been changed
        if down:                            #if the slider is changed and LED is turned on
            led.value = values['brightness']/10     #scales slider value/10

window.close()