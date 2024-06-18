import pygame

class SpriteSheet():
	def __init__(self, image, num_of_images):
		self.sheet = image
		self.frame_width = self.sheet.get_width() // num_of_images
		self.frame_height= self.sheet.get_height()

	def get_image(self, frame, scale):
		"""
		Takes the current frame of the spritesheet to be returned as well as
		and integer value for scaling.
		"""
		image = pygame.Surface((self.frame_width, self.frame_height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * self.frame_width), 0, self.frame_width, self.frame_height))
		image = pygame.transform.scale(image, (self.frame_width * scale, self.frame_height* scale))

		return image
	