#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frogger - Klasyczna Gra Przechodzenia Przez Ulicę (Enhanced Graphics)

Gra w stylu klasycznego Froggera, gdzie gracz musi przeprowadzić żabę
przez ruchliwą ulicę i rzekę pełną kłód.

Author: Sebastian Januchowski
Email: polsoft.its@fastservice.com
GitHub: https://github.com/seb07uk
Organization: polsoft.ITS™ London
Copyright: 2026© Sebastian Januchowski. All rights reserved.
Version: 2.0.0 (Enhanced Graphics)
Date: 2026-02-09
License: All rights reserved
"""

__author__ = "Sebastian Januchowski"
__copyright__ = "2026© Sebastian Januchowski. All rights reserved."
__credits__ = ["Sebastian Januchowski"]
__license__ = "All rights reserved"
__version__ = "2.0.0"
__maintainer__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__status__ = "Production"
__organization__ = "polsoft.ITS™ London"
__github__ = "https://github.com/seb07uk"

import pygame
import sys
import random
import json
import os
import math
from typing import List, Tuple, Dict
from datetime import datetime
from pathlib import Path

# Inicjalizacja Pygame
pygame.init()

# Stałe gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 50
FPS = 60

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
BLUE = (65, 105, 225)
DARK_BLUE = (25, 60, 140)
DARK_GRAY = (68, 68, 68)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
SKY_BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Konfiguracja ścieżek
def get_config_path() -> Path:
    """
    Zwraca ścieżkę do pliku konfiguracyjnego.
    
    Windows: %USERPROFILE%\.polsoft\games\Frogger.json
    Linux/Mac: ~/.polsoft/games/Frogger.json
    """
    if os.name == 'nt':  # Windows
        base_path = Path(os.environ.get('USERPROFILE', os.path.expanduser('~')))
    else:  # Linux/Mac
        base_path = Path.home()
    
    config_dir = base_path / '.polsoft' / 'games'
    config_dir.mkdir(parents=True, exist_ok=True)
    
    return config_dir / 'Frogger.json'

# Plik z wynikami i ustawieniami
CONFIG_FILE = get_config_path()


class ParticleSystem:
    """System cząsteczek dla efektów wizualnych."""
    
    def __init__(self):
        self.particles = []
    
    def add_splash(self, x: float, y: float):
        """Dodaje efekt rozchlapania wody."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed - random.uniform(2, 4),
                'life': random.randint(20, 40),
                'max_life': 40,
                'type': 'splash',
                'size': random.randint(3, 6)
            })
    
    def add_hop(self, x: float, y: float):
        """Dodaje efekt pyłu przy skoku."""
        for _ in range(5):
            self.particles.append({
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-5, 5),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'life': random.randint(10, 20),
                'max_life': 20,
                'type': 'dust',
                'size': random.randint(2, 4)
            })
    
    def add_crash(self, x: float, y: float):
        """Dodaje efekt zderzenia."""
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(15, 30),
                'max_life': 30,
                'type': 'crash',
                'size': random.randint(4, 8)
            })
    
    def update(self):
        """Aktualizuje wszystkie cząsteczki."""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Grawitacja
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Rysuje wszystkie cząsteczki."""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            
            if particle['type'] == 'splash':
                color = (100, 150, 255, alpha)
            elif particle['type'] == 'dust':
                color = (200, 200, 150, alpha)
            elif particle['type'] == 'crash':
                color = (255, 100, 0, alpha)
            else:
                color = (255, 255, 255, alpha)
            
            # Pygame nie wspiera alpha bezpośrednio w draw.circle,
            # więc używamy powierzchni z alpha
            size = int(particle['size'] * (particle['life'] / particle['max_life']))
            if size > 0:
                surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color[:3] + (alpha,), (size, size), size)
                screen.blit(surf, (int(particle['x'] - size), int(particle['y'] - size)))


class WaterEffect:
    """Klasa odpowiedzialna za animowany efekt wody."""
    
    def __init__(self):
        self.time = 0
        self.wave_offset = 0
    
    def update(self):
        """Aktualizuje animację wody."""
        self.time += 0.05
        self.wave_offset = math.sin(self.time) * 3
    
    def draw(self, screen: pygame.Surface, rect: pygame.Rect):
        """Rysuje animowaną wodę."""
        # Gradient wody
        for i in range(rect.height):
            color_value = 65 + int(40 * math.sin(self.time + i * 0.1))
            color = (0, color_value, 150 + int(30 * math.sin(self.time + i * 0.05)))
            pygame.draw.line(screen, color, 
                           (rect.x, rect.y + i), 
                           (rect.x + rect.width, rect.y + i))
        
        # Fale
        for y in range(rect.y, rect.y + rect.height, 20):
            for x in range(0, rect.width, 30):
                wave_y = y + int(self.wave_offset * math.sin((x + self.time * 50) * 0.1))
                if rect.y <= wave_y < rect.y + rect.height:
                    pygame.draw.circle(screen, (100, 150, 255, 100), 
                                     (rect.x + x, wave_y), 3, 1)


class ConfigManager:
    """
    Klasa zarządzająca konfiguracją gry i wynikami.
    
    Zapisuje dane w formacie:
    {
        "settings": {
            "sound_enabled": true,
            "music_enabled": true,
            "difficulty": "normal",
            "last_played": "2026-02-09 14:30:00"
        },
        "scores": [
            {"name": "Player1", "score": 500, "date": "2026-02-09 14:30"}
        ],
        "statistics": {
            "total_games": 10,
            "total_score": 2500,
            "highest_score": 500
        }
    }
    """
    
    def __init__(self, filename: Path = CONFIG_FILE):
        """Inicjalizuje menedżera konfiguracji."""
        self.filename = filename
        self.config = self.load_config()
        
        # Inicjalizuj domyślne ustawienia jeśli nie istnieją
        if 'settings' not in self.config:
            self.config['settings'] = {
                'sound_enabled': True,
                'music_enabled': True,
                'difficulty': 'normal',
                'last_played': None
            }
        
        if 'scores' not in self.config:
            self.config['scores'] = []
        
        if 'statistics' not in self.config:
            self.config['statistics'] = {
                'total_games': 0,
                'total_score': 0,
                'highest_score': 0
            }
    
    def load_config(self) -> Dict:
        """Loads configuration from JSON file."""
        if self.filename.exists():
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading configuration: {e}")
                return {}
        return {}
    
    def save_config(self):
        """Saves configuration to JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"Configuration saved: {self.filename}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get_setting(self, key: str, default=None):
        """Pobiera ustawienie."""
        return self.config['settings'].get(key, default)
    
    def set_setting(self, key: str, value):
        """Ustawia wartość ustawienia."""
        self.config['settings'][key] = value
        self.save_config()
    
    def update_last_played(self):
        """Aktualizuje czas ostatniej gry."""
        self.config['settings']['last_played'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_config()
    
    def get_scores(self) -> List[Dict]:
        """Zwraca listę wyników."""
        return self.config.get('scores', [])
    
    def add_score(self, name: str, score: int) -> int:
        """
        Dodaje nowy wynik do listy.
        
        Args:
            name: Imię gracza
            score: Osiągnięty wynik
            
        Returns:
            Pozycja w rankingu (1-5) lub 0 jeśli nie wszedł do top 5
        """
        new_entry = {
            'name': name,
            'score': score,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        self.config['scores'].append(new_entry)
        self.config['scores'].sort(key=lambda x: x['score'], reverse=True)
        self.config['scores'] = self.config['scores'][:5]  # Zachowaj tylko top 5
        
        # Aktualizuj statystyki
        self.update_statistics(score)
        
        self.save_config()
        
        # Sprawdź pozycję
        for i, entry in enumerate(self.config['scores']):
            if entry == new_entry:
                return i + 1
        return 0
    
    def update_statistics(self, score: int):
        """Aktualizuje statystyki gry."""
        stats = self.config['statistics']
        stats['total_games'] += 1
        stats['total_score'] += score
        if score > stats['highest_score']:
            stats['highest_score'] = score
    
    def is_high_score(self, score: int) -> bool:
        """Sprawdza czy wynik kwalifikuje się do top 5."""
        scores = self.get_scores()
        if len(scores) < 5:
            return True
        return score > scores[-1]['score']
    
    def get_statistics(self) -> Dict:
        """Zwraca statystyki gry."""
        return self.config.get('statistics', {})


class ScoreManager:
    """
    Klasa zarządzająca najlepszymi wynikami.
    
    Używa ConfigManager do zarządzania wynikami.
    """
    
    def __init__(self):
        """Inicjalizuje menedżera wyników."""
        self.config_manager = ConfigManager()
    
    def load_scores(self) -> List[Dict]:
        """Wczytuje wyniki."""
        return self.config_manager.get_scores()
    
    def save_scores(self):
        """Zapisuje wyniki."""
        self.config_manager.save_config()
    
    def add_score(self, name: str, score: int) -> int:
        """Dodaje nowy wynik."""
        return self.config_manager.add_score(name, score)
    
    def get_top_scores(self) -> List[Dict]:
        """Zwraca listę top 5 wyników."""
        return self.config_manager.get_scores()
    
    def is_high_score(self, score: int) -> bool:
        """Sprawdza czy wynik kwalifikuje się do top 5."""
        return self.config_manager.is_high_score(score)


class Menu:
    """
    Class representing the game's main menu.
    
    Handles navigation between options and displaying different screens.
    """
    
    def __init__(self, screen: pygame.Surface):
        """Initializes the menu."""
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.options = ["NEW GAME", "TOP 5", "HELP", "EXIT"]
        self.selected = 0
        self.state = "main"  # main, top5, help
        
        self.score_manager = ScoreManager()
        self.pulse = 0  # For animation
    
    def draw_title(self):
        """Draws the game title with enhanced graphics."""
        self.pulse += 0.05
        pulse_offset = int(math.sin(self.pulse) * 3)
        
        # Multi-layer shadow for depth
        for offset in range(5, 0, -1):
            shadow_color = (20 + offset * 5, 20 + offset * 5, 20 + offset * 5)
            title_shadow = self.font_large.render("FROGGER", True, shadow_color)
            self.screen.blit(title_shadow, 
                           (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + offset, 
                            50 + offset))
        
        # Main title with gradient effect (simulated with multiple renders)
        title = self.font_large.render("FROGGER", True, (50, 200 + pulse_offset, 50))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Highlight
        title_highlight = self.font_large.render("FROGGER", True, (150, 255, 150))
        title_highlight.set_alpha(100)
        self.screen.blit(title_highlight, 
                        (SCREEN_WIDTH // 2 - title_highlight.get_width() // 2, 48))
        
        # Subtitle
        subtitle = self.font_small.render("Enhanced Graphics Edition", True, GOLD)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))
        
        # Copyright
        copyright_text = self.font_tiny.render(
            "polsoft.ITS™ London © 2026 Sebastian Januchowski",
            True, LIGHT_GREEN
        )
        self.screen.blit(copyright_text, 
                        (SCREEN_WIDTH // 2 - copyright_text.get_width() // 2, 170))
    
    def draw_main_menu(self):
        """Draws the main menu with enhanced background."""
        # Gradient background
        for i in range(SCREEN_HEIGHT):
            color_value = int(i / SCREEN_HEIGHT * 30)
            pygame.draw.line(self.screen, (color_value, color_value, color_value), 
                           (0, i), (SCREEN_WIDTH, i))
        
        # Animated background pattern
        time_offset = pygame.time.get_ticks() * 0.001
        for i in range(0, SCREEN_WIDTH, 50):
            for j in range(0, SCREEN_HEIGHT, 50):
                alpha = int(20 + 10 * math.sin(time_offset + i * 0.01 + j * 0.01))
                color = (0, alpha, 0)
                pygame.draw.rect(self.screen, color, (i, j, 45, 45), 1)
        
        self.draw_title()
        
        # Menu options with glow effect
        start_y = 250
        spacing = 80
        
        for i, option in enumerate(self.options):
            if i == self.selected:
                # Glow effect
                for glow_size in range(5, 0, -1):
                    glow_color = (255 - glow_size * 30, 255 - glow_size * 30, 0)
                    glow_text = self.font_medium.render(f"> {option} <", True, glow_color)
                    glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
                    glow_text.set_alpha(50)
                    self.screen.blit(glow_text, glow_rect.move(0, glow_size))
                
                # Highlighted option
                text = self.font_medium.render(f"> {option} <", True, YELLOW)
                # Frame around selected option
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
                
                # Animated border
                pulse_width = int(3 + math.sin(self.pulse * 2) * 1)
                pygame.draw.rect(self.screen, YELLOW, rect.inflate(20, 10), pulse_width)
            else:
                text = self.font_medium.render(option, True, WHITE)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            self.screen.blit(text, text_rect)
        
        # Instructions
        instructions = self.font_tiny.render(
            "Use ↑↓ to select, ENTER to confirm",
            True, LIGHT_GREEN
        )
        self.screen.blit(instructions, 
                        (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 600))
    
    def draw_top5(self):
        """Draws the top 5 scores screen."""
        # Gradient background
        for i in range(SCREEN_HEIGHT):
            color_value = int(i / SCREEN_HEIGHT * 30)
            pygame.draw.line(self.screen, (color_value, color_value, 20), 
                           (0, i), (SCREEN_WIDTH, i))
        
        # Background pattern
        for i in range(0, SCREEN_WIDTH, 50):
            for j in range(0, SCREEN_HEIGHT, 50):
                alpha = 20
                color = (alpha, alpha, 0)
                pygame.draw.rect(self.screen, color, (i, j, 45, 45), 1)
        
        # Title with shadow
        for offset in range(3, 0, -1):
            title_shadow = self.font_large.render("TOP 5 SCORES", True, (100, 100, 0))
            self.screen.blit(title_shadow, 
                           (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + offset, 50 + offset))
        
        title = self.font_large.render("TOP 5 SCORES", True, GOLD)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Scores list
        scores = self.score_manager.get_top_scores()
        start_y = 180
        spacing = 80
        
        if not scores:
            no_scores = self.font_medium.render("No scores yet", True, WHITE)
            self.screen.blit(no_scores, 
                           (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, 300))
        else:
            medal_colors = [GOLD, SILVER, BRONZE, WHITE, WHITE]
            
            for i, entry in enumerate(scores):
                y_pos = start_y + i * spacing
                color = medal_colors[i]
                
                # Draw podium background for top 3
                if i < 3:
                    bg_height = 60
                    bg_rect = pygame.Rect(80, y_pos - 10, SCREEN_WIDTH - 160, bg_height)
                    # Gradient background
                    for j in range(bg_height):
                        alpha = int(50 - j * 0.5)
                        pygame.draw.line(self.screen, (*color[:3], alpha), 
                                       (bg_rect.x, bg_rect.y + j), 
                                       (bg_rect.x + bg_rect.width, bg_rect.y + j))
                    pygame.draw.rect(self.screen, color, bg_rect, 2)
                
                # Position
                if i < 3:
                    medal = ["🥇", "🥈", "🥉"][i]
                    pos_text = self.font_medium.render(f"{i+1}. {medal}", True, color)
                else:
                    pos_text = self.font_medium.render(f"{i+1}.", True, color)
                
                self.screen.blit(pos_text, (100, y_pos))
                
                # Name
                name_text = self.font_medium.render(entry['name'][:15], True, color)
                self.screen.blit(name_text, (220, y_pos))
                
                # Score
                score_text = self.font_medium.render(f"{entry['score']} pts", True, color)
                self.screen.blit(score_text, (500, y_pos))
        
        # Instructions
        back_text = self.font_small.render("Press ESC to go back", True, LIGHT_GREEN)
        self.screen.blit(back_text, 
                        (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 630))
    
    def draw_help(self):
        """Draws the help screen."""
        # Gradient background
        for i in range(SCREEN_HEIGHT):
            color_value = int(i / SCREEN_HEIGHT * 40)
            pygame.draw.line(self.screen, (0, color_value, color_value), 
                           (0, i), (SCREEN_WIDTH, i))
        
        # Background pattern
        for i in range(0, SCREEN_WIDTH, 50):
            for j in range(0, SCREEN_HEIGHT, 50):
                alpha = 20
                color = (0, alpha, alpha)
                pygame.draw.rect(self.screen, color, (i, j, 45, 45), 1)
        
        # Title
        for offset in range(3, 0, -1):
            title_shadow = self.font_large.render("HELP", True, (0, 100, 100))
            self.screen.blit(title_shadow, 
                           (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + offset, 30 + offset))
        
        title = self.font_large.render("HELP", True, CYAN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Instructions
        help_text = [
            ("OBJECTIVE:", YELLOW, True),
            ("Guide the frog across the road and river to reach the goal!", WHITE, False),
            ("", WHITE, False),
            ("CONTROLS:", YELLOW, True),
            ("↑ - Move forward", WHITE, False),
            ("↓ - Move backward", WHITE, False),
            ("← - Move left", WHITE, False),
            ("→ - Move right", WHITE, False),
            ("", WHITE, False),
            ("SCORING:", YELLOW, True),
            ("Move forward: +10 points", GREEN, False),
            ("Reach goal: +100 points", GREEN, False),
            ("", WHITE, False),
            ("RULES:", YELLOW, True),
            ("• Avoid cars on the road", RED, False),
            ("• Jump on logs in the river", BROWN, False),
            ("• Don't fall into the water!", BLUE, False),
            ("• You have 3 lives", MAGENTA, False),
        ]
        
        y_pos = 120
        for text, color, is_bold in help_text:
            font = self.font_medium if is_bold else self.font_small
            rendered = font.render(text, True, color)
            x_pos = SCREEN_WIDTH // 2 - rendered.get_width() // 2 if is_bold else 100
            self.screen.blit(rendered, (x_pos, y_pos))
            y_pos += 35 if is_bold else 28
        
        # Back instructions
        back_text = self.font_small.render("Press ESC to go back", True, LIGHT_GREEN)
        self.screen.blit(back_text, 
                        (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 650))
    
    def handle_input(self, event) -> str:
        """
        Handles user input in the menu.
        
        Returns:
            Action to perform: 'start', 'quit', None
        """
        if event.type == pygame.KEYDOWN:
            if self.state == "main":
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:  # New game
                        return 'start'
                    elif self.selected == 1:  # Top 5
                        self.state = 'top5'
                    elif self.selected == 2:  # Help
                        self.state = 'help'
                    elif self.selected == 3:  # Exit
                        return 'quit'
            
            elif self.state in ['top5', 'help']:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'main'
        
        return None
    
    def draw(self):
        """Draws the current menu state."""
        if self.state == "main":
            self.draw_main_menu()
        elif self.state == "top5":
            self.draw_top5()
        elif self.state == "help":
            self.draw_help()


class Vehicle:
    """
    Klasa reprezentująca pojazd na drodze z ulepszoną grafiką.
    
    Attributes:
        x (float): Pozycja X pojazdu
        y (int): Pozycja Y pojazdu
        width (int): Szerokość pojazdu
        height (int): Wysokość pojazdu
        speed (float): Prędkość pojazdu
        direction (int): Kierunek ruchu (1 lub -1)
        color (tuple): Kolor pojazdu
        vehicle_type (str): Typ pojazdu (car, truck)
    """
    
    def __init__(self, x: float, y: int, width: int, height: int, 
                 speed: float, direction: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.color = color
        self.vehicle_type = "truck" if width > 85 else "car"
    
    def update(self):
        """Aktualizuje pozycję pojazdu."""
        self.x += self.speed * self.direction
        
        # Resetuj pozycję gdy pojazd wyjdzie poza ekran
        if self.direction > 0 and self.x > SCREEN_WIDTH:
            self.x = -self.width
        elif self.direction < 0 and self.x < -self.width:
            self.x = SCREEN_WIDTH
    
    def draw(self, screen: pygame.Surface):
        """Rysuje pojazd na ekranie z ulepszoną grafiką."""
        # Cień
        shadow_surf = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), 
                          shadow_surf.get_rect())
        screen.blit(shadow_surf, (self.x - 5, self.y + self.height - 5))
        
        # Główne ciało pojazdu z gradientem (symulowane)
        for i in range(self.height):
            shade = int(i / self.height * 40)
            adjusted_color = tuple(max(0, min(255, c - shade)) for c in self.color)
            pygame.draw.line(screen, adjusted_color, 
                           (self.x, self.y + i), 
                           (self.x + self.width, self.y + i))
        
        # Obramowanie
        pygame.draw.rect(screen, tuple(max(0, c - 50) for c in self.color), 
                        (self.x, self.y, self.width, self.height), 2)
        
        # Okna z refleksją
        window_height = 15
        window_y = self.y + 5
        
        # Przednie okno
        if self.direction > 0:  # Jedzie w prawo
            window_x = self.x + self.width - 25
        else:  # Jedzie w lewo
            window_x = self.x + 10
        
        # Ciemniejsze okno (szkło)
        pygame.draw.rect(screen, (50, 70, 90), 
                        (window_x, window_y, 20, window_height))
        # Refleks
        pygame.draw.rect(screen, (150, 180, 200), 
                        (window_x, window_y, 20, 5), 1)
        
        # Światła
        if self.direction > 0:  # Światła przednie (prawo)
            # Reflektory
            light_color = (255, 255, 200)
            pygame.draw.circle(screen, light_color, 
                             (int(self.x + self.width - 5), int(self.y + self.height // 2)), 3)
        else:  # Światła tylne (lewo)
            # Światła stop
            light_color = (255, 50, 50)
            pygame.draw.circle(screen, light_color, 
                             (int(self.x + 5), int(self.y + self.height // 2)), 3)
        
        # Dodatkowe detale dla ciężarówek
        if self.vehicle_type == "truck":
            # Przyczepa
            pygame.draw.rect(screen, tuple(max(0, c - 30) for c in self.color),
                           (self.x + 15, self.y + 8, self.width - 30, self.height - 16), 1)
    
    def get_rect(self) -> pygame.Rect:
        """Zwraca prostokąt kolizji pojazdu."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Log:
    """
    Klasa reprezentująca kłodę w rzece z ulepszoną grafiką.
    
    Attributes:
        x (float): Pozycja X kłody
        y (int): Pozycja Y kłody
        width (int): Szerokość kłody
        height (int): Wysokość kłody
        speed (float): Prędkość kłody
        direction (int): Kierunek ruchu (1 lub -1)
        color (tuple): Kolor kłody
    """
    
    def __init__(self, x: float, y: int, width: int, height: int, 
                 speed: float, direction: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.color = color
        self.wood_rings = []
        
        # Generuj losowe słoje drewna
        for _ in range(random.randint(2, 4)):
            self.wood_rings.append({
                'x': random.randint(10, width - 10),
                'size': random.randint(5, 10)
            })
    
    def update(self):
        """Aktualizuje pozycję kłody."""
        self.x += self.speed * self.direction
        
        # Resetuj pozycję gdy kłoda wyjdzie poza ekran
        if self.direction > 0 and self.x > SCREEN_WIDTH:
            self.x = -self.width
        elif self.direction < 0 and self.x < -self.width:
            self.x = SCREEN_WIDTH
    
    def draw(self, screen: pygame.Surface):
        """Rysuje kłodę na ekranie z ulepszoną grafiką."""
        # Cień w wodzie
        shadow_surf = pygame.Surface((self.width, self.height + 5), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 50, 100), 
                          shadow_surf.get_rect())
        screen.blit(shadow_surf, (self.x, self.y + 5))
        
        # Główna część kłody z gradientem
        for i in range(self.height):
            shade = int(abs(i - self.height // 2) / (self.height // 2) * 30)
            adjusted_color = tuple(max(0, c - shade) for c in self.color)
            pygame.draw.line(screen, adjusted_color, 
                           (self.x, self.y + i), 
                           (self.x + self.width, self.y + i))
        
        # Zaokrąglone końce
        end_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.circle(screen, end_color, 
                         (int(self.x), int(self.y + self.height // 2)), 
                         self.height // 2)
        pygame.draw.circle(screen, end_color, 
                         (int(self.x + self.width), int(self.y + self.height // 2)), 
                         self.height // 2)
        
        # Tekstura drewna - słoje
        for i in range(3):
            line_color = (int(self.color[0] * 0.7), int(self.color[1] * 0.7), int(self.color[2] * 0.7))
            y_pos = self.y + 10 + i * 12
            # Faliste linie
            points = []
            for x in range(0, int(self.width), 5):
                wave = int(math.sin(x * 0.2) * 2)
                points.append((self.x + x, y_pos + wave))
            if len(points) > 1:
                pygame.draw.lines(screen, line_color, False, points, 1)
        
        # Słoje drewna na końcach
        for ring in self.wood_rings:
            ring_color = tuple(max(0, c - 50) for c in self.color)
            for size in range(ring['size'], 0, -2):
                pygame.draw.circle(screen, ring_color, 
                                 (int(self.x + ring['x']), int(self.y + self.height // 2)), 
                                 size, 1)
        
        # Highlight na górze
        highlight_surf = pygame.Surface((self.width, 5), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surf, (*self.color, 100), highlight_surf.get_rect())
        screen.blit(highlight_surf, (self.x, self.y))
    
    def get_rect(self) -> pygame.Rect:
        """Zwraca prostokąt kolizji kłody."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Frog:
    """
    Klasa reprezentująca gracza (żabę) z ulepszoną grafiką.
    
    Attributes:
        x (int): Pozycja X żaby
        y (int): Pozycja Y żaby
        size (int): Rozmiar żaby
        lives (int): Liczba żyć
        score (int): Wynik gracza
        direction (str): Kierunek patrzenia żaby
    """
    
    def __init__(self, x: int, y: int, size: int):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.size = size
        self.lives = 3
        self.score = 0
        self.direction = "up"  # up, down, left, right
        self.hop_animation = 0
        self.hop_height = 0
    
    def move(self, dx: int, dy: int):
        """Przesuwa żabę o określoną wartość."""
        old_y = self.y
        self.x += dx * GRID_SIZE
        self.y += dy * GRID_SIZE
        
        # Ustaw kierunek
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
        
        # Animacja skoku
        self.hop_animation = 10
        
        # Ogranicz ruch do ekranu
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
        
        # Punkty za ruch do przodu
        if dy < 0 and self.y < old_y:
            self.score += 10
    
    def reset(self):
        """Resetuje pozycję żaby do startu."""
        self.x = self.start_x
        self.y = self.start_y
        self.lives -= 1
    
    def update(self):
        """Aktualizuje animację żaby."""
        if self.hop_animation > 0:
            self.hop_animation -= 1
            # Parabola skoku
            progress = 1 - (self.hop_animation / 10)
            self.hop_height = int(math.sin(progress * math.pi) * 10)
        else:
            self.hop_height = 0
    
    def draw(self, screen: pygame.Surface):
        """Rysuje żabę na ekranie z ulepszoną grafiką."""
        draw_x = self.x
        draw_y = self.y - self.hop_height
        
        # Cień
        shadow_surf = pygame.Surface((self.size, self.size // 3), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), shadow_surf.get_rect())
        screen.blit(shadow_surf, (draw_x, self.y + self.size - 10))
        
        # Ciało żaby z gradientem
        body_center_x = draw_x + self.size // 2
        body_center_y = draw_y + self.size // 2
        body_radius = self.size // 2 - 5
        
        # Gradient ciała (symulowany z kręgami)
        for i in range(body_radius, 0, -2):
            shade = int((body_radius - i) / body_radius * 100)
            color = (50 + shade, 220 - shade // 2, 50 + shade)
            pygame.draw.circle(screen, color, (body_center_x, body_center_y), i)
        
        # Brzuch (jaśniejszy)
        belly_radius = body_radius - 8
        pygame.draw.circle(screen, (180, 255, 180), 
                         (body_center_x, body_center_y + 5), belly_radius)
        
        # Nogi (zależne od kierunku)
        leg_color = (80, 200, 80)
        
        if self.direction == "up":
            # Tylne nogi (widoczne po bokach)
            # Lewa noga
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x - 8, draw_y + self.size - 20, 15, 25))
            # Prawa noga
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x + self.size - 7, draw_y + self.size - 20, 15, 25))
        
        elif self.direction == "down":
            # Przednie łapy widoczne
            # Lewa
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x - 5, draw_y + 5, 12, 20))
            # Prawa
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x + self.size - 7, draw_y + 5, 12, 20))
        
        elif self.direction == "left":
            # Nogi po lewej stronie
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x - 10, draw_y + 10, 15, 15))
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x - 10, draw_y + 25, 15, 15))
        
        else:  # right
            # Nogi po prawej stronie
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x + self.size - 5, draw_y + 10, 15, 15))
            pygame.draw.ellipse(screen, leg_color,
                              (draw_x + self.size - 5, draw_y + 25, 15, 15))
        
        # Oczy
        eye_offset_x = 12 if self.direction in ["up", "down"] else 0
        eye_offset_y = -5 if self.direction == "up" else 0
        
        # Białka oczu
        left_eye_x = draw_x + 15 + eye_offset_x
        right_eye_x = draw_x + 35 - eye_offset_x
        eye_y = draw_y + 15 + eye_offset_y
        
        # Większe oczy z gradientem
        for i in range(7, 0, -1):
            shade = int(i / 7 * 255)
            pygame.draw.circle(screen, (shade, shade, shade), 
                             (left_eye_x, eye_y), i)
            pygame.draw.circle(screen, (shade, shade, shade), 
                             (right_eye_x, eye_y), i)
        
        pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), 7)
        pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), 7)
        
        # Źrenice (patrzą w kierunku ruchu)
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        if self.direction == "up":
            pupil_offset_y = -2
        elif self.direction == "down":
            pupil_offset_y = 2
        elif self.direction == "left":
            pupil_offset_x = -2
        elif self.direction == "right":
            pupil_offset_x = 2
        
        pygame.draw.circle(screen, BLACK, 
                         (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), 3)
        pygame.draw.circle(screen, BLACK, 
                         (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), 3)
        
        # Highlight w oczach
        pygame.draw.circle(screen, WHITE, 
                         (left_eye_x + pupil_offset_x - 1, eye_y + pupil_offset_y - 1), 1)
        pygame.draw.circle(screen, WHITE, 
                         (right_eye_x + pupil_offset_x - 1, eye_y + pupil_offset_y - 1), 1)
        
        # Uśmiech
        smile_y = draw_y + 28
        pygame.draw.arc(screen, (50, 100, 50), 
                       (draw_x + 18, smile_y - 5, 14, 8), 
                       math.pi, 2 * math.pi, 2)
    
    def get_rect(self) -> pygame.Rect:
        """Zwraca prostokąt kolizji żaby."""
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Game:
    """
    Główna klasa gry Frogger.
    
    Zarządza logiką gry, kolizjami i renderowaniem.
    """
    
    def __init__(self):
        """Inicjalizuje grę."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(
            f"Frogger Enhanced - polsoft.ITS™ London © 2026 Sebastian Januchowski"
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.input_font = pygame.font.Font(None, 48)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Menu i wyniki
        self.menu = Menu(self.screen)
        self.score_manager = ScoreManager()
        self.config_manager = ConfigManager()
        
        # Efekty
        self.particle_system = ParticleSystem()
        self.water_effect = WaterEffect()
        
        # Stan gry
        self.state = "menu"  # menu, playing, game_over, enter_name
        self.player_name = ""
        self.input_active = False
        
        # Inicjalizacja obiektów gry
        self.frog = None
        self.vehicles = []
        self.logs = []
        
        self.running = True
        
        # Display configuration file location
        print(f"\n{'='*60}")
        print(f"Configuration file: {CONFIG_FILE}")
        print(f"{'='*60}\n")
    
    def start_new_game(self):
        """Rozpoczyna nową grę."""
        self.frog = Frog(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        self.vehicles = self._create_vehicles()
        self.logs = self._create_logs()
        self.state = "playing"
        self.player_name = ""
        self.particle_system = ParticleSystem()
        
        # Aktualizuj czas ostatniej gry
        self.config_manager.update_last_played()
    
    def _create_vehicles(self) -> List[Vehicle]:
        """Tworzy listę pojazdów."""
        vehicles = []
        
        # 5 pasów ruchu
        lanes = [
            {'y': 600, 'speed': 2, 'direction': 1, 'color': (220, 20, 60), 'width': 80},
            {'y': 550, 'speed': 3, 'direction': -1, 'color': (30, 144, 255), 'width': 80},
            {'y': 500, 'speed': 1.5, 'direction': 1, 'color': (255, 215, 0), 'width': 100},
            {'y': 450, 'speed': 2.5, 'direction': -1, 'color': (138, 43, 226), 'width': 70},
            {'y': 400, 'speed': 2, 'direction': 1, 'color': (0, 206, 209), 'width': 90}
        ]
        
        for lane in lanes:
            for i in range(3):
                x = i * (SCREEN_WIDTH / 2) + random.randint(0, 100)
                vehicles.append(Vehicle(
                    x, lane['y'], lane['width'], 40,
                    lane['speed'], lane['direction'], lane['color']
                ))
        
        return vehicles
    
    def _create_logs(self) -> List[Log]:
        """Tworzy listę kłód."""
        logs = []
        
        # 4 rzędy kłód
        lanes = [
            {'y': 200, 'speed': 1.5, 'direction': 1, 'color': (139, 69, 19), 'width': 150},
            {'y': 150, 'speed': 2, 'direction': -1, 'color': (160, 82, 45), 'width': 120},
            {'y': 100, 'speed': 1, 'direction': 1, 'color': (139, 69, 19), 'width': 180},
            {'y': 50, 'speed': 2.5, 'direction': -1, 'color': (160, 82, 45), 'width': 130}
        ]
        
        for lane in lanes:
            for i in range(2):
                x = i * (SCREEN_WIDTH / 1.5) + random.randint(0, 150)
                logs.append(Log(
                    x, lane['y'], lane['width'], 40,
                    lane['speed'], lane['direction'], lane['color']
                ))
        
        return logs
    
    def draw_background(self):
        """Rysuje tło gry z ulepszoną grafiką."""
        # Rzeka z animacją
        water_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 200)
        self.water_effect.draw(self.screen, water_rect)
        
        # Droga z teksturą
        for i in range(250):
            shade = int(i / 250 * 30)
            road_color = (68 + shade, 68 + shade, 68 + shade)
            pygame.draw.line(self.screen, road_color, 
                           (0, 400 + i), (SCREEN_WIDTH, 400 + i))
        
        # Bezpieczne strefy z teksturą trawy
        # Start
        for i in range(GRID_SIZE):
            grass_shade = random.randint(-10, 10)
            grass_color = (
                max(0, min(255, 34 + grass_shade)),
                max(0, min(255, 139 + grass_shade)),
                max(0, min(255, 34 + grass_shade))
            )
            for x in range(0, SCREEN_WIDTH, 20):
                if random.random() > 0.3:
                    pygame.draw.line(self.screen, grass_color, 
                                   (x + random.randint(-5, 5), 650 + i), 
                                   (x + random.randint(-3, 3), 650 + i + random.randint(5, 15)), 1)
        
        # Środek
        for i in range(GRID_SIZE):
            grass_shade = random.randint(-10, 10)
            grass_color = (
                max(0, min(255, 34 + grass_shade)),
                max(0, min(255, 139 + grass_shade)),
                max(0, min(255, 34 + grass_shade))
            )
            for x in range(0, SCREEN_WIDTH, 20):
                if random.random() > 0.3:
                    pygame.draw.line(self.screen, grass_color, 
                                   (x + random.randint(-5, 5), 350 + i), 
                                   (x + random.randint(-3, 3), 350 + i + random.randint(5, 15)), 1)
        
        # Meta (jaśniejsza trawa)
        for i in range(GRID_SIZE):
            grass_shade = random.randint(-10, 10)
            grass_color = (
                max(0, min(255, 144 + grass_shade)),
                max(0, min(255, 238 + grass_shade)),
                max(0, min(255, 144 + grass_shade))
            )
            for x in range(0, SCREEN_WIDTH, 15):
                if random.random() > 0.2:
                    pygame.draw.line(self.screen, grass_color, 
                                   (x + random.randint(-5, 5), i), 
                                   (x + random.randint(-3, 3), i + random.randint(5, 12)), 1)
        
        # Linie na drodze z efektem świecenia
        for i in range(1, 5):
            y = 400 + i * 50
            for x in range(0, SCREEN_WIDTH, 40):
                # Główna linia
                pygame.draw.line(self.screen, WHITE, (x, y), (x + 20, y), 3)
                # Świecenie
                pygame.draw.line(self.screen, (255, 255, 255, 100), 
                               (x, y - 1), (x + 20, y - 1), 1)
                pygame.draw.line(self.screen, (255, 255, 255, 100), 
                               (x, y + 1), (x + 20, y + 1), 1)
    
    def draw_ui(self):
        """Draws the user interface with enhanced graphics."""
        # Panel tło
        panel_surf = pygame.Surface((SCREEN_WIDTH, 45), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 150), panel_surf.get_rect())
        self.screen.blit(panel_surf, (0, 0))
        
        # Score and lives with glow
        score_text = f"Score: {self.frog.score}  Lives: {self.frog.lives}"
        
        # Glow effect
        for offset in range(3, 0, -1):
            glow = self.font.render(score_text, True, (100, 100, 0))
            glow.set_alpha(50)
            self.screen.blit(glow, (10 + offset, 10 + offset))
        
        # Main text
        score_surf = self.font.render(score_text, True, GOLD)
        self.screen.blit(score_surf, (10, 10))
        
        # Lives hearts
        heart_x = 220
        for i in range(self.frog.lives):
            # Heart shape (simplified)
            pygame.draw.circle(self.screen, RED, (heart_x + i * 25, 22), 6)
            pygame.draw.circle(self.screen, RED, (heart_x + i * 25 + 10, 22), 6)
            points = [
                (heart_x + i * 25 + 5, 26),
                (heart_x + i * 25, 32),
                (heart_x + i * 25 + 10, 32)
            ]
            pygame.draw.polygon(self.screen, RED, points)
        
        # Author information
        author_text = self.small_font.render(
            "polsoft.ITS™ London © 2026 Sebastian Januchowski", 
            True, WHITE
        )
        author_rect = author_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35))
        
        # Shadow
        author_shadow = self.small_font.render(
            "polsoft.ITS™ London © 2026 Sebastian Januchowski", 
            True, BLACK
        )
        self.screen.blit(author_shadow, author_rect.move(2, 2))
        self.screen.blit(author_text, author_rect)
        
        # Config file path (smaller font)
        config_path = str(CONFIG_FILE)
        if len(config_path) > 80:
            config_path = "..." + config_path[-77:]
        
        config_text = self.font_tiny.render(
            f"Config: {config_path}",
            True, DARK_GRAY
        )
        self.screen.blit(config_text, (10, SCREEN_HEIGHT - 15))
    
    def check_collisions(self):
        """Sprawdza kolizje żaby."""
        if not self.frog:
            return
            
        frog_rect = self.frog.get_rect()
        
        # Kolizja z pojazdami
        for vehicle in self.vehicles:
            if frog_rect.colliderect(vehicle.get_rect()):
                self.particle_system.add_crash(
                    self.frog.x + self.frog.size // 2,
                    self.frog.y + self.frog.size // 2
                )
                self.frog.reset()
                if self.frog.lives <= 0:
                    self.end_game()
                return
        
        # Sprawdź czy żaba jest w wodzie
        if 50 <= self.frog.y < 250:
            on_log = False
            for log in self.logs:
                if frog_rect.colliderect(log.get_rect()):
                    on_log = True
                    # Przesuń żabę z kłodą
                    self.frog.x += log.speed * log.direction
                    # Ogranicz pozycję żaby
                    self.frog.x = max(0, min(self.frog.x, SCREEN_WIDTH - self.frog.size))
                    break
            
            if not on_log:
                self.particle_system.add_splash(
                    self.frog.x + self.frog.size // 2,
                    self.frog.y + self.frog.size // 2
                )
                self.frog.reset()
                if self.frog.lives <= 0:
                    self.end_game()
                return
        
        # Sprawdź osiągnięcie mety
        if self.frog.y < GRID_SIZE:
            self.frog.score += 100
            # Efekt sukcesu
            for _ in range(30):
                self.particle_system.add_hop(
                    self.frog.x + self.frog.size // 2,
                    self.frog.y + self.frog.size // 2
                )
            self.frog.x = self.frog.start_x
            self.frog.y = self.frog.start_y
    
    def end_game(self):
        """Kończy grę i sprawdza czy wynik jest w top 5."""
        if self.score_manager.is_high_score(self.frog.score):
            self.state = "enter_name"
            self.input_active = True
        else:
            self.state = "game_over"
    
    def save_score(self):
        """Zapisuje wynik gracza."""
        if self.player_name.strip():
            self.score_manager.add_score(self.player_name.strip(), self.frog.score)
        self.state = "game_over"
        self.input_active = False
    
    def handle_events(self):
        """Obsługuje zdarzenia pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Menu
            if self.state == "menu":
                action = self.menu.handle_input(event)
                if action == 'start':
                    self.start_new_game()
                elif action == 'quit':
                    self.running = False
            
            # Wprowadzanie imienia
            elif self.state == "enter_name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.save_score()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "game_over"
                        self.input_active = False
                    elif len(self.player_name) < 15:
                        if event.unicode.isprintable():
                            self.player_name += event.unicode
            
            # Gra
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.frog.move(0, -1)
                        self.particle_system.add_hop(
                            self.frog.x + self.frog.size // 2,
                            self.frog.y + self.frog.size
                        )
                    elif event.key == pygame.K_DOWN:
                        self.frog.move(0, 1)
                        self.particle_system.add_hop(
                            self.frog.x + self.frog.size // 2,
                            self.frog.y
                        )
                    elif event.key == pygame.K_LEFT:
                        self.frog.move(-1, 0)
                        self.particle_system.add_hop(
                            self.frog.x + self.frog.size,
                            self.frog.y + self.frog.size // 2
                        )
                    elif event.key == pygame.K_RIGHT:
                        self.frog.move(1, 0)
                        self.particle_system.add_hop(
                            self.frog.x,
                            self.frog.y + self.frog.size // 2
                        )
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
            
            # Koniec gry
            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
    
    def update(self):
        """Aktualizuje stan gry."""
        if self.state == "playing":
            for vehicle in self.vehicles:
                vehicle.update()
            
            for log in self.logs:
                log.update()
            
            if self.frog:
                self.frog.update()
            
            self.water_effect.update()
            self.particle_system.update()
            self.check_collisions()
    
    def draw_name_input(self):
        """Draws the name input screen with enhanced graphics."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 220), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))
        
        # Congratulations with glow
        for offset in range(5, 0, -1):
            congrats_glow = self.font.render("NEW HIGH SCORE!", True, 
                                           (255 - offset * 30, 215 - offset * 30, 0))
            congrats_glow.set_alpha(50)
            self.screen.blit(congrats_glow, 
                           (SCREEN_WIDTH // 2 - congrats_glow.get_width() // 2, 
                            150 + offset))
        
        congrats = self.font.render("NEW HIGH SCORE!", True, GOLD)
        self.screen.blit(congrats, 
                        (SCREEN_WIDTH // 2 - congrats.get_width() // 2, 150))
        
        score_text = self.font.render(f"Your score: {self.frog.score}", True, WHITE)
        self.screen.blit(score_text,
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
        
        # Input field
        prompt = self.font.render("Enter your name:", True, WHITE)
        self.screen.blit(prompt,
                        (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
        
        # Text field frame with glow
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 360, 400, 60)
        
        # Glow
        for offset in range(3, 0, -1):
            pygame.draw.rect(self.screen, (255, 255, 255, 50), 
                           input_rect.inflate(offset * 2, offset * 2), offset)
        
        # Main frame
        pygame.draw.rect(self.screen, WHITE, input_rect, 3)
        
        # Text entered by user
        cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0
        name_display = self.player_name + ("|" if cursor_visible and self.input_active else "")
        name_text = self.input_font.render(name_display, True, YELLOW)
        self.screen.blit(name_text,
                        (input_rect.x + 10, input_rect.y + 10))
        
        # Instructions
        instructions = [
            "ENTER - Save score",
            "ESC - Skip",
            "Max. 15 characters"
        ]
        
        y_pos = 470
        for instruction in instructions:
            text = self.small_font.render(instruction, True, LIGHT_GREEN)
            self.screen.blit(text,
                           (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 35
    
    def draw_game_over(self):
        """Draws the game over screen with enhanced graphics."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with glow
        for offset in range(5, 0, -1):
            glow = self.font.render("GAME OVER!", True, (255 - offset * 30, 0, 0))
            glow.set_alpha(50)
            self.screen.blit(glow, 
                           (SCREEN_WIDTH // 2 - glow.get_width() // 2, 
                            250 + offset))
        
        game_over_text = self.font.render("GAME OVER!", True, RED)
        score_text = self.font.render(f"Your score: {self.frog.score}", True, WHITE)
        restart_text = self.small_font.render(
            "SPACE - New Game  |  ESC - Menu",
            True, WHITE
        )
        
        self.screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 250))
        self.screen.blit(score_text, 
                       (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 310))
        self.screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 380))
    
    def draw(self):
        """Rysuje wszystkie elementy gry."""
        if self.state == "menu":
            self.menu.draw()
        
        elif self.state == "playing":
            self.screen.fill(BLACK)
            self.draw_background()
            
            # Rysuj obiekty
            for vehicle in self.vehicles:
                vehicle.draw(self.screen)
            
            for log in self.logs:
                log.draw(self.screen)
            
            # Rysuj cząsteczki za żabą
            self.particle_system.draw(self.screen)
            
            self.frog.draw(self.screen)
            self.draw_ui()
        
        elif self.state == "enter_name":
            # Rysuj grę w tle
            self.screen.fill(BLACK)
            self.draw_background()
            for vehicle in self.vehicles:
                vehicle.draw(self.screen)
            for log in self.logs:
                log.draw(self.screen)
            self.particle_system.draw(self.screen)
            self.frog.draw(self.screen)
            
            # Nakładka z wprowadzaniem imienia
            self.draw_name_input()
        
        elif self.state == "game_over":
            # Rysuj grę w tle
            self.screen.fill(BLACK)
            self.draw_background()
            for vehicle in self.vehicles:
                vehicle.draw(self.screen)
            for log in self.logs:
                log.draw(self.screen)
            self.particle_system.draw(self.screen)
            self.frog.draw(self.screen)
            
            # Nakładka z końcem gry
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """Główna pętla gry."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """
    Main function that launches the game.
    
    Displays information about the author and starts Frogger.
    """
    print("=" * 60)
    print("FROGGER - Classic Street Crossing Game (Enhanced Graphics)")
    print("=" * 60)
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")
    print(f"GitHub: {__github__}")
    print(f"Organization: {__organization__}")
    print(f"Version: {__version__}")
    print(f"Copyright: {__copyright__}")
    print("=" * 60)
    print("\nData Location:")
    print(f"Configuration file: {CONFIG_FILE}")
    print(f"Directory: {CONFIG_FILE.parent}")
    print("=" * 60)
    print("\nControls:")
    print("  MENU:")
    print("    ↑↓ - Navigation")
    print("    ENTER - Select option")
    print("    ESC - Back/Exit")
    print("\n  GAME:")
    print("    ↑↓←→ - Move frog")
    print("    ESC - Back to menu")
    print("\nObjective:")
    print("  Guide the frog across the road and river to the goal!")
    print("  Avoid cars and jump on logs in the river.")
    print("\nEnhancements:")
    print("  • Detailed frog graphics with directional facing")
    print("  • 3D-looking vehicles with shadows and lights")
    print("  • Wood-textured logs with realistic details")
    print("  • Animated water effects")
    print("  • Particle effects (splashes, dust, crashes)")
    print("  • Gradient backgrounds and enhanced UI")
    print("  • Smooth animations and visual polish")
    print("=" * 60)
    print("\nStarting game...\n")
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()