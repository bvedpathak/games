import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 40
BULLET_SPEED = 10
BULLET_SIZE = 5

# Enemy settings
ENEMY_SPEED = 3
ENEMY_SIZE = 30
ENEMY_SPAWN_RATE = 60  # frames between enemy spawns

class Player:
    """Player spaceship class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        
    def move(self, keys):
        """Move player based on key input"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            
        # Keep player within screen bounds
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
    def draw(self, screen):
        """Draw the player spaceship"""
        # Draw main body
        pygame.draw.polygon(screen, CYAN, [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
        # Draw cockpit
        pygame.draw.circle(screen, BLUE, 
                         (self.x + self.width // 2, self.y + self.height // 2), 8)
        
    def get_rect(self):
        """Get rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    """Bullet class for player shots"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET_SIZE
        self.height = BULLET_SIZE
        self.speed = BULLET_SPEED
        self.active = True
        
    def update(self):
        """Move bullet upward"""
        self.y -= self.speed
        
    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        """Get rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_off_screen(self):
        """Check if bullet is off screen"""
        return self.y < -self.height

class Enemy:
    """Enemy class for aliens/meteors"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.speed = ENEMY_SPEED
        self.active = True
        self.enemy_type = random.choice(['alien', 'meteor'])
        
    def update(self):
        """Move enemy downward"""
        self.y += self.speed
        
    def draw(self, screen):
        """Draw the enemy"""
        if self.enemy_type == 'alien':
            # Draw alien
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, WHITE, 
                             (self.x + self.width // 2, self.y + self.height // 2), 5)
        else:
            # Draw meteor
            pygame.draw.polygon(screen, (100, 100, 100), [
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ])
            
    def get_rect(self):
        """Get rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_off_screen(self):
        """Check if enemy is off screen"""
        return self.y > SCREEN_HEIGHT

class Star:
    """Background star class"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
        
    def update(self):
        """Move star downward"""
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
            
    def draw(self, screen):
        """Draw the star"""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, 
                           SCREEN_HEIGHT - PLAYER_SIZE - 20)
        self.bullets = []
        self.enemies = []
        self.stars = [Star() for _ in range(50)]
        
        # Game state
        self.enemy_spawn_timer = 0
        self.shoot_delay = 0
        
        # Load sounds (if available)
        self.shoot_sound = None
        self.explosion_sound = None
        self.load_sounds()
        
    def load_sounds(self):
        """Load game sounds if available"""
        try:
            # Create simple sounds programmatically
            self.shoot_sound = pygame.mixer.Sound(self.create_beep_sound(800, 100))
            self.explosion_sound = pygame.mixer.Sound(self.create_beep_sound(200, 200))
        except:
            pass
            
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound"""
        sample_rate = 22050
        num_samples = int(sample_rate * duration / 1000)
        sound_data = []
        
        for i in range(num_samples):
            sample = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_data.append(sample)
            
        # Convert to bytes
        sound_bytes = bytes(sound_data)
        
        # Create a temporary file
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.write(sound_bytes)
        temp_file.close()
        
        return temp_file.name
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move player
        self.player.move(keys)
        
        # Handle shooting
        if keys[pygame.K_SPACE] and self.shoot_delay <= 0:
            self.shoot()
            self.shoot_delay = 10
            
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                
        # Update stars
        for star in self.stars:
            star.update()
            
        # Check collisions
        self.check_collisions()
        
    def shoot(self):
        """Create a new bullet"""
        bullet_x = self.player.x + self.player.width // 2 - BULLET_SIZE // 2
        bullet_y = self.player.y
        bullet = Bullet(bullet_x, bullet_y)
        self.bullets.append(bullet)
        
        # Play shoot sound
        if self.shoot_sound:
            self.shoot_sound.play()
            
    def spawn_enemy(self):
        """Spawn a new enemy"""
        x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        y = -ENEMY_SIZE
        enemy = Enemy(x, y)
        self.enemies.append(enemy)
        
    def check_collisions(self):
        """Check for collisions between game objects"""
        player_rect = self.player.get_rect()
        
        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                enemy_rect = enemy.get_rect()
                if bullet_rect.colliderect(enemy_rect):
                    # Remove bullet and enemy
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    # Increase score
                    self.player.score += 10
                    # Play explosion sound
                    if self.explosion_sound:
                        self.explosion_sound.play()
                    break
                    
        # Check player-enemy collisions
        for enemy in self.enemies[:]:
            enemy_rect = enemy.get_rect()
            if player_rect.colliderect(enemy_rect):
                # Remove enemy
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                # Decrease lives
                self.player.lives -= 1
                # Play explosion sound
                if self.explosion_sound:
                    self.explosion_sound.play()
                    
                # Check game over
                if self.player.lives <= 0:
                    self.game_over = True
                    
    def draw(self):
        """Draw all game objects"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            star.draw(self.screen)
            
        # Draw game objects
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
            
        # Update display
        pygame.display.flip()
        
    def draw_ui(self):
        """Draw user interface elements"""
        font = pygame.font.Font(None, 36)
        
        # Draw score
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 48)
        
        # Game Over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = font_small.render(f"Final Score: {self.player.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(final_score_text, score_rect)
        
        # Restart instruction
        restart_text = font_small.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
    def restart_game(self):
        """Restart the game"""
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, 
                           SCREEN_HEIGHT - PLAYER_SIZE - 20)
        self.bullets = []
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.shoot_delay = 0
        self.game_over = False
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

def main():
    """Main function to run the game"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
