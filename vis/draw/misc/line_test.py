import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
draw_set = True
a = (-100, -100)
b = (20, 200)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			draw_set = not draw_set
		
	screen.fill('black')
	
	if draw_set: # incorrect lines
		pygame.draw.line(screen, 'red', a, b, 15)
		pygame.draw.line(screen, 'blue', (-29, 131), (21, 106),  5)
		pygame.draw.line(screen, 'blue', (-58, 262), (42, 212),  5)
	else: # correct lines
		pygame.draw.line(screen, 'red', b, a, 15) # reversed is fine
		pygame.draw.line(screen, 'blue', (-29, 131), (20, 106),  5) # offset by 1, not extended

	pygame.display.update()
	clock.tick(60)