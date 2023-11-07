import pygame
import pyaudio
import numpy as np
import vlc
# 2.11.23 Fungerar!
# 7.11.23 This is the current workfile

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Tuukka Kaila")
# Set the screen dimensions to match your display resolution
screen_width = 1280 # Change this to your display width
screen_height = 800 # Change this to your display height

# Create a fullscreen display surface
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
#Hide the cursor
pygame.mouse.set_visible(False)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

# Initialize VLC and open the stream
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
#Stream URL
media = vlc_instance.media_new("http://5.9.106.210/vlf39")
player.set_media(media)
player.play()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False

    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    frequency = np.abs(np.fft.fft(data))[:len(data) // 2].argmax()

    # Map frequency to color
    color = (frequency % 50, 10 - (frequency % 10), 50)

    screen.fill(color)
    pygame.display.flip()
    clock.tick(76)

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
