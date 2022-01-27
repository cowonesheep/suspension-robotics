import pygame
import serial
import time

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pygame Demonstration")

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    mainloop = True
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
                if event.key == pygame.K_1:
                    ser.write(b"1\n")
                if event.key == pygame.K_2:
                    ser.write(b"2\n")
                if event.key == pygame.K_3:
                    ser.write(b"3\n")
                if event.key == pygame.K_4:
                    ser.write(b"4\n")
                if event.key == pygame.K_5:
                    ser.write(b"5\n")
                if event.key == pygame.K_6:
                    ser.write(b"6\n")
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
pygame.quit()
