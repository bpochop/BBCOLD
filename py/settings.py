import tkinter as tk
import json


read = open("./data/theme.json", "r")
theme = json.load(read)
read.close()


class settingsLayout():
    def __init__(self, master):
        super(settingsLayout, self).__init__()

        self.master = master

        self.frame = tk.Frame(master)
        self.setLayout()
        self.frame.pack()

    def setLayout(self):
        # img4 = tk.PhotoImage(file="img/clean.png")
        self.cleanLabel = tk.Button(self.frame, text="\tClean/Prime",
                                    command=self.clean,
                                    relief="flat",
                                    # image=img4,
                                    compound="left",
                                    highlightcolor=theme["button_highlight_color"],
                                    bg=theme["button_colors"])
        self.options = {}
        self.time = tk.StringVar(self.frame)
        self.time.set(" ")
        self.display = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.timeMenu = tk.OptionMenu(self.frame, self.time, *self.display)

        self.MotorUpButton = tk.Button(self.frame,
                                       text="\tMotor Up",
                                       command=self.motorUp,
                                       relief="flat",
                                       # image=img4,
                                       compound="left",
                                       highlightcolor=theme["button_highlight_color"],
                                       bg=theme["button_colors"]
                                       )

        self.motorDownButton = tk.Button(self.frame,
                                         text="\tMotor Down",
                                         command=self.motorDown,
                                         relief="flat",
                                         # image=img4,
                                         compound="left",
                                         highlightcolor=theme["button_highlight_color"],
                                         bg=theme["button_colors"])

        self.turnOffMixer = tk.Button(self.frame,
                                      text="\tTurn OFF Mixer",
                                      command=self.mixerOff,
                                      relief="flat",
                                      # image=img4,
                                      compound="left",
                                      highlightcolor=theme["button_highlight_color"],
                                      bg=theme["button_colors"]
                                      )

        self.turnOnMixer = tk.Button(self.frame,
                                     text="\tTurn ON Mixer",
                                     command=self.mixerOn,
                                     relief="flat",
                                     # image=img4,
                                     compound="left",
                                     highlightcolor=theme["button_highlight_color"],
                                     bg=theme["button_colors"]
                                     )

        self.cleanLabel.grid(row=0, column=1, padx=10, pady=10)
        self.timeMenu.grid(row=0, column=0, padx=10, pady=10)

        self.MotorUpButton.grid(row=1, column=0, padx=10, pady=10)
        self.motorDownButton.grid(row=1, column=1, padx=10, pady=10)

        self.turnOffMixer.grid(row=2, column=0, padx=10, pady=10)
        self.turnOnMixer.grid(row=2, column=1, padx=10, pady=10)

    def mixerOn(self):
        pass
        # CHECK HERE FOR BUGS, ON 3RD DRINK IT KEPT SPINNING FOREVER!
        # mixer_motor.write(0)  # turns on motor

    def mixerOff(self):
        pass
        # mixer_motor.write(1)

    def motorUp(self):
        pass
        '''
        stepper_motor_dir.write(1)
        for x in range(step_count):
            #         GPIO.output(STEP, GPIO.HIGH)
            stepper_motor_step.write(1)
            t.sleep(delay)
            stepper_motor_step.write(0)
            t.sleep(delay)
        stepper_motor_enable.write(1)
        '''

    def motorDown(self):
        pass
        '''
        stepper_motor_enable.write(0)
        t.sleep(1)
        stepper_motor_dir.write(0)

        for x in range(step_count):
            stepper_motor_step.write(1)
            t.sleep(delay)
            stepper_motor_step.write(0)
            t.sleep(delay)
        '''

    def clean(self):
        pass


'''
            pump1_1.write(0)
            pump1_2.write(0)
            pump1_3.write(0)
            pump1_4.write(0)
            pump1_5.write(0)
            pump1_6.write(0)
            pump1_7.write(0)
            pump1_8.write(0)
#             pump2_1.write(0)
#             pump2_2.write(0)
#             pump2_3.write(0)
#             pump2_4.write(0)
#             pump2_5.write(0)
#             pump2_6.write(0)
#             pump2_7.write(0)
#             pump2_8.write(0


            t.sleep(int(self.time.get()))

            pump1_1.write(1)
            pump1_2.write(1)
            pump1_3.write(1)
            pump1_4.write(1)
            pump1_5.write(1)
            pump1_6.write(1)
            pump1_7.write(1)
            pump1_8.write(1)
#             pump2_1.write(1)
#             pump2_2.write(1)
#             pump2_3.write(1)
#             pump2_4.write(1)
#             pump2_5.write(1)
#             pump2_6.write(1)
#             pump2_7.write(1)
#             pump2_8.write(1)
          '''
